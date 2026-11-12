// Hand-owned (not generated): what `sync` pulls and how. The generator only syncs list
// endpoints with no required params, and almost every v3 list endpoint requires the
// location, so it was left with nothing a location token can read. These resources are
// fetched for the active location, all pages at once, and handed to the generated sync
// loop as one array. scripts/regen/fix_sync.py wires this into sync.go on every regen.

package cli

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"

	"scalify-pp-cli/internal/client"
)

// syncLocationID is the location sync reads; set from the active location in sync's RunE.
var syncLocationID string

type scalifySyncDef struct {
	Path   string            // {locationId} is filled in
	Query  map[string]string // extra query params; "{locationId}" values are filled in
	Paging string            // "", "offset", "skip", "page", or "post-page" (POST search with page/pageLimit)
	Limit  int
	Items  string // dotted path to the item array when it is nested (e.g. "results.accounts")
}

var syncLocQuery = map[string]string{"locationId": "{locationId}"}
var syncAltQuery = map[string]string{"altId": "{locationId}", "altType": "location"}

// scalifySyncDefs: the resources `sync` pulls by default, by local table name.
var scalifySyncDefs = map[string]scalifySyncDef{
	"location":        {Path: "/locations/{locationId}"},
	"contacts":        {Path: "/contacts/search", Paging: "post-page", Limit: 100},
	"conversations":   {Path: "/conversations/search", Query: syncLocQuery, Limit: 100},
	"opportunities":   {Path: "/opportunities/search", Query: syncLocQuery, Paging: "page", Limit: 100},
	"pipelines":       {Path: "/opportunities/pipelines", Query: syncLocQuery},
	"calendars":       {Path: "/calendars/", Query: syncLocQuery},
	"calendar_groups": {Path: "/calendars/groups", Query: syncLocQuery},
	"workflows":       {Path: "/workflows/", Query: syncLocQuery},
	"campaigns":       {Path: "/campaigns/", Query: syncLocQuery},
	"forms":           {Path: "/forms/", Query: syncLocQuery, Paging: "skip", Limit: 50},
	"surveys":         {Path: "/surveys/", Query: syncLocQuery, Paging: "skip", Limit: 50},
	"funnels":         {Path: "/funnels/funnel/list", Query: syncLocQuery, Paging: "offset", Limit: 50},
	"links":           {Path: "/links/", Query: syncLocQuery},
	"custom_fields":   {Path: "/locations/{locationId}/customFields"},
	"custom_values":   {Path: "/locations/{locationId}/customValues"},
	"tags":            {Path: "/locations/{locationId}/tags"},
	"email_templates": {Path: "/emails/locations/{locationId}/templates", Paging: "offset", Limit: 50},
	"email_campaigns": {Path: "/emails/locations/{locationId}/campaigns/emails", Paging: "offset", Limit: 20},
	"products":        {Path: "/products/", Query: syncLocQuery, Paging: "offset", Limit: 100},
	"invoices":        {Path: "/invoices/", Query: syncAltQuery, Paging: "offset", Limit: 100},
	"estimates":       {Path: "/invoices/estimate/list", Query: syncAltQuery, Paging: "offset", Limit: 100},
	"orders":          {Path: "/payments/orders", Query: syncAltQuery, Paging: "offset", Limit: 100},
	"transactions":    {Path: "/payments/transactions", Query: syncAltQuery, Paging: "offset", Limit: 100},
	"subscriptions":   {Path: "/payments/subscriptions", Query: syncAltQuery, Paging: "offset", Limit: 100},
	"coupons":         {Path: "/payments/coupon/list", Query: syncAltQuery, Paging: "offset", Limit: 100},
	"social_accounts": {Path: "/social-media-posting/{locationId}/accounts", Items: "results.accounts"},
	"blogs":           {Path: "/blogs/site/all", Query: syncLocQuery, Paging: "skip", Limit: 50},
	"businesses":      {Path: "/businesses/", Query: syncLocQuery},
	"courses":         {Path: "/courses/products", Query: syncLocQuery},
	"proposals":       {Path: "/proposals/document", Query: syncLocQuery, Paging: "skip", Limit: 20},
	"objects":         {Path: "/objects/", Query: syncLocQuery},
}

// scalifySyncResources lists the default resources in a stable order.
func scalifySyncResources() []string {
	return []string{"location", "contacts", "conversations", "opportunities", "pipelines", "calendars",
		"calendar_groups", "workflows", "campaigns", "forms", "surveys", "funnels", "links", "custom_fields",
		"custom_values", "tags", "email_templates", "email_campaigns", "products", "invoices", "estimates",
		"orders", "transactions", "subscriptions", "coupons", "social_accounts", "blogs", "businesses",
		"courses", "proposals", "objects"}
}

// scalifySyncFetch reads every page of a resource (up to maxPages; 0 = no cap) and returns
// the items as one JSON array, so the generated loop stores them in one pass.
func scalifySyncFetch(c any, resource string, maxPages int) (json.RawMessage, error) {
	def, ok := scalifySyncDefs[resource]
	if !ok {
		return nil, fmt.Errorf("unknown sync resource %q", resource)
	}
	if syncLocationID == "" {
		return nil, fmt.Errorf("no active location: run 'scalify-cli location use <id>' or set SCALIFY_LOCATION_ID")
	}
	cl, ok := c.(*client.Client)
	if !ok {
		return nil, fmt.Errorf("sync needs the API client")
	}
	path := strings.ReplaceAll(def.Path, "{locationId}", syncLocationID)

	all := []json.RawMessage{}
	for page := 0; maxPages == 0 || page < maxPages; page++ {
		params := map[string]string{}
		for k, v := range def.Query {
			params[k] = strings.ReplaceAll(v, "{locationId}", syncLocationID)
		}
		limit := strconv.Itoa(def.Limit)
		switch def.Paging {
		case "offset":
			params["limit"], params["offset"] = limit, strconv.Itoa(page*def.Limit)
		case "skip":
			params["limit"], params["skip"] = limit, strconv.Itoa(page*def.Limit)
		case "page":
			params["limit"], params["page"] = limit, strconv.Itoa(page+1)
		case "":
			if def.Limit > 0 {
				params["limit"] = limit
			}
		}

		var data json.RawMessage
		var err error
		if def.Paging == "post-page" {
			data, _, err = cl.Post(path, map[string]any{"locationId": syncLocationID, "pageLimit": def.Limit, "page": page + 1})
		} else {
			data, err = cl.Get(path, params)
		}
		if err != nil {
			if page > 0 {
				break // keep what earlier pages returned
			}
			return nil, err
		}

		if def.Items != "" {
			for _, key := range strings.Split(def.Items, ".") {
				var env map[string]json.RawMessage
				if json.Unmarshal(data, &env) != nil {
					break
				}
				data = env[key]
			}
		}
		items, _, _ := extractPageItems(data, "")
		if len(items) == 0 && page == 0 {
			// A single record (e.g. the location itself): store its inner object.
			var env map[string]json.RawMessage
			if json.Unmarshal(data, &env) == nil {
				for _, v := range env {
					if len(v) > 0 && v[0] == '{' {
						return json.RawMessage("[" + string(v) + "]"), nil
					}
				}
			}
		}
		all = append(all, items...)
		if def.Paging == "" || def.Limit == 0 || len(items) < def.Limit {
			break
		}
	}
	return json.Marshal(all)
}
