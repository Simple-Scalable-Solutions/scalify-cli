// Hand-owned (not generated): output and error helpers the generated helpers.go calls
// into (wired by scripts/regen/patches/internal_cli_helpers.go.patch).
//
// Most list endpoints wrap their items in an object ({"workflows": [...], "count": 3}),
// and the generated --select / --compact / --csv only handle a bare array, so they
// returned {} or the full payload. These helpers find the list inside the wrapper.

package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strings"

	"scalify-pp-cli/internal/config"
)

// listEnvelope returns the key and items when data is an object holding exactly one
// array of objects (the other keys being counts, cursors and the like).
func listEnvelope(data json.RawMessage) (string, []json.RawMessage, bool) {
	var obj map[string]json.RawMessage
	if json.Unmarshal(data, &obj) != nil {
		return "", nil, false
	}
	key := ""
	var items []json.RawMessage
	for k, v := range obj {
		var arr []json.RawMessage
		if json.Unmarshal(v, &arr) != nil || !allObjects(arr) {
			continue
		}
		if key != "" {
			return "", nil, false // two lists: ambiguous, leave it alone
		}
		key, items = k, arr
	}
	return key, items, key != ""
}

func allObjects(arr []json.RawMessage) bool {
	for _, el := range arr {
		if len(el) == 0 || el[0] != '{' {
			return false
		}
	}
	return true
}

// unwrapList returns the items of a wrapped list, or data unchanged.
func unwrapList(data json.RawMessage) json.RawMessage {
	if _, items, ok := listEnvelope(data); ok {
		out, _ := json.Marshal(items)
		return out
	}
	return data
}

// selectNested applies --select inside a wrapped list when no selected field names a
// top-level key (so "workflows.id" keeps working as before).
func selectNested(data json.RawMessage, paths [][]string) (json.RawMessage, bool) {
	key, items, ok := listEnvelope(data)
	if !ok {
		return nil, false
	}
	var obj map[string]json.RawMessage
	_ = json.Unmarshal(data, &obj)
	for k := range obj {
		keepWhole, subPaths := map[string]bool{}, map[string][][]string{}
		for _, p := range paths {
			if len(p) == 1 {
				keepWhole[p[0]] = true
			} else if len(p) > 1 {
				subPaths[p[0]] = append(subPaths[p[0]], p[1:])
			}
		}
		if matchSelectSegment(k, keepWhole, subPaths) != "" {
			return nil, false
		}
	}
	arr, _ := json.Marshal(items)
	out, _ := json.Marshal(map[string]json.RawMessage{key: filterFieldsRec(arr, paths)})
	return out, true
}

// warnEmptySelect tells the user when --select matched nothing, listing what it could
// have matched, instead of silently printing empty results.
func warnEmptySelect(in, out json.RawMessage, fields string) {
	if !isEmptySelection(out) {
		return
	}
	sample := in
	if _, items, ok := listEnvelope(in); ok && len(items) > 0 {
		sample = items[0]
	} else {
		var arr []json.RawMessage
		if json.Unmarshal(in, &arr) == nil && len(arr) > 0 {
			sample = arr[0]
		}
	}
	var obj map[string]json.RawMessage
	if json.Unmarshal(sample, &obj) != nil || len(obj) == 0 {
		return
	}
	keys := make([]string, 0, len(obj))
	for k := range obj {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	fmt.Fprintf(os.Stderr, "warning: --select %q matched no fields; available: %s\n", fields, strings.Join(keys, ", "))
}

// isEmptySelection: {} or [] or every item {} (recursing through a one-key wrapper).
func isEmptySelection(data json.RawMessage) bool {
	var arr []json.RawMessage
	if json.Unmarshal(data, &arr) == nil {
		if len(arr) == 0 {
			return false // nothing to select from: not the user's mistake
		}
		for _, el := range arr {
			if strings.TrimSpace(string(el)) != "{}" {
				return false
			}
		}
		return true
	}
	var obj map[string]json.RawMessage
	if json.Unmarshal(data, &obj) != nil {
		return false
	}
	if len(obj) == 0 {
		return true
	}
	if len(obj) == 1 {
		for _, v := range obj {
			return isEmptySelection(v)
		}
	}
	return false
}

// compactNested applies the list allow-list inside a wrapped list, keeping the
// wrapper's other keys (counts, cursors).
func compactNested(data json.RawMessage) (json.RawMessage, bool) {
	key, items, ok := listEnvelope(data)
	if !ok {
		return nil, false
	}
	var maps []map[string]any
	arr, _ := json.Marshal(items)
	if json.Unmarshal(arr, &maps) != nil {
		return nil, false
	}
	var obj map[string]json.RawMessage
	_ = json.Unmarshal(data, &obj)
	obj[key] = compactListFields(maps)
	out, _ := json.Marshal(obj)
	return out, true
}

// locationAuthHint explains a 401/403 in terms of locations: which saved token went
// out, and how to use or add another one.
func locationAuthHint(flags *rootFlags, status int) string {
	path := ""
	if flags != nil {
		path = flags.configPath
	}
	cfg, err := config.Load(path)
	if err != nil {
		return "\n      Run 'scalify-cli doctor' to check auth status."
	}
	_ = cfg.AuthHeader() // sets AuthSource
	used := "no location token (agency/env token)"
	if strings.HasPrefix(cfg.AuthSource, "location:") {
		id := strings.TrimPrefix(cfg.AuthSource, "location:")
		used = "the token saved for " + id
		if name := cfg.LocationNames[id]; name != "" {
			used = fmt.Sprintf("the token saved for %s (%s)", name, id)
		}
	} else if cfg.AuthSource == "" {
		used = "no token"
	}
	var b strings.Builder
	if status == 403 {
		fmt.Fprintf(&b, "\nhint: this used %s, and it can't reach this resource.", used)
		b.WriteString("\n      Another account? Add --location <id-or-name> (saved: 'scalify-cli location list'),")
		b.WriteString("\n      or save its token: scalify-cli location add <location-id> --token <token>")
		b.WriteString("\n      Same account? The token may lack a permission (scope) this call needs.")
	} else {
		fmt.Fprintf(&b, "\nhint: this used %s, and it was rejected (expired or revoked?).", used)
		b.WriteString("\n      Save a fresh one: scalify-cli location add <location-id> --token <token>")
	}
	b.WriteString("\n      Run 'scalify-cli doctor' to check auth status.")
	return b.String()
}
