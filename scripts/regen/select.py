"""Pick the endpoints listed in endpoints.txt out of the live llms.txt index.

usage: select.py <llms.txt> <endpoints.txt> <out.json>
Fails if a listed endpoint is no longer in the live docs.
"""
import json, re, sys

index, wanted_file, out = sys.argv[1:4]
entries = {}
for line in open(index):
    m = re.match(r'- \[([^\]]+)\]\((\S+\.md)\): (GET|POST|PUT|PATCH|DELETE) (/\S+)', line)
    if m:
        entries.setdefault(f"{m[3]} {m[4]}", {"title": m[1], "url": m[2], "method": m[3], "path": m[4]})
wanted = [l.strip() for l in open(wanted_file) if l.strip() and not l.startswith("#")]
missing = [w for w in wanted if w not in entries]
if missing:
    sys.exit("not in live docs any more:\n  " + "\n  ".join(missing))
json.dump([entries[w] for w in wanted], open(out, "w"), indent=0)
print(len(wanted), "endpoints selected")
