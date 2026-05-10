---
name: pp-scalify
description: "Printing Press CLI for Scalify. Scalify Platform API"
author: "scalify"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - scalify-pp-cli
---

# Scalify — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `scalify-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer:
   ```bash
   npx -y @mvanhorn/printing-press install scalify --cli-only
   ```
2. Verify: `scalify-pp-cli --version`
3. Ensure `$GOPATH/bin` (or `$HOME/go/bin`) is on `$PATH`.

If the `npx` install fails before this CLI has a public-library category, install Node or use the category-specific Go fallback after publish.

If `--version` reports "command not found" after install, the install step did not put the binary on `$PATH`. Do not proceed with skill commands until verification succeeds.

Scalify Platform API

## HTTP Transport

This CLI uses Chrome-compatible HTTP transport for browser-facing endpoints. It does not require a resident browser process for normal API calls.

## Command Reference

**blogs** — Operations on posts

- `scalify-pp-cli blogs get_posts` — GET /blogs/{id}/posts/{id}
- `scalify-pp-cli blogs list_authors` — GET /blogs/authors
- `scalify-pp-cli blogs list_categories` — GET /blogs/categories
- `scalify-pp-cli blogs list_posts` — GET /blogs/posts
- `scalify-pp-cli blogs list_url_slug_exists` — GET /blogs/posts/url-slug-exists

**businesses** — Operations on businesses

- `scalify-pp-cli businesses create_businesses` — POST /businesses
- `scalify-pp-cli businesses delete_businesses` — DELETE /businesses/{id}
- `scalify-pp-cli businesses get_businesses` — GET /businesses/{id}
- `scalify-pp-cli businesses list_businesses` — GET /businesses
- `scalify-pp-cli businesses update_businesses` — PUT /businesses/{id}

**calendars** — Operations on calendars

- `scalify-pp-cli calendars create_appointments` — POST /calendars/events/appointments
- `scalify-pp-cli calendars create_calendars` — POST /calendars
- `scalify-pp-cli calendars delete_calendars` — DELETE /calendars/{id}
- `scalify-pp-cli calendars get_calendars` — GET /calendars/{id}
- `scalify-pp-cli calendars get_free_slots` — GET /calendars/{id}/free-slots
- `scalify-pp-cli calendars list_calendars` — GET /calendars
- `scalify-pp-cli calendars list_events` — GET /calendars/events
- `scalify-pp-cli calendars update_calendars` — PUT /calendars/{id}

**campaigns** — Operations on campaigns

- `scalify-pp-cli campaigns` — GET /campaigns

**contacts** — Operations on contacts

- `scalify-pp-cli contacts create_contacts` — POST /contacts
- `scalify-pp-cli contacts create_notes` — POST /contacts/{id}/notes
- `scalify-pp-cli contacts create_tags` — POST /contacts/{id}/tags
- `scalify-pp-cli contacts create_tasks` — POST /contacts/{id}/tasks
- `scalify-pp-cli contacts create_upsert` — POST /contacts/upsert
- `scalify-pp-cli contacts create_workflow` — POST /contacts/{id}/workflow/{id}
- `scalify-pp-cli contacts delete_contacts` — DELETE /contacts/{id}
- `scalify-pp-cli contacts delete_tags` — DELETE /contacts/{id}/tags
- `scalify-pp-cli contacts get_appointments` — GET /contacts/{id}/appointments
- `scalify-pp-cli contacts get_contacts` — GET /contacts/{id}
- `scalify-pp-cli contacts get_notes` — GET /contacts/{id}/notes
- `scalify-pp-cli contacts get_tasks` — GET /contacts/{id}/tasks
- `scalify-pp-cli contacts list_contacts` — GET /contacts
- `scalify-pp-cli contacts update_contacts` — PUT /contacts/{id}

**conversations** — Operations on search

- `scalify-pp-cli conversations create_conversations` — POST /conversations
- `scalify-pp-cli conversations create_inbound` — POST /conversations/messages/inbound
- `scalify-pp-cli conversations create_messages` — POST /conversations/messages
- `scalify-pp-cli conversations get_conversations` — GET /conversations/{id}
- `scalify-pp-cli conversations get_messages` — GET /conversations/{id}/messages
- `scalify-pp-cli conversations get_messages_2` — GET /conversations/messages/{id}
- `scalify-pp-cli conversations list_search` — GET /conversations/search
- `scalify-pp-cli conversations update_status` — PUT /conversations/messages/{id}/status

**courses** — Operations on courses

- `scalify-pp-cli courses` — GET /courses

**documents** — Operations on documents

- `scalify-pp-cli documents create_send` — POST /documents/{id}/send
- `scalify-pp-cli documents delete_documents` — DELETE /documents/{id}
- `scalify-pp-cli documents get_documents` — GET /documents/{id}
- `scalify-pp-cli documents list_documents` — GET /documents

**emails** — Operations on emails

- `scalify-pp-cli emails` — GET /emails

**forms** — Operations on forms

- `scalify-pp-cli forms list_forms` — GET /forms
- `scalify-pp-cli forms list_submissions` — GET /forms/submissions

**funnels** — Operations on list

- `scalify-pp-cli funnels list_funnels` — GET /funnels
- `scalify-pp-cli funnels list_list` — GET /funnels/funnel/list
- `scalify-pp-cli funnels list_page` — GET /funnels/page

**invoices** — Operations on invoices

- `scalify-pp-cli invoices create_estimate` — POST /invoices/estimate
- `scalify-pp-cli invoices create_invoices` — POST /invoices
- `scalify-pp-cli invoices create_record_payment` — POST /invoices/{id}/record-payment
- `scalify-pp-cli invoices create_send` — POST /invoices/{id}/send
- `scalify-pp-cli invoices create_send_2` — POST /invoices/estimate/{id}/send
- `scalify-pp-cli invoices create_void` — POST /invoices/{id}/void
- `scalify-pp-cli invoices delete_estimate` — DELETE /invoices/estimate/{id}
- `scalify-pp-cli invoices delete_invoices` — DELETE /invoices/{id}
- `scalify-pp-cli invoices get_estimate` — GET /invoices/estimate/{id}
- `scalify-pp-cli invoices get_invoices` — GET /invoices/{id}
- `scalify-pp-cli invoices list_estimate` — GET /invoices/estimate
- `scalify-pp-cli invoices list_invoices` — GET /invoices
- `scalify-pp-cli invoices update_estimate` — PUT /invoices/estimate/{id}
- `scalify-pp-cli invoices update_invoices` — PUT /invoices/{id}

**links** — Operations on links

- `scalify-pp-cli links` — GET /links

**locations** — Operations on locations

- `scalify-pp-cli locations create_customFields` — POST /locations/{id}/customFields
- `scalify-pp-cli locations create_customValues` — POST /locations/{id}/customValues
- `scalify-pp-cli locations create_tags` — POST /locations/{id}/tags
- `scalify-pp-cli locations delete_customFields` — DELETE /locations/{id}/customFields/{id}
- `scalify-pp-cli locations delete_customValues` — DELETE /locations/{id}/customValues/{id}
- `scalify-pp-cli locations delete_tags` — DELETE /locations/{id}/tags/{id}
- `scalify-pp-cli locations get_customFields` — GET /locations/{id}/customFields
- `scalify-pp-cli locations get_customValues` — GET /locations/{id}/customValues
- `scalify-pp-cli locations get_locations` — GET /locations/{id}
- `scalify-pp-cli locations get_tags` — GET /locations/{id}/tags
- `scalify-pp-cli locations list_locations` — GET /locations
- `scalify-pp-cli locations list_search` — GET /locations/search
- `scalify-pp-cli locations update_customFields` — PUT /locations/{id}/customFields/{id}
- `scalify-pp-cli locations update_customValues` — PUT /locations/{id}/customValues/{id}
- `scalify-pp-cli locations update_locations` — PUT /locations/{id}
- `scalify-pp-cli locations update_tags` — PUT /locations/{id}/tags/{id}

**medias** — Operations on files

- `scalify-pp-cli medias delete_medias` — DELETE /medias/{id}
- `scalify-pp-cli medias list_files` — GET /medias/files

**objects** — Operations on objects

- `scalify-pp-cli objects create_records` — POST /objects/{id}/records
- `scalify-pp-cli objects delete_records` — DELETE /objects/{id}/records/{id}
- `scalify-pp-cli objects get_objects` — GET /objects/{id}
- `scalify-pp-cli objects get_records` — GET /objects/{id}/records
- `scalify-pp-cli objects get_records_2` — GET /objects/{id}/records/{id}
- `scalify-pp-cli objects list_objects` — GET /objects
- `scalify-pp-cli objects update_records` — PUT /objects/{id}/records/{id}

**opportunities** — Operations on search

- `scalify-pp-cli opportunities create_opportunities` — POST /opportunities
- `scalify-pp-cli opportunities delete_opportunities` — DELETE /opportunities/{id}
- `scalify-pp-cli opportunities get_opportunities` — GET /opportunities/{id}
- `scalify-pp-cli opportunities list_pipelines` — GET /opportunities/pipelines
- `scalify-pp-cli opportunities list_search` — GET /opportunities/search
- `scalify-pp-cli opportunities update_opportunities` — PUT /opportunities/{id}

**payments** — Operations on orders

- `scalify-pp-cli payments create_coupons` — POST /payments/coupons
- `scalify-pp-cli payments delete_coupons` — DELETE /payments/coupons/{id}
- `scalify-pp-cli payments get_coupons` — GET /payments/coupons/{id}
- `scalify-pp-cli payments get_orders` — GET /payments/orders/{id}
- `scalify-pp-cli payments list_coupons` — GET /payments/coupons
- `scalify-pp-cli payments list_orders` — GET /payments/orders
- `scalify-pp-cli payments list_subscriptions` — GET /payments/subscriptions
- `scalify-pp-cli payments list_transactions` — GET /payments/transactions
- `scalify-pp-cli payments update_coupons` — PUT /payments/coupons/{id}

**social-media-posting** — Operations on social-media-posting

- `scalify-pp-cli social-media-posting create_social_media_posting` — POST /social-media-posting
- `scalify-pp-cli social-media-posting delete_social_media_posting` — DELETE /social-media-posting/{id}
- `scalify-pp-cli social-media-posting get_social_media_posting` — GET /social-media-posting/{id}
- `scalify-pp-cli social-media-posting list_social_media_posting` — GET /social-media-posting

**surveys** — Operations on surveys

- `scalify-pp-cli surveys list_submissions` — GET /surveys/submissions
- `scalify-pp-cli surveys list_surveys` — GET /surveys

**users** — Operations on users

- `scalify-pp-cli users get_users` — GET /users/{id}
- `scalify-pp-cli users list_users` — GET /users

**webhooks** — Operations on webhooks

- `scalify-pp-cli webhooks create_webhooks` — POST /webhooks
- `scalify-pp-cli webhooks delete_webhooks` — DELETE /webhooks/{id}
- `scalify-pp-cli webhooks get_webhooks` — GET /webhooks/{id}
- `scalify-pp-cli webhooks list_webhooks` — GET /webhooks
- `scalify-pp-cli webhooks update_webhooks` — PUT /webhooks/{id}

**workflows** — Operations on workflows

- `scalify-pp-cli workflows` — GET /workflows


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
scalify-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Auth Setup

Store your access token:

```bash
scalify-pp-cli auth set-token YOUR_TOKEN_HERE
```

Or set `SCALIFY_TOKEN` as an environment variable.

Run `scalify-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color --yes`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  scalify-pp-cli blogs get_posts mock-value --agent --select id,name,status
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success, and `--ignore-missing` only when a missing delete target should count as success

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal — piped/agent consumers get pure JSON on stdout.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
scalify-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
scalify-pp-cli feedback --stdin < notes.txt
scalify-pp-cli feedback list --json --limit 10
```

Entries are stored locally at `~/.scalify-pp-cli/feedback.jsonl`. They are never POSTed unless `SCALIFY_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `SCALIFY_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled agent calls the same command every run with the same configuration - HeyGen's "Beacon" pattern.

```
scalify-pp-cli profile save briefing --json
scalify-pp-cli --profile briefing blogs get_posts mock-value
scalify-pp-cli profile list --json
scalify-pp-cli profile show briefing
scalify-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `scalify-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

Install the MCP binary from this CLI's published public-library entry or pre-built release, then register it:

```bash
claude mcp add scalify-pp-mcp -- scalify-pp-mcp
```

Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which scalify-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   scalify-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `scalify-pp-cli <command> --help`.
