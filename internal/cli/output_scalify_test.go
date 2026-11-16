package cli

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/spf13/cobra"
)

const wrapped = `{"workflows":[{"id":"1","name":"A","status":"draft","version":2}],"count":1}`

func TestSelectFindsWrappedList(t *testing.T) {
	got := string(filterFields(json.RawMessage(wrapped), "id,name"))
	if got != `{"workflows":[{"id":"1","name":"A"}]}` {
		t.Fatalf("got %s", got)
	}
	// dotted paths and top-level keys keep their old meaning
	if got := string(filterFields(json.RawMessage(wrapped), "workflows.id")); got != `{"workflows":[{"id":"1"}]}` {
		t.Fatalf("dotted: got %s", got)
	}
	if got := string(filterFields(json.RawMessage(wrapped), "count")); got != `{"count":1}` {
		t.Fatalf("top-level: got %s", got)
	}
}

func TestEmptySelectionDetected(t *testing.T) {
	if !isEmptySelection(filterFields(json.RawMessage(wrapped), "nope")) {
		t.Fatal("want empty")
	}
	if isEmptySelection(json.RawMessage(`{"workflows":[]}`)) {
		t.Fatal("an empty list is not a bad --select")
	}
}

func TestCompactAndCSVFindWrappedList(t *testing.T) {
	var out map[string]any
	_ = json.Unmarshal(compactFields(json.RawMessage(wrapped)), &out)
	item := out["workflows"].([]any)[0].(map[string]any)
	if _, ok := item["version"]; ok || out["count"] == nil {
		t.Fatalf("compact: got %v", out)
	}
	var b bytes.Buffer
	_ = printCSV(&b, json.RawMessage(wrapped))
	if !strings.HasPrefix(b.String(), "id,name,status,version\n1,A,draft,2") {
		t.Fatalf("csv: got %q", b.String())
	}
	// two lists: ambiguous, left alone
	if _, _, ok := listEnvelope(json.RawMessage(`{"a":[{}],"b":[{}]}`)); ok {
		t.Fatal("want no envelope")
	}
}

func TestLocationOverride(t *testing.T) {
	cfgPath := filepath.Join(t.TempDir(), "config.toml")
	_ = os.WriteFile(cfgPath, []byte("location_id = \"ACTIVE\"\n[location_tokens]\nOTHER = \"t1\"\nACTIVE = \"t0\"\n[location_names]\nOTHER = \"Other Co \"\n"), 0o600)
	cmd := &cobra.Command{Use: "contacts"}
	run := func(flag string, args ...string) (string, error) {
		t.Setenv("SCALIFY_LOCATION_ID", "")
		locationOverride = flag
		defer func() { locationOverride = "" }()
		err := applyLocationOverride(cmd, args, cfgPath)
		return os.Getenv("SCALIFY_LOCATION_ID"), err
	}
	if id, _ := run("other co"); id != "OTHER" {
		t.Fatalf("by name: got %q", id)
	}
	if _, err := run("nope"); err == nil {
		t.Fatal("unknown location: want error")
	}
	if id, _ := run("", "OTHER"); id != "OTHER" {
		t.Fatalf("argument: got %q", id)
	}
	if id, _ := run("", "someContactId"); id != "" {
		t.Fatalf("plain argument: got %q", id)
	}
}
