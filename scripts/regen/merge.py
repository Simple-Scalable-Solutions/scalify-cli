import json,re,sys,os,glob
pages=sys.argv[1]; out=sys.argv[2]
spec={"openapi":"3.0.0","info":{"title":"Scalify","version":"v3"},
      "servers":[{"url":"https://services.leadconnectorhq.com"}],"paths":{},"components":{"schemas":{},"securitySchemes":{}},
      # MCP: a search + execute pair instead of one tool per endpoint (~62k tokens)
      "x-mcp":{"orchestration":"code","endpoint_tools":"hidden"}}
conflicts=[];bad=[];renamed=[]
for f in sorted(glob.glob(pages+"/*")):
    t=open(f).read()
    m=re.search(r'## OpenAPI Specification\s*```json\n(.*?)\n```',t,re.S)
    if not m: bad.append(os.path.basename(f)); continue
    d=json.loads(m[1])
    svc="".join(w.title() for w in re.split(r"[-_]",os.path.basename(f).split("__")[0]))
    ren={}
    for k,v in d.get("components",{}).get("schemas",{}).items():
        cur=spec["components"]["schemas"].get(k)
        if cur is not None and cur!=v: ren[k]=svc+k
    if ren:
        txt=json.dumps(d)
        for a,b in ren.items(): txt=txt.replace('"#/components/schemas/'+a+'"','"#/components/schemas/'+b+'"')
        d=json.loads(txt)
        sch=d["components"]["schemas"]
        for a,b in ren.items(): sch[b]=sch.pop(a); sch[b]["title"]=b
        renamed.extend(ren.values())
    for p,ops in d["paths"].items():
        spec["paths"].setdefault(p,{})
        for meth,op in ops.items():
            if meth in spec["paths"][p]: conflicts.append(("op",p,meth))
            spec["paths"][p][meth]=op
    for kind in ("schemas","securitySchemes"):
        for k,v in d.get("components",{}).get(kind,{}).items():
            cur=spec["components"][kind].get(k)
            if cur is not None and cur!=v: conflicts.append((kind,k,os.path.basename(f)))
            spec["components"][kind].setdefault(k,v)
json.dump(spec,open(out,"w"),indent=1)
n=sum(len(v) for v in spec["paths"].values())
print("ops",n,"schemas",len(spec["components"]["schemas"]),"bad",bad)
print("renamed",renamed)
print("conflicts",len(conflicts)); [print(c) for c in conflicts[:30]]
# Collapse every security scheme into one bearer scheme (keeps SCALIFY_TOKEN + `token` config key);
# keep each endpoint's token level and scopes in its description.
LEVEL={"Agency-Access":"agency token","Agency-Access-Only":"agency OAuth token only","Location-Access":"location token","Location-Access-Only":"location OAuth token only","bearer":"location token"}
for p,ops in spec["paths"].items():
    for meth,op in ops.items():
        notes=[]
        for req in op.pop("security",[]) or []:
            for k,sc in req.items():
                notes.append(LEVEL.get(k,k)+(" (scopes: "+", ".join(sc)+")" if sc else ""))
spec["components"]["securitySchemes"]={"bearer":{"type":"http","scheme":"bearer","bearerFormat":"JWT"}}
spec["security"]=[{"bearer":[]}]
# Fix doc gaps the generator trips on:
# - a path placeholder the page doesn't declare is sent literally ("/conversations/messages/{id}")
# - an enum path param becomes a flag while the code still reads the next argument by position
# - payments endpoints that take altId need altType too (the API rejects the call without it)
# - a path param listed after query params is read from the wrong argument (args[5] for the 6th param)
fixed=[]
for p_,ops in spec["paths"].items():
    for m_,op in ops.items():
        params=op.setdefault("parameters",[])
        names={x.get("name") for x in params}
        for ph in re.findall(r"{(\w+)}",p_):
            if ph not in names:
                params.insert(0,{"name":ph,"in":"path","required":True,"schema":{"type":"string"}}); fixed.append((m_,p_,ph))
        for x in params:
            sch=x.get("schema",{})
            if x.get("in")=="path" and "enum" in sch:
                x["description"]=(x.get("description","")+" One of: "+", ".join(map(str,sch.pop("enum")))).strip()
                fixed.append((m_,p_,x["name"]+" enum"))
        order=[x.get("in")=="path" for x in params]
        if order!=sorted(order,reverse=True):
            params.sort(key=lambda x:x.get("in")!="path"); fixed.append((m_,p_,"path params first"))
        if "altId" in names and "altType" not in names:
            params.append({"name":"altType","in":"query","required":True,"description":"Always location","schema":{"type":"string","enum":["location"]}})
            fixed.append((m_,p_,"altType"))
print("doc gaps fixed",len(fixed)); [print(" ",*x) for x in fixed]
# Readable command names: override operationIds that produce clumsy commands.
ren={}
for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"renames.tsv")):
    if line.strip():
        k,v=line.rstrip("\n").split("\t"); ren[k]=v
used=set()
for p_,ops in spec["paths"].items():
    for m_,op in ops.items():
        k=m_.upper()+" "+p_
        if k in ren: op["operationId"]=ren[k]; used.add(k)
missing=set(ren)-used
assert not missing, missing
# White-label: no provider names or provider doc links in any text the CLI shows.
def clean(x):
    if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
    if isinstance(x,list): return [clean(v) for v in x]
    if isinstance(x,str):
        x=re.sub(r'\[([^\]]+)\]\((?:/docs/|https?://[^)]*(?:gohighlevel|leadconnector|highlevel)[^)]*)[^)]*\)',r'\1',x)
        x=re.sub(r'https?://\S*(?:gohighlevel|leadconnector|highlevel)\S*','',x).replace("services.leadconnectorhq.com","SERVICES_HOST")
        x=re.sub(r'<br\s*/?>',' ',x); x=re.sub(r'</?[a-zA-Z][^>]*>','',x)
        x=re.sub(r'(?i)\s*Documentation Link\s*-\s*\S*','',x)
        x=re.sub(r'(?i)go ?high ?level|high ?level|lead ?connector|\bGHL\b','Scalify',x)
        return x.replace("SERVICES_HOST","services.leadconnectorhq.com")
    return x
for p_,ops in spec["paths"].items():
    for m_,op in ops.items(): ops[m_]=clean(op)
spec["components"]["schemas"]=clean(spec["components"]["schemas"])
json.dump(spec,open(out,"w"),indent=1)
print("security collapsed, cleaned")
