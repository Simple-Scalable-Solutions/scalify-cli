#!/bin/zsh
# Regenerate scalify-cli from the live v3 API docs. See scripts/regen/README.md.
set -euo pipefail
D=${0:A:h}; R=${D:h:h}
W=${REGEN_WORK:-${TMPDIR:-/tmp}/scalify-regen}
PP=${PRINTING_PRESS:-printing-press}
export GOTOOLCHAIN=go1.26.3
mkdir -p $W/pages

# 1. Pick endpoints and fetch their doc pages (cached in $W/pages; delete it to refresh).
curl -sf https://marketplace.gohighlevel.com/docs/llms/v3/llms.txt -o $W/llms.txt
python3 -I $D/select.py $W/llms.txt $D/endpoints.txt $W/selected.json
python3 -I -c 'import json,sys; [print(e["url"]) for e in json.load(open(sys.argv[1]))]' $W/selected.json |
while read -r u; do
  f=$W/pages/${${u#*/docs/ghl/}//\//__}
  [[ -s $f ]] || { curl -sf --max-time 30 "$u" -o "$f"; sleep 0.3; }
done

# 2. Merge into one OpenAPI file (white-label clean, one bearer scheme, readable names).
python3 -I $D/merge.py $W/pages $R/spec.json

# 3. Generate, then re-apply Scalify's hand fixes.
rm -rf $W/gen
$PP generate --spec $R/spec.json --name scalify --owner Scalify --spec-source official \
  --spec-url https://marketplace.gohighlevel.com/docs/llms/v3/llms.txt --output $W/gen --validate=false > $W/gen.log 2>&1
gofmt -w $W/gen/internal
for p in $D/patches/*.patch; do patch -s -p1 -d $W/gen --no-backup-if-mismatch < $p; done
cp $R/internal/cli/location_config.go $R/internal/cli/location_default.go $W/gen/internal/cli/
cp $R/internal/client/query.go $W/gen/internal/client/
cp $R/internal/mcp/code_orch_scalify.go $R/internal/mcp/code_orch_scalify_test.go $W/gen/internal/mcp/
find $W/gen/internal $W/gen/cmd -name '*.go' -print0 | xargs -0 perl -pi -e "s/scalify-pp-cli(?=[ '])/scalify-cli/g"
python3 -I $D/fix_write_query.py $R/spec.json $W/gen
python3 -I $D/fix_code_orch.py $W/gen
python3 -I $D/gen_orch_meta.py $R/spec.json $W/gen/internal/mcp/code_orch_meta.go
gofmt -w $W/gen/internal
cp $R/go.sum $W/gen/go.sum
(cd $W/gen && GOFLAGS=-mod=mod go mod tidy && go build ./... && go vet ./...)

# 4. Copy into the repo.
rsync -a --delete $W/gen/internal/ $R/internal/
rsync -a --delete $W/gen/cmd/ $R/cmd/
cp $W/gen/go.mod $W/gen/go.sum $R/
python3 -I -c 'import json,sys; p=sys.argv[1]; d=json.load(open(sys.argv[2])); d["spec_path"]="spec.json"; d.pop("printer_name",None); json.dump(d,open(p,"w"),indent=2)' $R/.printing-press.json $W/gen/.printing-press.json
# The generator picks the live-search endpoint (search.go) and one sync path (sync.go) in random
# order, so each run differs. Keep the committed picks; drop this line to take the generator's.
git -C $R checkout -- internal/cli/search.go internal/cli/sync.go
echo "regenerated; now: go test ./... and review git diff"
