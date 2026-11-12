# Send the body on DELETE endpoints that take one (the generator defines the flags but calls c.Delete(path)).
import re,sys,glob
fixed=0
for f in glob.glob(sys.argv[1]+"/internal/cli/*.go"):
    s=open(f).read()
    if '"pp:method": "DELETE"' not in s: continue
    flags=re.findall(r'cmd\.Flags\(\)\.StringVar\(&(body\w+), "([\w-]+)"',s)
    if not flags: continue
    names={v:n for v,n in flags}
    # JSON field name: the var name minus "body", first letter lowered (bodyAltId -> altId)
    lines=["\t\t\tbody := map[string]any{}"]
    for v in names:
        key=v[4].lower()+v[5:]
        lines.append(f'\t\t\tif {v} != "" {{\n\t\t\t\tvar parsed any\n\t\t\t\tif json.Unmarshal([]byte({v}), &parsed) == nil {{\n\t\t\t\t\tbody["{key}"] = parsed\n\t\t\t\t}} else {{\n\t\t\t\t\tbody["{key}"] = {v}\n\t\t\t\t}}\n\t\t\t}}')
    old="\t\t\tdata, statusCode, err := c.Delete(path)\n"
    assert s.count(old)==1,f
    s=s.replace(old,"\n".join(lines)+"\n\t\t\tdata, statusCode, err := c.DeleteWithBody(path, body)\n")
    open(f,"w").write(s); fixed+=1
print("delete body fixed:",fixed,"cli files")
