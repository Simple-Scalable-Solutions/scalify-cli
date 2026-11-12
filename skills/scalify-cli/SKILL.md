---
name: scalify-cli
description: >
  Use when the user wants to interact with the Scalify Platform via the CLI — managing contacts,
  conversations, calendars, opportunities, invoices, users, locations, workflows, emails, social posts, or any other
  Scalify resource. Trigger whenever the user mentions "scalify-cli", asks to list/get/create/update/
  delete any Scalify resource, wants to run a Scalify API operation, needs to set up auth or switch
  locations, or asks what CLI commands are available. Also trigger when the user asks to automate,
  script, or pipe Scalify data — use --agent mode for those.
---

# Scalify CLI

`scalify-cli` is the command-line interface to the Scalify Platform. It wraps the Scalify API with
structured output, caching, and agent-friendly flags.

**Nothing gets deleted unless the user asked for that deletion.** This covers workflows, steps,
triggers, emails, blocks, snapshots, items in a snapshot, contacts and any other CRM record. A
general request ("tidy this up", "update the snapshot", "add these") is not an ask to delete.
Before every save, read the preview: if it deletes, removes, replaces or overwrites anything the
user didn't name, stop, tell them exactly what would go, and wait for a yes for those items.

## Installation

Before using any command, check if the CLI is installed:

```bash
which scalify-cli
```

If not found, install it:

macOS / Linux:
```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.ps1 | iex
```

This installs the latest release binary to `/usr/local/bin/scalify-cli`. After install, open a new
shell or run `hash -r` to pick up the new binary, then verify:

```bash
scalify-cli --version
```

## Version Check (run at session start)

At the start of every session, check for updates:

```bash
scalify-cli doctor
```

If the output contains `update_available`, a newer version is available. Warn the user and offer to upgrade both the CLI and the skill:

macOS / Linux:
```bash
# Upgrade CLI binary
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
# Upgrade skill
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.sh | bash
```

Windows (PowerShell):
```powershell
# Upgrade CLI binary
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.ps1 | iex
# Upgrade skill
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.ps1 | iex
```

After upgrading the skill, start a new Claude Code session for the changes to take effect.

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

Override for one command: `SCALIFY_LOCATION_ID=<id> scalify-cli contacts search --agent`

Commands with a `--location-id` flag fill it from the active location when you leave it out. Commands
that take the location as an argument (`scalify-cli emails list-templates <locationId>`) still need it
typed.

## Resource Groups

Subcommands follow the resource: `list`, `get`, `search`, `create`, `update`, `delete`, with nested
groups for sub-resources (`contacts notes list`, `locations custom-values get`). `--help` on any group
lists them.

| Group | What it covers |
|---|---|
| `contacts` | Search, count, lookup by email/phone, duplicates, bulk tags; notes, tasks, tags, appointments, workflow enrolment |
| `conversations` | Search (with filters), messages, email messages, call recordings and transcripts, export |
| `opportunities` | Search, pipelines, lost reasons, status |
| `calendars` | Calendars, groups, events, appointments and their notes, blocked and free slots, notifications |
| `locations` | Sub-account record, custom fields and values, tags, task search, SMS/email templates, timezones, features |
| `custom-fields` | Field and folder definitions on custom objects (create, update, delete) |
| `objects` | Custom object schemas; `objects records` get/search/create/update/delete |
| `associations` | Associations and a record's relations |
| `users` | Search, filter by email, get |
| `workflows` | List; definition, logs, status, search, create, delete (limited availability, see below) |
| `emails` | Email templates (list, get, create, update, delete, import) and campaigns with stats |
| `social-media-posting` | Statistics (root command), `posts`, `accounts`, `categories`, `tags` |
| `invoices` | Invoices, estimates, templates, schedules, settings, record payment, send, void |
| `payments` | Orders (notes, fulfilments), transactions, subscriptions, coupons |
| `products` | Products, prices, inventory, collections |
| `funnels` | Funnels, pages, page count, URL redirects |
| `blogs` | Blogs, posts, authors, categories, slug check |
| `forms`, `surveys` | Definitions and submissions |
| `businesses`, `medias`, `campaigns`, `links`, `courses`, `proposals`, `notes` | As named |

### Discover subcommands

```bash
scalify-cli contacts --help
scalify-cli contacts search --help
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
# Search contacts (page-limit is required, max 500)
scalify-cli contacts search --page-limit 50 --query "jane" --agent

# Get a specific contact
scalify-cli contacts get <contact-id> --agent

# Create a contact
scalify-cli contacts create --agent \
  --first-name "Jane" --last-name "Doe" --email "jane@example.com"

# Complex bodies (filters, nested objects): pipe JSON with --stdin
echo '{"locationId":"<loc>","pageLimit":20,"filters":[{"field":"tags","operator":"eq","value":"vip"}]}' \
  | scalify-cli contacts search --stdin --agent
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
scalify-cli sync                # Copy the active location's records (contacts, conversations, opportunities,
                                #   workflows, invoices and more; --resources to pick) into a local cache
scalify-cli search <query>      # Full-text search over the synced copy (--type contacts to narrow)
scalify-cli analytics --type contacts --group-by type   # Counts over the synced copy
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

## Full API Reference

`scalify-cli` wraps GHL's public API (base `services.leadconnectorhq.com`). **v3 is the current API
version for every service**: send `Version: v3` on every request. Older dated versions (e.g.
`2021-07-28`) still answer most calls, but some endpoints were removed in v3 (e.g.
`/oauth/locationToken`, now `/oauth/location-token`), so go by the v3 docs. For anything not
covered by a `--help` lookup — exact field shapes, auth scopes, a resource this CLI doesn't wrap yet —
check the official docs. **Read them as text from the live index:
https://marketplace.gohighlevel.com/docs/llms/v3/llms.txt** (each service links a compact `.md` file,
e.g. `.../llms/v3/social-planner.md`, and each endpoint its own `.md` page). The site
https://marketplace.gohighlevel.com/docs/ is a JS app that doesn't fetch as text, and the GitHub repo
`GoHighLevel/highlevel-api-docs` is stale (not updated since Aug 2025): don't treat either as the
source of truth for request fields. Example of what the stale copy missed: the social statistics
endpoint takes a date range (`currentRange`), which the old spec didn't list. Top-level: **OAuth 2.0**
(scopes, authorization, webhook auth) and **APIs** (40+ resource groups: Contacts, Conversations,
Calendars, Opportunities, Payments, Workflows, etc.), plus **Webhook Events** and **Custom JS**. The
old v1 API (`rest.gohighlevel.com`) is gone.

**Known gap, confirmed against these docs**: there is no endpoint that lists a location's connected
third-party integrations (Google Business Profile, Facebook Page, Stripe, etc.). The closest thing —
Marketplace App Management's `installedLocations` — answers the opposite question (given *your app*,
which locations installed it), not "what's connected to this location." Integration connection status
is UI-only (`Settings → Integrations` in the app); don't keep searching for an API path to it.

**Workflows API is limited availability**: `workflows list` works everywhere, but `workflows
definition`, `logs`, `status`, `search`, `create` and `delete` only work on sub-accounts HighLevel has
enabled; elsewhere they return 403 `WORKFLOW_API_NOT_ENABLED_FOR_LOCATION` (not a token problem). For
those, use the `scalify-workflows` skill (MCP `builder_get_workflow`), which reads the builder through
a logged-in browser profile.

**Social statistics**: `scalify-cli social-media-posting --profile-ids '[...]' --current-range
'{"startDate":"2026-10-01","endDate":"2026-10-31"}'`. Get the IDs from `social-media-posting accounts
get <locationId>` and pass each account's `profileId` (not its `id`, which returns 400 "Invalid
connected account ID").

**Docs vs API** (found in live tests): estimates need `title` and `expiryDate`, though the docs mark them
optional. Notes search `relations` takes `[{"objectKey":"contact","recordId":"<id>"}]`, not a list of IDs.

**Writes**: create/update/delete are tested end to end on a playground sub-account before each release
(`scripts/e2e/crud.py` in the scalify-cli repo). Not covered: workflow create/update/delete (API not enabled
there), funnel redirects, invoice void. `--dry-run` prints the request without sending it.

**When a call's behavior is genuinely murky** (undocumented error, unclear required headers/fields,
auth scope confusion) and `--help` plus the top-level docs above don't resolve it, check
**https://marketplace.gohighlevel.com/docs/Authorization/authorization_doc** — the authorization
reference — before guessing at request shape.

## Common Workflows

**Check everything is working:**
```bash
scalify-cli doctor
```

**Find a contact:**
```bash
scalify-cli contacts search --page-limit 10 --query "jane doe" --agent
scalify-cli contacts lookup-by-email-or-phone --email jane@example.com --agent
```

**Switch locations for location-scoped work:**
```bash
scalify-cli location add <loc-id> --token <pit>
scalify-cli location use <loc-id>
scalify-cli contacts search --page-limit 20 --agent   # now scoped to that location
```

**Troubleshoot a 401:**
- Agency PIT → works for agency-level endpoints, not location-scoped ones
- Location PIT → required for contacts, conversations, etc.
- Run `scalify-cli doctor` and `scalify-cli auth status` to check what's configured
