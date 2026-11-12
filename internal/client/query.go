package client

import (
	"net/url"
	"strings"
)

// WithQuery appends non-empty params to path as a query string. Post, Put,
// Patch and Delete take no params map, so endpoints that need query params on
// a write (e.g. locationId on POST /workflows/search) carry them in the path.
func WithQuery(path string, params map[string]string) string {
	q := url.Values{}
	for k, v := range params {
		if v != "" {
			q.Set(k, v)
		}
	}
	if len(q) == 0 {
		return path
	}
	sep := "?"
	if strings.Contains(path, "?") {
		sep = "&"
	}
	return path + sep + q.Encode()
}
