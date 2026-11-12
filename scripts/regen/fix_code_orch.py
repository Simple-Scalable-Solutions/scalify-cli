# Point the search + execute MCP tools at the hand-owned handlers in internal/mcp/code_orch_scalify.go.
import sys
f=sys.argv[1]+"/internal/mcp/code_orch.go"; s=open(f).read()
subs=[("\t\thandleCodeOrchSearch,\n","\t\tscalifySearch,\n"),
      ("\t\thandleCodeOrchExecute,\n","\t\tscalifyExecute,\n"),
      ("Returns a ranked list of {endpoint_id, method, path, summary} entries. Call this first to find the endpoint to execute.",
       "Returns a ranked list of {endpoint_id, method, path, summary, params} entries; params lists the path, query and body fields (* = required, then :type). Call this first to find the endpoint to execute."),
      ("Params are passed as a JSON object; path placeholders and query strings are resolved automatically.",
       "Params are one flat JSON object: path and query fields are taken out by name, the rest is the JSON body (POST/PUT/PATCH) or query string (GET/DELETE). locationId defaults to the active location."),
      ("Path placeholders match by name; remaining entries become query string on GET/DELETE or JSON body on POST/PUT/PATCH.",
       "Flat object of the endpoint's params, by name (see params in scalify_search results)."),
]
for a,b in subs:
    assert s.count(a)==1,a
    s=s.replace(a,b)
open(f,"w").write(s)
print("code orch: scalify handlers wired")
