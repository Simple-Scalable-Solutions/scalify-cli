// Hand-owned (not generated): Scalify's search + execute MCP handlers, replacing the
// generator's code_orch.go ones, which rank loosely, don't show params, put query params in the
// body on writes, miss some path placeholders and never fill the location.
// scripts/regen/fix_code_orch.py points the tool registrations here on every regen.

package mcp

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"time"

	mcplib "github.com/mark3labs/mcp-go/mcp"

	"scalify-pp-cli/internal/client"
	"scalify-pp-cli/internal/config"
)

type codeOrchParams struct {
	Path  []string
	Query []string
	Body  []string
}

var placeholderRe = regexp.MustCompile(`\{(\w+)\}`)

// paramName strips the "*" (required) and ":type" suffixes from a codeOrchMeta entry.
func paramName(p string) string {
	p, _, _ = strings.Cut(p, ":")
	return strings.TrimSuffix(p, "*")
}

func hasParam(list []string, name string) bool {
	for _, p := range list {
		if paramName(p) == name {
			return true
		}
	}
	return false
}

func queryValue(v any) string {
	if xs, ok := v.([]any); ok {
		parts := make([]string, len(xs))
		for i, x := range xs {
			parts[i] = fmt.Sprintf("%v", x)
		}
		return strings.Join(parts, ",")
	}
	return fmt.Sprintf("%v", v)
}

// stem drops a plural "s" so "templates" matches "template".
func stem(t string) string {
	if len(t) > 3 && strings.HasSuffix(t, "s") && !strings.HasSuffix(t, "ss") {
		return t[:len(t)-1]
	}
	return t
}

// termScore is how well one query term matches an endpoint: a hit in its id counts
// most, then an exact keyword, then a keyword sharing a prefix.
func termScore(t string, id []string, keywords []string) int {
	for _, k := range id {
		if stem(k) == t {
			return 4
		}
	}
	best := 0
	for _, k := range keywords {
		k = stem(k)
		switch {
		case k == t:
			return 2
		case len(t) >= 4 && (strings.HasPrefix(k, t) || strings.HasPrefix(t, k) && len(k) >= 4):
			best = 1
		}
	}
	return best
}

// scalifySearch ranks endpoints for a query and returns each one's params, so the
// agent can build a scalify_execute call without guessing.
func scalifySearch(ctx context.Context, req mcplib.CallToolRequest) (*mcplib.CallToolResult, error) {
	args := req.GetArguments()
	query, _ := args["query"].(string)
	if strings.TrimSpace(query) == "" {
		return mcplib.NewToolResultError("query is required"), nil
	}
	limit := 10
	if v, ok := args["limit"].(float64); ok && v > 0 {
		limit = int(v)
	}
	var terms []string
	for _, t := range codeOrchKeywords("", "", query, "") {
		terms = append(terms, stem(t))
	}

	type scored struct {
		ep    *codeOrchEndpoint
		score int
	}
	var results []scored
	for i := range codeOrchEndpoints {
		ep := &codeOrchEndpoints[i]
		id := strings.FieldsFunc(ep.ID, func(r rune) bool { return r == '.' || r == '-' })
		score := 0
		for _, t := range terms {
			score += termScore(t, id, ep.keywords)
		}
		if score > 0 {
			results = append(results, scored{ep, score})
		}
	}
	sort.SliceStable(results, func(i, j int) bool { return results[i].score > results[j].score })
	if len(results) > limit {
		results = results[:limit]
	}

	out := make([]map[string]any, 0, len(results))
	for _, r := range results {
		entry := map[string]any{"endpoint_id": r.ep.ID, "method": r.ep.Method, "path": r.ep.Path, "summary": r.ep.Summary}
		if meta, ok := codeOrchMeta[r.ep.Method+" "+r.ep.Path]; ok {
			params := map[string][]string{}
			if len(meta.Path) > 0 {
				params["path"] = meta.Path
			}
			if len(meta.Query) > 0 {
				params["query"] = meta.Query
			}
			if len(meta.Body) > 0 {
				params["body"] = meta.Body
			}
			entry["params"] = params
		}
		out = append(out, entry)
	}
	data, _ := json.Marshal(map[string]any{"count": len(out), "results": out})
	return mcplib.NewToolResultText(string(data)), nil
}

// scalifyExecute calls one endpoint. Path placeholders and the endpoint's query params
// come out of params by name; the rest is the query string (GET, DELETE) or JSON body
// (POST/PUT/PATCH, and DELETE fields the endpoint documents as body).
// locationId defaults to the active location when the endpoint takes one.
func scalifyExecute(ctx context.Context, req mcplib.CallToolRequest) (*mcplib.CallToolResult, error) {
	args := req.GetArguments()
	id, _ := args["endpoint_id"].(string)
	var ep *codeOrchEndpoint
	for i := range codeOrchEndpoints {
		if codeOrchEndpoints[i].ID == id {
			ep = &codeOrchEndpoints[i]
			break
		}
	}
	if ep == nil {
		return mcplib.NewToolResultError(fmt.Sprintf("unknown endpoint_id %q — call scalify_search to discover valid ids", id)), nil
	}
	meta := codeOrchMeta[ep.Method+" "+ep.Path]

	params := map[string]any{}
	if in, ok := args["params"].(map[string]any); ok {
		for k, v := range in {
			params[k] = v
		}
	}

	home, _ := os.UserHomeDir()
	cfg, err := config.Load(filepath.Join(home, ".config", "scalify-pp-cli", "config.toml"))
	if err != nil {
		return mcplib.NewToolResultError(fmt.Sprintf("loading config: %v", err)), nil
	}
	if _, set := params["locationId"]; !set && cfg.LocationID != "" &&
		(hasParam(meta.Path, "locationId") || hasParam(meta.Query, "locationId") || hasParam(meta.Body, "locationId") ||
			strings.Contains(ep.Path, "{locationId}")) {
		params["locationId"] = cfg.LocationID
	}

	var missing []string
	path := placeholderRe.ReplaceAllStringFunc(ep.Path, func(m string) string {
		name := m[1 : len(m)-1]
		v, ok := params[name]
		if !ok {
			missing = append(missing, name)
			return m
		}
		delete(params, name)
		return fmt.Sprintf("%v", v)
	})
	if len(missing) > 0 {
		return mcplib.NewToolResultError(fmt.Sprintf("missing path params: %s", strings.Join(missing, ", "))), nil
	}

	query := map[string]string{}
	for k, v := range params {
		if hasParam(meta.Query, k) || ep.Method == "GET" || ep.Method == "DELETE" && !hasParam(meta.Body, k) {
			query[k] = queryValue(v)
			delete(params, k)
		}
	}

	c := client.New(cfg, 30*time.Second, 0)
	c.NoCache = true
	var data json.RawMessage
	switch ep.Method {
	case "GET":
		data, err = c.Get(path, query)
	case "DELETE":
		if len(params) > 0 {
			data, _, err = c.DeleteWithBody(client.WithQuery(path, query), params)
		} else {
			data, _, err = c.Delete(client.WithQuery(path, query))
		}
	case "POST":
		data, _, err = c.Post(client.WithQuery(path, query), params)
	case "PUT":
		data, _, err = c.Put(client.WithQuery(path, query), params)
	case "PATCH":
		data, _, err = c.Patch(client.WithQuery(path, query), params)
	default:
		return mcplib.NewToolResultError(fmt.Sprintf("unsupported method %q", ep.Method)), nil
	}
	if err != nil {
		return mcplib.NewToolResultError(err.Error()), nil
	}
	return mcplib.NewToolResultText(string(data)), nil
}
