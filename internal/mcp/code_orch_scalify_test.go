// Hand-owned (not generated): tests for code_orch_scalify.go.

package mcp

import (
	"context"
	"encoding/json"
	"testing"

	mcplib "github.com/mark3labs/mcp-go/mcp"
)

func TestScalifySearchRanksAndShowsParams(t *testing.T) {
	cases := map[string]string{
		"search contacts":         "contacts.search",
		"list email templates":    "emails.list-templates",
		"search conversations":    "conversations.search",
		"social media statistics": "social-media-posting.get-statistics",
		"add tag to contact":      "contacts.tags.add",
	}
	for query, want := range cases {
		req := mcplib.CallToolRequest{}
		req.Params.Arguments = map[string]any{"query": query, "limit": float64(1)}
		res, err := scalifySearch(context.Background(), req)
		if err != nil || res.IsError {
			t.Fatalf("%q: err=%v result=%+v", query, err, res)
		}
		var out struct {
			Results []struct {
				EndpointID string              `json:"endpoint_id"`
				Params     map[string][]string `json:"params"`
			} `json:"results"`
		}
		if err := json.Unmarshal([]byte(res.Content[0].(mcplib.TextContent).Text), &out); err != nil {
			t.Fatal(err)
		}
		if len(out.Results) != 1 || out.Results[0].EndpointID != want {
			t.Errorf("%q: got %+v, want %s first", query, out.Results, want)
		}
	}
}

func TestEveryEndpointHasMeta(t *testing.T) {
	for _, ep := range codeOrchEndpoints {
		if _, ok := codeOrchMeta[ep.Method+" "+ep.Path]; !ok {
			t.Errorf("%s (%s %s) has no codeOrchMeta entry", ep.ID, ep.Method, ep.Path)
		}
	}
}

func TestScalifyExecuteMissingPathParam(t *testing.T) {
	t.Setenv("HOME", t.TempDir())
	req := mcplib.CallToolRequest{}
	req.Params.Arguments = map[string]any{"endpoint_id": "contacts.get", "params": map[string]any{}}
	res, _ := scalifyExecute(context.Background(), req)
	if !res.IsError || res.Content[0].(mcplib.TextContent).Text != "missing path params: contactId" {
		t.Errorf("got %+v", res)
	}
}
