package cli

import (
	"github.com/spf13/cobra"

	"scalify-pp-cli/internal/config"
)

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
