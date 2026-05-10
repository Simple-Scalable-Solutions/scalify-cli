---
name: scalify-cli
description: >
  Use when the user wants to interact with the Scalify Platform via the CLI — managing contacts,
  conversations, calendars, opportunities, invoices, users, locations, webhooks, or any other
  Scalify resource. Trigger whenever the user mentions "scalify-cli", asks to list/get/create/update/
  delete any Scalify resource, wants to run a Scalify API operation, needs to set up auth or switch
  locations, or asks what CLI commands are available. Also trigger when the user asks to automate,
  script, or pipe Scalify data — use --agent mode for those.
---

# Scalify CLI

`scalify-cli` is the command-line interface to the Scalify Platform. It wraps the Scalify API with
structured output, caching, and agent-friendly flags.

## Installation

Before using any command, check if the CLI is installed:

```bash
which scalify-cli
```

If not found, install it with the one-liner (macOS and Linux):

```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
```

This installs the latest release binary to `/usr/local/bin/scalify-cli`. After install, open a new
shell or run `hash -r` to pick up the new binary, then verify:

```bash
scalify-cli --version
```

## Auth Setup

Two methods (env var wins over config file):

```bash
# Option A: env var (temporary, per-session)
export SCALIFY_TOKEN=your-token-here

# Option B: persist to config (recommended)
scalify-cli auth set-token YOUR_TOKEN_HERE

# Verify
scalify-cli auth status
scalify-cli doctor
```

Config lives at `~/.config/scalify-pp-cli/config.toml`.
Override with `SCALIFY_CONFIG` env var or `--config <path>`.

## Location (Sub-account) Management

Agency-level tokens work for agency endpoints. Location-scoped endpoints need a per-location PIT:

```bash
# Save a location token (without switching)
scalify-cli location add <location-id> --token pit-abc123

# Switch to a location (uses saved token)
scalify-cli location use <location-id>

# Save + switch in one step
scalify-cli location use <location-id> --token pit-abc123

# See all saved locations (* = active)
scalify-cli location list

# Show active location
scalify-cli location show
```

Override for one command: `SCALIFY_LOCATION_ID=<id> scalify-cli contacts list-contacts`

## Resource Groups

Each group has subcommands like `list-*`, `get-*`, `create-*`, `update-*`, `delete-*`:

| Group | What it covers |
|---|---|
| `contacts` | CRM contacts, notes, tasks, tags, appointments, workflows |
| `conversations` | Conversations, messages |
| `opportunities` | Pipeline opportunities |
| `calendars` | Calendars, appointments, slots |
| `locations` | Location/sub-account records and custom fields |
| `users` | User accounts |
| `invoices` | Invoices, estimates |
| `payments` | Transactions, subscriptions, orders |
| `businesses` | Business records |
| `blogs` | Blog posts and categories |
| `forms` | Form definitions and submissions |
| `surveys` | Survey definitions |
| `funnels` | Funnels and pages |
| `medias` | Media library files |
| `objects` | Custom objects and records |
| `webhooks` | Webhook subscriptions |
| `social-media-posting` | Scheduled social posts |
| `analytics` | Analytics data |
| `documents` | Documents |

### Discover subcommands

```bash
scalify-cli contacts --help
scalify-cli contacts list-contacts --help
```

## Output Flags (available on every command)

| Flag | Effect |
|---|---|
| `--json` | JSON output |
| `--compact` | Key fields only (id, name, status, timestamps) — fewer tokens |
| `--csv` | CSV output |
| `--plain` | Tab-separated text |
| `--quiet` | Bare output, one value per line |
| `--select id,name,email` | Pick specific fields |
| `--agent` | Sets `--json --compact --no-input --no-color --yes` — use for scripting |

## Scripting / Agent Patterns

Always use `--agent` when piping or scripting — it disables prompts and sets structured output:

```bash
# List contacts as compact JSON
scalify-cli contacts list-contacts --agent

# Get a specific contact
scalify-cli contacts get-contacts <contact-id> --agent

# Create a contact
scalify-cli contacts create-contacts --agent \
  --firstName "Jane" --lastName "Doe" --email "jane@example.com"

# Pipe IDs into another command
scalify-cli contacts list-contacts --agent --select id \
  | jq -r '.[].id' \
  | xargs -I{} scalify-cli contacts get-contacts {} --agent
```

## Other Useful Flags

| Flag | Effect |
|---|---|
| `--dry-run` | Print the request without sending it |
| `--no-cache` | Bypass local response cache |
| `--data-source live\|local\|auto` | Force live API, cached data, or auto |
| `--yes` | Skip confirmation prompts |
| `--idempotent` | Treat duplicate creates as success |
| `--ignore-missing` | Treat missing deletes as success |
| `--deliver file:<path>` | Write output to a file instead of stdout |
| `--deliver webhook:<url>` | POST output to a webhook |
| `--rate-limit <n>` | Max requests per second |
| `--timeout <duration>` | Request timeout (default 30s) |

## System Commands

```bash
scalify-cli doctor              # Check auth + connectivity + cache health
scalify-cli sync                # Pull data into local SQLite cache
scalify-cli search <query>      # Full-text search over cached data
scalify-cli export              # Export data
scalify-cli tail                # Stream live events
scalify-cli which <command>     # Show which binary will run
```

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 2 | Usage / bad flags |
| 3 | Not found |
| 4 | Auth error |
| 5 | API error |
| 7 | Rate limited |

## Common Workflows

**Check everything is working:**
```bash
scalify-cli doctor
```

**Find a contact:**
```bash
scalify-cli search "jane doe" --agent
scalify-cli contacts list-contacts --agent --select id,name,email
```

**Switch locations for location-scoped work:**
```bash
scalify-cli location add <loc-id> --token <pit>
scalify-cli location use <loc-id>
scalify-cli contacts list-contacts --agent   # now scoped to that location
```

**Troubleshoot a 401:**
- Agency PIT → works for agency-level endpoints, not location-scoped ones
- Location PIT → required for contacts, conversations, etc.
- Run `scalify-cli doctor` and `scalify-cli auth status` to check what's configured
