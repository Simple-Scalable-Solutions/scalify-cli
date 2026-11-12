# Send query params on non-GET endpoints (the generator only wires them for GET).
import json,re,sys,glob,os
spec=json.load(open(sys.argv[1])); g=sys.argv[2]
want={}
for p,ops in spec["paths"].items():
    for m,op in ops.items():
        q=[x["name"] for x in op.get("parameters",[]) if x.get("in")=="query"]
        if m!="get" and q: want[(m.upper(),p)]=q
fixed=0
for f in glob.glob(g+"/internal/cli/*.go"):
    s=open(f).read()
    m=re.search(r'"pp:method": "(\w+)", "pp:path": "([^"]+)"',s)
    if not m or (m[1],m[2]) not in want: continue
    pairs=[]
    for name in want[(m[1],m[2])]:
        var="flag"+name[0].upper()+name[1:]
        if re.search(r'\bvar '+var+r' string\b',s): pairs.append(f'"{name}": {var}')
    if not pairs: continue
    call=re.search(r'\n(\t+)(data, (?:\w+, )?err :?= c\.(?:Post|Put|Patch|Delete)(?:WithHeaders)?\(path)',s)
    assert call, f
    ins=f'\n{call[1]}path = client.WithQuery(path, map[string]string{{{", ".join(pairs)}}})'
    s=s[:call.start()]+ins+s[call.start():]
    if '"scalify-pp-cli/internal/client"' not in s:
        s=s.replace('import (\n','import (\n\t"scalify-pp-cli/internal/client"\n',1)
    open(f,"w").write(s); fixed+=1
t=g+"/internal/mcp/tools.go"; s=open(t).read()
old="\t\tvar data json.RawMessage\n"
assert s.count(old)==1
s=s.replace(old,'\t\tif method != "GET" {\n\t\t\tpath = client.WithQuery(path, params)\n\t\t}\n'+old)
open(t,"w").write(s)
print("write-query fixed:",fixed,"cli files + mcp handler")
