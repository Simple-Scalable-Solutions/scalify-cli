# Wire sync and tail to internal/cli/sync_scalify.go: the generator syncs only list endpoints with
# no required params, and nearly every v3 list endpoint requires the location.
import re,sys
g=sys.argv[1]+"/internal/cli/"
def sub(s,a,b,f):
    assert s.count(a)==1,(f,a); return s.replace(a,b)
f=g+"sync.go"; s=open(f).read()
s=re.sub(r'(func defaultSyncResources\(\) \[\]string \{\n).*?\n\}\n',r'\1\treturn scalifySyncResources()\n}\n',s,count=1,flags=re.S)
s=re.sub(r'(func syncResourcePath\(resource string\) \(string, error\) \{\n).*?\n\}\n',
         r'\1\tif _, ok := scalifySyncDefs[resource]; ok {\n\t\treturn resource, nil\n\t}\n\treturn "", fmt.Errorf("unknown sync resource %q", resource)\n}\n',s,count=1,flags=re.S)
s=re.sub(r'(func dependentResourceDefs\(\) \[\]dependentResourceDef \{\n).*?\n\}\n',r'\1\treturn nil\n}\n',s,count=1,flags=re.S)
i=s.index("func syncResource(")
j=s.index("\nfunc ",i+1)
s=s[:i]+sub(s[i:j],"\t\tdata, err := c.Get(path, params)\n","\t\tdata, err := scalifySyncFetch(c, resource, maxPages)\n\t\t_, _ = path, params\n",f)+s[j:]
s=sub(s,"\t\t\tc.NoCache = true\n\n\t\t\tif dbPath == \"\" {","\t\t\tc.NoCache = true\n\t\t\tsyncLocationID = c.Config.LocationID\n\n\t\t\tif dbPath == \"\" {",f)
s=sub(s,'var genericIDFieldFallbacks = []string{"id",','var genericIDFieldFallbacks = []string{"id", "_id",',f)
open(f,"w").write(s)
# Payments records (orders, transactions) use _id.
f=sys.argv[1]+"/internal/store/store.go"; s=open(f).read()
s=sub(s,'var genericIDFieldFallbacks = []string{"id",','var genericIDFieldFallbacks = []string{"id", "_id",',f)
open(f,"w").write(s)
f=g+"tail.go"; s=open(f).read()
s=sub(s,"\t\t\tc.NoCache = true\n\n\t\t\tpath := \"/\" + resource\n","\t\t\tc.NoCache = true\n\t\t\tsyncLocationID = c.Config.LocationID\n\n\t\t\tpath := \"/\" + resource\n",f)
s=sub(s,"\tdata, err := c.Get(path, nil)\n","""\tvar data json.RawMessage
	var err error
	if _, ok := scalifySyncDefs[strings.TrimPrefix(path, "/")]; ok {
		data, err = scalifySyncFetch(c, strings.TrimPrefix(path, "/"), 1)
	} else {
		data, err = c.Get(path, nil)
	}
""",f)
s=re.sub(r'(func tailKnownResources\(\) \[\]string \{\n).*?\n\}\n',r'\1\treturn scalifySyncResources()\n}\n',s,count=1,flags=re.S)
if '\t"strings"\n' not in s: s=s.replace('import (\n','import (\n\t"strings"\n',1)
open(f,"w").write(s)
# search with no --type: also search the generic table (contacts, workflows and the rest of sync's resources).
f=g+"search.go"; s=open(f).read()
a="\t\t\tdefault:\n\t\t\t\t// Unrecognized type"
b="""\t\t\t\t{
\t\t\t\t\tpartial, searchErr := db.Search(query, limit)
\t\t\t\t\tif searchErr != nil {
\t\t\t\t\t\treturn fmt.Errorf("search failed: %w", searchErr)
\t\t\t\t\t}
\t\t\t\t\tfor _, r := range partial {
\t\t\t\t\t\tif !seen[string(r)] {
\t\t\t\t\t\t\tseen[string(r)] = true
\t\t\t\t\t\t\tresults = append(results, r)
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t}
"""
if "partial, searchErr := db.Search(query, limit)" not in s:
    s=sub(s,a,b+a,f); open(f,"w").write(s)
print("sync + tail + search: scalify resources wired")
