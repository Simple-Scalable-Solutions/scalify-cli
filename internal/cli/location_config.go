package cli

import (
	"encoding/json"
	"fmt"
	"os"
	"sort"

	"scalify-pp-cli/internal/client"
	"scalify-pp-cli/internal/config"
	"github.com/spf13/cobra"
)

// fetchLocationName calls GET /locations/{id} authenticated with the location's
// own PIT — no agency token required. Returns empty string on any error.
func fetchLocationName(flags *rootFlags, id, pit string) string {
	if pit == "" {
		return ""
	}
	// Load config only for base URL / env overrides; replace auth with the PIT.
	cfg, err := config.Load(flags.configPath)
	if err != nil {
		cfg = &config.Config{BaseURL: "https://services.leadconnectorhq.com"}
	}
	cfg.ScalifyToken = pit
	cfg.AuthHeaderVal = ""
	cfg.AccessToken = ""

	c := client.New(cfg, flags.timeout, flags.rateLimit)
	data, err := c.Get("/locations/"+id, nil)
	if err != nil {
		return ""
	}
	var resp struct {
		Location struct {
			Name string `json:"name"`
		} `json:"location"`
	}
	if err := json.Unmarshal(data, &resp); err != nil {
		return ""
	}
	return resp.Location.Name
}

func newLocationConfigCmd(flags *rootFlags) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "location",
		Short: "Manage active Scalify location (sub-account)",
	}
	cmd.AddCommand(newLocationUseCmd(flags))
	cmd.AddCommand(newLocationAddCmd(flags))
	cmd.AddCommand(newLocationListCmd(flags))
	cmd.AddCommand(newLocationShowCmd(flags))
	return cmd
}

func newLocationUseCmd(flags *rootFlags) *cobra.Command {
	var token string
	cmd := &cobra.Command{
		Use:   "use <location-id-or-name>",
		Short: "Switch to a location (sub-account)",
		Long: `Switch the active location. Accepts a location ID or a saved name.
If you have already saved a token for this location via 'location add',
no --token is needed. Otherwise provide --token to save it and switch in one step.`,
		Example: `  scalify-cli location use OGpQQmmQzXMpwEkaNxHr
  scalify-cli location use "My Office"
  scalify-cli location use OGpQQmmQzXMpwEkaNxHr --token pit-abc123`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			cfg, err := config.Load(flags.configPath)
			if err != nil {
				return configErr(err)
			}
			id := cfg.ResolveLocation(args[0])
			_, hasSaved := cfg.LocationTokens[id]
			if token == "" && !hasSaved {
				return usageErr(fmt.Errorf(
					"no saved token for location %s\nProvide one with: scalify-cli location use %s --token <pit>",
					id, id,
				))
			}
			name := cfg.LocationNames[id]
			if name == "" {
				// Use the provided PIT, or fall back to the already-saved one.
				pit := token
				if pit == "" {
					pit = cfg.LocationTokens[id]
				}
				name = fetchLocationName(flags, id, pit)
			}
			if err := cfg.SaveLocation(id, name, token); err != nil {
				return configErr(fmt.Errorf("switching location: %w", err))
			}
			if flags.asJSON {
				out := map[string]any{"location_id": id, "config": cfg.Path}
				if name != "" {
					out["name"] = name
				}
				return printJSONFiltered(cmd.OutOrStdout(), out, flags)
			}
			if name != "" {
				fmt.Fprintf(cmd.OutOrStdout(), "Switched to location %s (%s)\n", name, id)
			} else {
				fmt.Fprintf(cmd.OutOrStdout(), "Switched to location %s\n", id)
			}
			return nil
		},
	}
	cmd.Flags().StringVar(&token, "token", "", "PIT for this location (saved for future switches)")
	return cmd
}

func newLocationAddCmd(flags *rootFlags) *cobra.Command {
	var token, name string
	cmd := &cobra.Command{
		Use:   "add <location-id>",
		Short: "Save a location and its PIT token (without switching)",
		Example: `  scalify-cli location add OGpQQmmQzXMpwEkaNxHr --token pit-abc123
  scalify-cli location add OGpQQmmQzXMpwEkaNxHr --token pit-abc123 --name "My Office"`,
		Args: cobra.ExactArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			if token == "" {
				return usageErr(fmt.Errorf("--token is required"))
			}
			cfg, err := config.Load(flags.configPath)
			if err != nil {
				return configErr(err)
			}
			id := args[0]
			if name == "" {
				name = fetchLocationName(flags, id, token)
			}
			if err := cfg.AddLocation(id, name, token); err != nil {
				return configErr(fmt.Errorf("saving location: %w", err))
			}
			if flags.asJSON {
				out := map[string]any{"location_id": id, "saved": true}
				if name != "" {
					out["name"] = name
				}
				return printJSONFiltered(cmd.OutOrStdout(), out, flags)
			}
			if name != "" {
				fmt.Fprintf(cmd.OutOrStdout(), "Saved location %s as %q\n", id, name)
			} else {
				fmt.Fprintf(cmd.OutOrStdout(), "Saved location %s\n", id)
			}
			fmt.Fprintf(cmd.OutOrStdout(), "Switch to it with: scalify-cli location use %s\n", args[0])
			return nil
		},
	}
	cmd.Flags().StringVar(&token, "token", "", "PIT for this location")
	cmd.Flags().StringVar(&name, "name", "", "friendly name for this location")
	return cmd
}

func newLocationListCmd(flags *rootFlags) *cobra.Command {
	return &cobra.Command{
		Use:     "list",
		Short:   "List all saved locations",
		Example: "  scalify-cli location list",
		RunE: func(cmd *cobra.Command, args []string) error {
			cfg, err := config.Load(flags.configPath)
			if err != nil {
				return configErr(err)
			}
			type entry struct {
				ID       string `json:"id"`
				Name     string `json:"name,omitempty"`
				Active   bool   `json:"active"`
				HasToken bool   `json:"has_token"`
			}
			ids := make([]string, 0, len(cfg.LocationTokens))
			for id := range cfg.LocationTokens {
				ids = append(ids, id)
			}
			sort.Strings(ids)

			if flags.asJSON {
				entries := make([]entry, 0, len(ids))
				for _, id := range ids {
					entries = append(entries, entry{
						ID:       id,
						Name:     cfg.LocationNames[id],
						Active:   id == cfg.LocationID,
						HasToken: true,
					})
				}
				return printJSONFiltered(cmd.OutOrStdout(), entries, flags)
			}
			if len(ids) == 0 {
				fmt.Fprintln(cmd.OutOrStdout(), "No saved locations.")
				fmt.Fprintln(cmd.OutOrStdout(), "  scalify-cli location add <id> --token <pit>")
				return nil
			}
			for _, id := range ids {
				marker := "  "
				if id == cfg.LocationID {
					marker = "* "
				}
				if name := cfg.LocationNames[id]; name != "" {
					fmt.Fprintf(cmd.OutOrStdout(), "%s%s  (%s)\n", marker, name, id)
				} else {
					fmt.Fprintf(cmd.OutOrStdout(), "%s%s\n", marker, id)
				}
			}
			return nil
		},
	}
}

func newLocationShowCmd(flags *rootFlags) *cobra.Command {
	return &cobra.Command{
		Use:     "show",
		Short:   "Show the active location",
		Example: "  scalify-cli location show",
		RunE: func(cmd *cobra.Command, args []string) error {
			cfg, err := config.Load(flags.configPath)
			if err != nil {
				return configErr(err)
			}
			id := cfg.LocationID
			if envID := os.Getenv("SCALIFY_LOCATION_ID"); envID != "" {
				id = envID
			}
			name := cfg.LocationNames[id]
			if flags.asJSON {
				out := map[string]any{
					"location_id": id,
					"source":      locationSource(cfg),
				}
				if name != "" {
					out["name"] = name
				}
				return printJSONFiltered(cmd.OutOrStdout(), out, flags)
			}
			if id == "" {
				fmt.Fprintln(cmd.OutOrStdout(), "No active location set.")
				fmt.Fprintln(cmd.OutOrStdout(), "  scalify-cli location add <id> --token <pit>")
				fmt.Fprintln(cmd.OutOrStdout(), "  scalify-cli location use <id>")
				return nil
			}
			if name != "" {
				fmt.Fprintf(cmd.OutOrStdout(), "Location: %s (%s)\n", name, id)
			} else {
				fmt.Fprintf(cmd.OutOrStdout(), "Location: %s\n", id)
			}
			fmt.Fprintf(cmd.OutOrStdout(), "Source:   %s\n", locationSource(cfg))
			return nil
		},
	}
}

func locationSource(cfg *config.Config) string {
	if os.Getenv("SCALIFY_LOCATION_ID") != "" {
		return "env:SCALIFY_LOCATION_ID"
	}
	if cfg.LocationID != "" {
		return "config"
	}
	return "none"
}
