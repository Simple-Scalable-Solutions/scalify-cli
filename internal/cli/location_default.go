package cli

import (
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"

	"scalify-pp-cli/internal/config"
)

// locationOverride is the global --location flag: run one command against another
// saved location without switching the active one.
var locationOverride string

func addLocationFlag(root *cobra.Command) {
	root.PersistentFlags().StringVar(&locationOverride, "location", "",
		"Run this command against a saved location (id or name) using its token; the active location is unchanged")
}

// applyLocationOverride picks the location, and so the saved token, for this one
// command: --location first, else a saved location id passed as an argument or as
// --location-id (so `locations custom-values list <id>` uses <id>'s token). It works
// through SCALIFY_LOCATION_ID for this process only, never by rewriting the config.
func applyLocationOverride(cmd *cobra.Command, args []string, configPath string) error {
	// `location` and `auth` manage the config itself; an override would get saved into it.
	if p := strings.Fields(cmd.CommandPath()); len(p) > 1 && (p[1] == "location" || p[1] == "auth") {
		return nil
	}
	cfg, err := config.Load(configPath)
	if err != nil {
		return nil
	}
	if locationOverride != "" {
		id := cfg.ResolveLocation(locationOverride)
		for lid, name := range cfg.LocationNames { // names as typed: any case, stray spaces
			if strings.EqualFold(strings.TrimSpace(name), strings.TrimSpace(locationOverride)) {
				id = lid
			}
		}
		if cfg.LocationTokens[id] == "" {
			return usageErr(fmt.Errorf("no saved token for location %q: see 'scalify-cli location list', or add it with 'scalify-cli location add <location-id> --token <token>'", locationOverride))
		}
		return os.Setenv("SCALIFY_LOCATION_ID", id)
	}
	cands := args
	if f := cmd.Flags().Lookup("location-id"); f != nil && f.Changed {
		cands = append([]string{f.Value.String()}, args...)
	}
	for _, a := range cands {
		if a != cfg.LocationID && cfg.LocationTokens[a] != "" {
			return os.Setenv("SCALIFY_LOCATION_ID", a)
		}
	}
	return nil
}

// applyLocationDefault fills an unset --location-id flag from the active
// location (`scalify-cli location use`, or SCALIFY_LOCATION_ID). Only commands
// whose endpoint takes a locationId have the flag, so endpoints that reject an
// unexpected locationId never receive one.
func applyLocationDefault(cmd *cobra.Command, configPath string) {
	f := cmd.Flags().Lookup("location-id")
	if f == nil || f.Changed {
		return
	}
	cfg, err := config.Load(configPath)
	if err != nil || cfg.LocationID == "" {
		return
	}
	_ = cmd.Flags().Set("location-id", cfg.LocationID)
}
