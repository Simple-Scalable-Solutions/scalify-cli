# Scalify CLI

Scalify Platform API

## Install

The recommended path installs both the `scalify-pp-cli` binary and the `pp-scalify` agent skill in one shot:

```bash
npx -y @mvanhorn/printing-press install scalify
```

For CLI only (no skill):

```bash
npx -y @mvanhorn/printing-press install scalify --cli-only
```


### Without Node

The generated install path is category-agnostic until this CLI is published. If `npx` is not available before publish, install Node or use the category-specific Go fallback from the public-library entry after publish.

### Pre-built binary

Download a pre-built binary for your platform from the [latest release](https://github.com/mvanhorn/printing-press-library/releases/tag/scalify-current). On macOS, clear the Gatekeeper quarantine: `xattr -d com.apple.quarantine <binary>`. On Unix, mark it executable: `chmod +x <binary>`.

<!-- pp-hermes-install-anchor -->
## Install for Hermes

From the Hermes CLI:

```bash
hermes skills install mvanhorn/printing-press-library/cli-skills/pp-scalify --force
```

Inside a Hermes chat session:

```bash
/skills install mvanhorn/printing-press-library/cli-skills/pp-scalify --force
```

## Install for OpenClaw

Tell your OpenClaw agent (copy this):

```
Install the pp-scalify skill from https://github.com/mvanhorn/printing-press-library/tree/main/cli-skills/pp-scalify. The skill defines how its required CLI can be installed.
```

## Quick Start

### 1. Install

See [Install](#install) above.

### 2. Set Up Credentials

Get your access token from your API provider's developer portal, then store it:

```bash
scalify-pp-cli auth set-token YOUR_TOKEN_HERE
```

Or set it via environment variable:

```bash
export SCALIFY_TOKEN="your-token-here"
```

### 3. Verify Setup

```bash
scalify-pp-cli doctor
```

This checks your configuration and credentials.

### 4. Try Your First Command

```bash
scalify-pp-cli blogs get_posts mock-value
```

## Usage

Run `scalify-pp-cli --help` for the full command reference and flag list.

## Commands

### blogs

Operations on posts

- **`scalify-pp-cli blogs get_posts`** - GET /blogs/{id}/posts/{id}
- **`scalify-pp-cli blogs list_authors`** - GET /blogs/authors
- **`scalify-pp-cli blogs list_categories`** - GET /blogs/categories
- **`scalify-pp-cli blogs list_posts`** - GET /blogs/posts
- **`scalify-pp-cli blogs list_url_slug_exists`** - GET /blogs/posts/url-slug-exists

### businesses

Operations on businesses

- **`scalify-pp-cli businesses create_businesses`** - POST /businesses
- **`scalify-pp-cli businesses delete_businesses`** - DELETE /businesses/{id}
- **`scalify-pp-cli businesses get_businesses`** - GET /businesses/{id}
- **`scalify-pp-cli businesses list_businesses`** - GET /businesses
- **`scalify-pp-cli businesses update_businesses`** - PUT /businesses/{id}

### calendars

Operations on calendars

- **`scalify-pp-cli calendars create_appointments`** - POST /calendars/events/appointments
- **`scalify-pp-cli calendars create_calendars`** - POST /calendars
- **`scalify-pp-cli calendars delete_calendars`** - DELETE /calendars/{id}
- **`scalify-pp-cli calendars get_calendars`** - GET /calendars/{id}
- **`scalify-pp-cli calendars get_free_slots`** - GET /calendars/{id}/free-slots
- **`scalify-pp-cli calendars list_calendars`** - GET /calendars
- **`scalify-pp-cli calendars list_events`** - GET /calendars/events
- **`scalify-pp-cli calendars update_calendars`** - PUT /calendars/{id}

### campaigns

Operations on campaigns

- **`scalify-pp-cli campaigns list_campaigns`** - GET /campaigns

### contacts

Operations on contacts

- **`scalify-pp-cli contacts create_contacts`** - POST /contacts
- **`scalify-pp-cli contacts create_notes`** - POST /contacts/{id}/notes
- **`scalify-pp-cli contacts create_tags`** - POST /contacts/{id}/tags
- **`scalify-pp-cli contacts create_tasks`** - POST /contacts/{id}/tasks
- **`scalify-pp-cli contacts create_upsert`** - POST /contacts/upsert
- **`scalify-pp-cli contacts create_workflow`** - POST /contacts/{id}/workflow/{id}
- **`scalify-pp-cli contacts delete_contacts`** - DELETE /contacts/{id}
- **`scalify-pp-cli contacts delete_tags`** - DELETE /contacts/{id}/tags
- **`scalify-pp-cli contacts get_appointments`** - GET /contacts/{id}/appointments
- **`scalify-pp-cli contacts get_contacts`** - GET /contacts/{id}
- **`scalify-pp-cli contacts get_notes`** - GET /contacts/{id}/notes
- **`scalify-pp-cli contacts get_tasks`** - GET /contacts/{id}/tasks
- **`scalify-pp-cli contacts list_contacts`** - GET /contacts
- **`scalify-pp-cli contacts update_contacts`** - PUT /contacts/{id}

### conversations

Operations on search

- **`scalify-pp-cli conversations create_conversations`** - POST /conversations
- **`scalify-pp-cli conversations create_inbound`** - POST /conversations/messages/inbound
- **`scalify-pp-cli conversations create_messages`** - POST /conversations/messages
- **`scalify-pp-cli conversations get_conversations`** - GET /conversations/{id}
- **`scalify-pp-cli conversations get_messages`** - GET /conversations/{id}/messages
- **`scalify-pp-cli conversations get_messages_2`** - GET /conversations/messages/{id}
- **`scalify-pp-cli conversations list_search`** - GET /conversations/search
- **`scalify-pp-cli conversations update_status`** - PUT /conversations/messages/{id}/status

### courses

Operations on courses

- **`scalify-pp-cli courses list_courses`** - GET /courses

### documents

Operations on documents

- **`scalify-pp-cli documents create_send`** - POST /documents/{id}/send
- **`scalify-pp-cli documents delete_documents`** - DELETE /documents/{id}
- **`scalify-pp-cli documents get_documents`** - GET /documents/{id}
- **`scalify-pp-cli documents list_documents`** - GET /documents

### emails

Operations on emails

- **`scalify-pp-cli emails list_emails`** - GET /emails

### forms

Operations on forms

- **`scalify-pp-cli forms list_forms`** - GET /forms
- **`scalify-pp-cli forms list_submissions`** - GET /forms/submissions

### funnels

Operations on list

- **`scalify-pp-cli funnels list_funnels`** - GET /funnels
- **`scalify-pp-cli funnels list_list`** - GET /funnels/funnel/list
- **`scalify-pp-cli funnels list_page`** - GET /funnels/page

### invoices

Operations on invoices

- **`scalify-pp-cli invoices create_estimate`** - POST /invoices/estimate
- **`scalify-pp-cli invoices create_invoices`** - POST /invoices
- **`scalify-pp-cli invoices create_record_payment`** - POST /invoices/{id}/record-payment
- **`scalify-pp-cli invoices create_send`** - POST /invoices/{id}/send
- **`scalify-pp-cli invoices create_send_2`** - POST /invoices/estimate/{id}/send
- **`scalify-pp-cli invoices create_void`** - POST /invoices/{id}/void
- **`scalify-pp-cli invoices delete_estimate`** - DELETE /invoices/estimate/{id}
- **`scalify-pp-cli invoices delete_invoices`** - DELETE /invoices/{id}
- **`scalify-pp-cli invoices get_estimate`** - GET /invoices/estimate/{id}
- **`scalify-pp-cli invoices get_invoices`** - GET /invoices/{id}
- **`scalify-pp-cli invoices list_estimate`** - GET /invoices/estimate
- **`scalify-pp-cli invoices list_invoices`** - GET /invoices
- **`scalify-pp-cli invoices update_estimate`** - PUT /invoices/estimate/{id}
- **`scalify-pp-cli invoices update_invoices`** - PUT /invoices/{id}

### links

Operations on links

- **`scalify-pp-cli links list_links`** - GET /links

### locations

Operations on locations

- **`scalify-pp-cli locations create_customFields`** - POST /locations/{id}/customFields
- **`scalify-pp-cli locations create_customValues`** - POST /locations/{id}/customValues
- **`scalify-pp-cli locations create_tags`** - POST /locations/{id}/tags
- **`scalify-pp-cli locations delete_customFields`** - DELETE /locations/{id}/customFields/{id}
- **`scalify-pp-cli locations delete_customValues`** - DELETE /locations/{id}/customValues/{id}
- **`scalify-pp-cli locations delete_tags`** - DELETE /locations/{id}/tags/{id}
- **`scalify-pp-cli locations get_customFields`** - GET /locations/{id}/customFields
- **`scalify-pp-cli locations get_customValues`** - GET /locations/{id}/customValues
- **`scalify-pp-cli locations get_locations`** - GET /locations/{id}
- **`scalify-pp-cli locations get_tags`** - GET /locations/{id}/tags
- **`scalify-pp-cli locations list_locations`** - GET /locations
- **`scalify-pp-cli locations list_search`** - GET /locations/search
- **`scalify-pp-cli locations update_customFields`** - PUT /locations/{id}/customFields/{id}
- **`scalify-pp-cli locations update_customValues`** - PUT /locations/{id}/customValues/{id}
- **`scalify-pp-cli locations update_locations`** - PUT /locations/{id}
- **`scalify-pp-cli locations update_tags`** - PUT /locations/{id}/tags/{id}

### medias

Operations on files

- **`scalify-pp-cli medias delete_medias`** - DELETE /medias/{id}
- **`scalify-pp-cli medias list_files`** - GET /medias/files

### objects

Operations on objects

- **`scalify-pp-cli objects create_records`** - POST /objects/{id}/records
- **`scalify-pp-cli objects delete_records`** - DELETE /objects/{id}/records/{id}
- **`scalify-pp-cli objects get_objects`** - GET /objects/{id}
- **`scalify-pp-cli objects get_records`** - GET /objects/{id}/records
- **`scalify-pp-cli objects get_records_2`** - GET /objects/{id}/records/{id}
- **`scalify-pp-cli objects list_objects`** - GET /objects
- **`scalify-pp-cli objects update_records`** - PUT /objects/{id}/records/{id}

### opportunities

Operations on search

- **`scalify-pp-cli opportunities create_opportunities`** - POST /opportunities
- **`scalify-pp-cli opportunities delete_opportunities`** - DELETE /opportunities/{id}
- **`scalify-pp-cli opportunities get_opportunities`** - GET /opportunities/{id}
- **`scalify-pp-cli opportunities list_pipelines`** - GET /opportunities/pipelines
- **`scalify-pp-cli opportunities list_search`** - GET /opportunities/search
- **`scalify-pp-cli opportunities update_opportunities`** - PUT /opportunities/{id}

### payments

Operations on orders

- **`scalify-pp-cli payments create_coupons`** - POST /payments/coupons
- **`scalify-pp-cli payments delete_coupons`** - DELETE /payments/coupons/{id}
- **`scalify-pp-cli payments get_coupons`** - GET /payments/coupons/{id}
- **`scalify-pp-cli payments get_orders`** - GET /payments/orders/{id}
- **`scalify-pp-cli payments list_coupons`** - GET /payments/coupons
- **`scalify-pp-cli payments list_orders`** - GET /payments/orders
- **`scalify-pp-cli payments list_subscriptions`** - GET /payments/subscriptions
- **`scalify-pp-cli payments list_transactions`** - GET /payments/transactions
- **`scalify-pp-cli payments update_coupons`** - PUT /payments/coupons/{id}

### social-media-posting

Operations on social-media-posting

- **`scalify-pp-cli social-media-posting create_social_media_posting`** - POST /social-media-posting
- **`scalify-pp-cli social-media-posting delete_social_media_posting`** - DELETE /social-media-posting/{id}
- **`scalify-pp-cli social-media-posting get_social_media_posting`** - GET /social-media-posting/{id}
- **`scalify-pp-cli social-media-posting list_social_media_posting`** - GET /social-media-posting

### surveys

Operations on surveys

- **`scalify-pp-cli surveys list_submissions`** - GET /surveys/submissions
- **`scalify-pp-cli surveys list_surveys`** - GET /surveys

### users

Operations on users

- **`scalify-pp-cli users get_users`** - GET /users/{id}
- **`scalify-pp-cli users list_users`** - GET /users

### webhooks

Operations on webhooks

- **`scalify-pp-cli webhooks create_webhooks`** - POST /webhooks
- **`scalify-pp-cli webhooks delete_webhooks`** - DELETE /webhooks/{id}
- **`scalify-pp-cli webhooks get_webhooks`** - GET /webhooks/{id}
- **`scalify-pp-cli webhooks list_webhooks`** - GET /webhooks
- **`scalify-pp-cli webhooks update_webhooks`** - PUT /webhooks/{id}

### workflows

Operations on workflows

- **`scalify-pp-cli workflows list_workflows`** - GET /workflows


## Output Formats

```bash
# Human-readable table (default in terminal, JSON when piped)
scalify-pp-cli blogs get_posts mock-value

# JSON for scripting and agents
scalify-pp-cli blogs get_posts mock-value --json

# Filter to specific fields
scalify-pp-cli blogs get_posts mock-value --json --select id,name,status

# Dry run — show the request without sending
scalify-pp-cli blogs get_posts mock-value --dry-run

# Agent mode — JSON + compact + no prompts in one flag
scalify-pp-cli blogs get_posts mock-value --agent
```

## Agent Usage

This CLI is designed for AI agent consumption:

- **Non-interactive** - never prompts, every input is a flag
- **Pipeable** - `--json` output to stdout, errors to stderr
- **Filterable** - `--select id,name` returns only fields you need
- **Previewable** - `--dry-run` shows the request without sending
- **Explicit retries** - add `--idempotent` to create retries and `--ignore-missing` to delete retries when a no-op success is acceptable
- **Confirmable** - `--yes` for explicit confirmation of destructive actions
- **Piped input** - write commands can accept structured input when their help lists `--stdin`
- **Offline-friendly** - sync/search commands can use the local SQLite store when available
- **Agent-safe by default** - no colors or formatting unless `--human-friendly` is set

Exit codes: `0` success, `2` usage error, `3` not found, `4` auth error, `5` API error, `7` rate limited, `10` config error.

## Use with Claude Code

Install the focused skill — it auto-installs the CLI on first invocation:

```bash
npx skills add mvanhorn/printing-press-library/cli-skills/pp-scalify -g
```

Then invoke `/pp-scalify <query>` in Claude Code. The skill is the most efficient path — Claude Code drives the CLI directly without an MCP server in the middle.

<details>
<summary>Use as an MCP server in Claude Code (advanced)</summary>

If you'd rather register this CLI as an MCP server in Claude Code, install the MCP binary first:


Install the MCP binary from this CLI's published public-library entry or pre-built release.

Then register it:

```bash
claude mcp add scalify scalify-pp-mcp -e SCALIFY_TOKEN=<your-token>
```

</details>

## Use with Claude Desktop

This CLI ships an [MCPB](https://github.com/modelcontextprotocol/mcpb) bundle — Claude Desktop's standard format for one-click MCP extension installs (no JSON config required).

To install:

1. Download the `.mcpb` for your platform from the [latest release](https://github.com/mvanhorn/printing-press-library/releases/tag/scalify-current).
2. Double-click the `.mcpb` file. Claude Desktop opens and walks you through the install.
3. Fill in `SCALIFY_TOKEN` when Claude Desktop prompts you.

Requires Claude Desktop 1.0.0 or later. Pre-built bundles ship for macOS Apple Silicon (`darwin-arm64`) and Windows (`amd64`, `arm64`); for other platforms, use the manual config below.

<details>
<summary>Manual JSON config (advanced)</summary>

If you can't use the MCPB bundle (older Claude Desktop, unsupported platform), install the MCP binary and configure it manually.


Install the MCP binary from this CLI's published public-library entry or pre-built release.

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

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

</details>

## Health Check

```bash
scalify-pp-cli doctor
```

Verifies configuration, credentials, and connectivity to the API.

## Configuration

Config file: `~/.config/scalify-pp-cli/config.toml`

Static request headers can be configured under `headers`; per-command header overrides take precedence.

Environment variables:

| Name | Kind | Required | Description |
| --- | --- | --- | --- |
| `SCALIFY_TOKEN` | per_call | Yes | Set to your API credential. |

## Troubleshooting
**Authentication errors (exit code 4)**
- Run `scalify-pp-cli doctor` to check credentials
- Verify the environment variable is set: `echo $SCALIFY_TOKEN`
**Not found errors (exit code 3)**
- Check the resource ID is correct
- Run the `list` command to see available items

## HTTP Transport

This CLI uses Chrome-compatible HTTP transport for browser-facing endpoints. It does not require a resident browser process for normal API calls.

---

Generated by [CLI Printing Press](https://github.com/mvanhorn/cli-printing-press)
