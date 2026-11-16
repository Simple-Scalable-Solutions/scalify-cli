# Make list output work when the API wraps the list in an object ({"workflows": [...]}):
# the generated commands count, table and CSV-render only bare arrays (helpers in output_scalify.go),
# and when piped they take the JSON path before looking at --csv.
import sys,glob
SUBS=[
    ("if flags.asJSON || !isTerminal(cmd.OutOrStdout()) {", "if !flags.csv && (flags.asJSON || !isTerminal(cmd.OutOrStdout())) {"),
    ("_ = json.Unmarshal(data, &countItems)", "_ = json.Unmarshal(unwrapList(data), &countItems)"),
    ("if json.Unmarshal(data, &items) == nil && len(items) > 0 {", "if json.Unmarshal(unwrapList(data), &items) == nil && len(items) > 0 {"),
]
counts=[0]*len(SUBS)
for f in glob.glob(sys.argv[1]+"/internal/cli/*.go"):
    s=open(f).read(); o=s
    for i,(a,b) in enumerate(SUBS):
        counts[i]+=s.count(a); s=s.replace(a,b)
    if s!=o: open(f,"w").write(s)
assert all(counts), counts  # a zero means the generator changed: re-check these patterns
print("output fixed:", counts)
