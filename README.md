# Scalify CLI

Command-line interface to the Scalify Platform. Manage contacts, conversations, calendars,
opportunities, invoices, and more — directly from your terminal or AI agent.

## Install

### CLI

```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
```

Installs the `scalify-cli` binary to `/usr/local/bin`. Supports macOS and Linux.

After install, open a new shell (or run `hash -r`) and verify:

```bash
scalify-cli --version
```

### Claude Code Skill

Install the companion skill so Claude Code understands how to use the CLI on your behalf:

```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.sh | bash
```

Then restart Claude Code (or start a new session). The skill teaches Claude to use `scalify-cli`
commands, handle auth, switch locations, and pipe output — no additional setup needed.

---

## Quick Start

### 1. Set Up Credentials

Get your API token from the Scalify Platform, then save it:

```bash
scalify-cli auth set-token YOUR_TOKEN_HERE
```

Or use an environment variable (takes precedence over the config file):

```bash
export SCALIFY_TOKEN="your-token-here"
```

### 2. Verify Setup

```bash
scalify-cli doctor
```

Checks configuration, credentials, and API connectivity.

### 3. Try a Command

```bash
scalify-cli contacts list-contacts --compact
```

---

## Location (Sub-account) Management

Agency-level tokens work for agency endpoints. Location-scoped endpoints (contacts, conversations,
etc.) require a per-location Private Integration Token (PIT):

```bash
# Save a location and its token
scalify-cli location add <location-id> --token pit-abc123

# Switch to that location
scalify-cli location use <location-id>

# Save + switch in one step
scalify-cli location use <location-id> --token pit-abc123

# List saved locations (* = active)
scalify-cli location list

# Show the currently active location
scalify-cli location show
```

Override for a single command without switching:

```bash
SCALIFY_LOCATION_ID=<id> scalify-cli contacts list-contacts
```

---

## Commands

Run `scalify-cli <group> --help` to see all subcommands for a group.

### analytics
- `scalify-cli analytics` — analytics data

### blogs
- `scalify-cli blogs get-posts` — GET /blogs/{id}/posts/{id}
- `scalify-cli blogs list-authors` — GET /blogs/authors
- `scalify-cli blogs list-categories` — GET /blogs/categories
- `scalify-cli blogs list-posts` — GET /blogs/posts

### businesses
- `scalify-cli businesses create-businesses` — POST /businesses
- `scalify-cli businesses delete-businesses` — DELETE /businesses/{id}
- `scalify-cli businesses get-businesses` — GET /businesses/{id}
- `scalify-cli businesses list-businesses` — GET /businesses
- `scalify-cli businesses update-businesses` — PUT /businesses/{id}

### calendars
- `scalify-cli calendars create-appointments` — POST /calendars/events/appointments
- `scalify-cli calendars create-calendars` — POST /calendars
- `scalify-cli calendars delete-calendars` — DELETE /calendars/{id}
- `scalify-cli calendars get-calendars` — GET /calendars/{id}
- `scalify-cli calendars get-free-slots` — GET /calendars/{id}/free-slots
- `scalify-cli calendars list-calendars` — GET /calendars
- `scalify-cli calendars list-events` — GET /calendars/events
- `scalify-cli calendars update-calendars` — PUT /calendars/{id}

### contacts
- `scalify-cli contacts create-contacts` — POST /contacts
- `scalify-cli contacts create-notes` — POST /contacts/{id}/notes
- `scalify-cli contacts create-tags` — POST /contacts/{id}/tags
- `scalify-cli contacts create-tasks` — POST /contacts/{id}/tasks
- `scalify-cli contacts create-upsert` — POST /contacts/upsert
- `scalify-cli contacts create-workflow` — POST /contacts/{id}/workflow/{id}
- `scalify-cli contacts delete-contacts` — DELETE /contacts/{id}
- `scalify-cli contacts delete-tags` — DELETE /contacts/{id}/tags
- `scalify-cli contacts get-appointments` — GET /contacts/{id}/appointments
- `scalify-cli contacts get-contacts` — GET /contacts/{id}
- `scalify-cli contacts get-notes` — GET /contacts/{id}/notes
- `scalify-cli contacts get-tasks` — GET /contacts/{id}/tasks
- `scalify-cli contacts list-contacts` — GET /contacts
- `scalify-cli contacts list-search` — GET /contacts/search
- `scalify-cli contacts update-contacts` — PUT /contacts/{id}

### conversations
- `scalify-cli conversations create-conversations` — POST /conversations
- `scalify-cli conversations create-inbound` — POST /conversations/messages/inbound
- `scalify-cli conversations create-messages` — POST /conversations/messages
- `scalify-cli conversations get-conversations` — GET /conversations/{id}
- `scalify-cli conversations get-messages` — GET /conversations/{id}/messages
- `scalify-cli conversations list-search` — GET /conversations/search
- `scalify-cli conversations update-status` — PUT /conversations/messages/{id}/status

### documents
- `scalify-cli documents create-send` — POST /documents/{id}/send
- `scalify-cli documents delete-documents` — DELETE /documents/{id}
- `scalify-cli documents get-documents` — GET /documents/{id}
- `scalify-cli documents list-documents` — GET /documents

### forms
- `scalify-cli forms list-forms` — GET /forms
- `scalify-cli forms list-submissions` — GET /forms/submissions

### funnels
- `scalify-cli funnels list-funnels` — GET /funnels
- `scalify-cli funnels list-list` — GET /funnels/funnel/list
- `scalify-cli funnels list-page` — GET /funnels/page

### invoices
- `scalify-cli invoices create-estimate` — POST /invoices/estimate
- `scalify-cli invoices create-invoices` — POST /invoices
- `scalify-cli invoices create-record-payment` — POST /invoices/{id}/record-payment
- `scalify-cli invoices create-send` — POST /invoices/{id}/send
- `scalify-cli invoices create-void` — POST /invoices/{id}/void
- `scalify-cli invoices delete-estimate` — DELETE /invoices/estimate/{id}
- `scalify-cli invoices delete-invoices` — DELETE /invoices/{id}
- `scalify-cli invoices get-estimate` — GET /invoices/estimate/{id}
- `scalify-cli invoices get-invoices` — GET /invoices/{id}
- `scalify-cli invoices list-estimate` — GET /invoices/estimate
- `scalify-cli invoices list-invoices` — GET /invoices
- `scalify-cli invoices update-estimate` — PUT /invoices/estimate/{id}
- `scalify-cli invoices update-invoices` — PUT /invoices/{id}

### locations
- `scalify-cli locations create-customFields` — POST /locations/{id}/customFields
- `scalify-cli locations create-customValues` — POST /locations/{id}/customValues
- `scalify-cli locations create-tags` — POST /locations/{id}/tags
- `scalify-cli locations delete-customFields` — DELETE /locations/{id}/customFields/{id}
- `scalify-cli locations delete-customValues` — DELETE /locations/{id}/customValues/{id}
- `scalify-cli locations delete-tags` — DELETE /locations/{id}/tags/{id}
- `scalify-cli locations get-customFields` — GET /locations/{id}/customFields
- `scalify-cli locations get-customValues` — GET /locations/{id}/customValues
- `scalify-cli locations get-locations` — GET /locations/{id}
- `scalify-cli locations get-tags` — GET /locations/{id}/tags
- `scalify-cli locations list-locations` — GET /locations
- `scalify-cli locations list-search` — GET /locations/search
- `scalify-cli locations update-customFields` — PUT /locations/{id}/customFields/{id}
- `scalify-cli locations update-customValues` — PUT /locations/{id}/customValues/{id}
- `scalify-cli locations update-locations` — PUT /locations/{id}
- `scalify-cli locations update-tags` — PUT /locations/{id}/tags/{id}

### medias
- `scalify-cli medias delete-medias` — DELETE /medias/{id}
- `scalify-cli medias list-files` — GET /medias/files

### objects
- `scalify-cli objects create-records` — POST /objects/{id}/records
- `scalify-cli objects delete-records` — DELETE /objects/{id}/records/{id}
- `scalify-cli objects get-objects` — GET /objects/{id}
- `scalify-cli objects get-records` — GET /objects/{id}/records
- `scalify-cli objects list-objects` — GET /objects
- `scalify-cli objects update-records` — PUT /objects/{id}/records/{id}

### opportunities
- `scalify-cli opportunities create-opportunities` — POST /opportunities
- `scalify-cli opportunities delete-opportunities` — DELETE /opportunities/{id}
- `scalify-cli opportunities get-opportunities` — GET /opportunities/{id}
- `scalify-cli opportunities list-pipelines` — GET /opportunities/pipelines
- `scalify-cli opportunities list-search` — GET /opportunities/search
- `scalify-cli opportunities update-opportunities` — PUT /opportunities/{id}

### payments
- `scalify-cli payments create-coupons` — POST /payments/coupons
- `scalify-cli payments delete-coupons` — DELETE /payments/coupons/{id}
- `scalify-cli payments get-coupons` — GET /payments/coupons/{id}
- `scalify-cli payments get-orders` — GET /payments/orders/{id}
- `scalify-cli payments list-coupons` — GET /payments/coupons
- `scalify-cli payments list-orders` — GET /payments/orders
- `scalify-cli payments list-subscriptions` — GET /payments/subscriptions
- `scalify-cli payments list-transactions` — GET /payments/transactions
- `scalify-cli payments update-coupons` — PUT /payments/coupons/{id}

### social-media-posting
- `scalify-cli social-media-posting create-social-media-posting` — POST /social-media-posting
- `scalify-cli social-media-posting delete-social-media-posting` — DELETE /social-media-posting/{id}
- `scalify-cli social-media-posting get-social-media-posting` — GET /social-media-posting/{id}
- `scalify-cli social-media-posting list-social-media-posting` — GET /social-media-posting

### surveys
- `scalify-cli surveys list-submissions` — GET /surveys/submissions
- `scalify-cli surveys list-surveys` — GET /surveys

### users
- `scalify-cli users get-users` — GET /users/{id}
- `scalify-cli users list-users` — GET /users

### webhooks
- `scalify-cli webhooks create-webhooks` — POST /webhooks
- `scalify-cli webhooks delete-webhooks` — DELETE /webhooks/{id}
- `scalify-cli webhooks get-webhooks` — GET /webhooks/{id}
- `scalify-cli webhooks list-webhooks` — GET /webhooks
- `scalify-cli webhooks update-webhooks` — PUT /webhooks/{id}

---

## Output Formats

```bash
# Human-readable table (default in terminal, JSON when piped)
scalify-cli contacts list-contacts

# JSON
scalify-cli contacts list-contacts --json

# Compact JSON — key fields only (id, name, status, timestamps)
scalify-cli contacts list-contacts --compact

# Filter to specific fields
scalify-cli contacts list-contacts --json --select id,firstName,email

# CSV
scalify-cli contacts list-contacts --csv

# Dry run — print the request without sending
scalify-cli contacts list-contacts --dry-run

# Agent mode — JSON + compact + no prompts in one flag
scalify-cli contacts list-contacts --agent
```

---

## Agent / Scripting Usage

`scalify-cli` is designed to be driven by AI agents and scripts:

- **`--agent`** — sets `--json --compact --no-input --no-color --yes` in one flag
- **`--select id,name`** — return only the fields you need
- **`--dry-run`** — preview requests without side effects
- **`--idempotent`** — makes create retries safe (treats duplicates as success)
- **`--ignore-missing`** — makes delete retries safe (treats not-found as success)
- **`--yes`** — skip confirmation prompts
- **`--deliver file:<path>`** — write output to a file instead of stdout
- **`--deliver webhook:<url>`** — POST output to a webhook
- **`--data-source live|local|auto`** — force live API, cached SQLite, or auto

Exit codes: `0` success · `2` usage error · `3` not found · `4` auth error · `5` API error · `7` rate limited

Example — search contacts by query:

```bash
scalify-cli contacts list-search --params "query=jane doe" --agent
```

Example — fetch all contact IDs and look each one up:

```bash
scalify-cli contacts list-contacts --agent --select id \
  | jq -r '.[].id' \
  | xargs -I{} scalify-cli contacts get-contacts {} --agent
```

---

## Use with Claude Code

Install the skill so Claude understands `scalify-cli` commands and can use them autonomously:

```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.sh | bash
```

Restart Claude Code after install. The skill covers auth setup, location switching, all resource
groups, output flags, and common workflows — Claude will invoke the CLI directly rather than
asking you to run commands manually.

---

## Use as an MCP Server (Claude Code or Claude Desktop)

The CLI ships a companion MCP server binary (`scalify-pp-mcp`) that exposes every command as an
agent tool. Register it in Claude Code:

```bash
claude mcp add scalify scalify-pp-mcp -e SCALIFY_TOKEN=<your-token>
```

Or add it to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "scalify": {
      "command": "scalify-pp-mcp",
      "env": {
        "SCALIFY_TOKEN": "<your-key>"
      }
    }
  }
}
```

---

## Configuration

Config file: `~/.config/scalify-pp-cli/config.toml`

| Environment variable | Description |
|---|---|
| `SCALIFY_TOKEN` | API token (takes precedence over config file) |
| `SCALIFY_LOCATION_ID` | Active location ID (takes precedence over config file) |
| `SCALIFY_CONFIG` | Override config file path |

---

## Troubleshooting

**401 / auth errors (exit code 4)**
- Agency PITs work for agency-level endpoints only — location-scoped endpoints (contacts, conversations, etc.) need a location PIT
- Run `scalify-cli doctor` and `scalify-cli auth status` to check what's configured
- Set a location token: `scalify-cli location add <id> --token <pit>`

**Not found errors (exit code 3)**
- Check the resource ID is correct
- Run the `list` variant of the command to see available items

**HTTP transport**
This CLI uses Chrome-compatible HTTP transport for browser-facing endpoints and does not require a
resident browser process for normal API calls.

---

Generated by [CLI Printing Press](https://github.com/mvanhorn/cli-printing-press)
