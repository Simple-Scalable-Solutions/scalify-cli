---
name: scalify-cli
description: "Scalify Platform CLI"
author: "scalify"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - scalify-cli
---

# Scalify — CLI

## Prerequisites: Install the CLI

This skill drives the `scalify-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the one-liner installer:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
   ```
2. Verify: `scalify-cli --version`

If `--version` reports "command not found" after install, open a new shell or run `hash -r`, then verify again.

Scalify Platform API

## HTTP Transport

This CLI makes direct HTTP requests to the Scalify REST API. It does not require Node.js or any external runtime.

## Command Reference

**blogs** — Operations on posts

- `scalify-cli blogs get-posts` — GET /blogs/{id}/posts/{id}
- `scalify-cli blogs list-authors` — GET /blogs/authors
- `scalify-cli blogs list-categories` — GET /blogs/categories
- `scalify-cli blogs list-posts` — GET /blogs/posts
- `scalify-cli blogs list-url-slug-exists` — GET /blogs/posts/url-slug-exists

**businesses** — Operations on businesses

- `scalify-cli businesses create-businesses` — POST /businesses
- `scalify-cli businesses delete-businesses` — DELETE /businesses/{id}
- `scalify-cli businesses get-businesses` — GET /businesses/{id}
- `scalify-cli businesses list-businesses` — GET /businesses
- `scalify-cli businesses update-businesses` — PUT /businesses/{id}

**calendars** — Operations on calendars

- `scalify-cli calendars create-appointments` — POST /calendars/events/appointments
- `scalify-cli calendars create-calendars` — POST /calendars
- `scalify-cli calendars delete-calendars` — DELETE /calendars/{id}
- `scalify-cli calendars get-calendars` — GET /calendars/{id}
- `scalify-cli calendars get-free-slots` — GET /calendars/{id}/free-slots
- `scalify-cli calendars list-calendars` — GET /calendars
- `scalify-cli calendars list-events` — GET /calendars/events
- `scalify-cli calendars update-calendars` — PUT /calendars/{id}

**campaigns** — Operations on campaigns

- `scalify-cli campaigns` — GET /campaigns

**contacts** — Operations on contacts

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

**conversations** — Operations on conversations

- `scalify-cli conversations create-conversations` — POST /conversations
- `scalify-cli conversations create-inbound` — POST /conversations/messages/inbound
- `scalify-cli conversations create-messages` — POST /conversations/messages
- `scalify-cli conversations get-conversations` — GET /conversations/{id}
- `scalify-cli conversations get-messages` — GET /conversations/{id}/messages
- `scalify-cli conversations get-messages-2` — GET /conversations/messages/{id}
- `scalify-cli conversations list-search` — GET /conversations/search
- `scalify-cli conversations update-status` — PUT /conversations/messages/{id}/status

**courses** — Operations on courses

- `scalify-cli courses` — GET /courses

**documents** — Operations on documents

- `scalify-cli documents create-send` — POST /documents/{id}/send
- `scalify-cli documents delete-documents` — DELETE /documents/{id}
- `scalify-cli documents get-documents` — GET /documents/{id}
- `scalify-cli documents list-documents` — GET /documents

**emails** — Operations on emails

- `scalify-cli emails` — GET /emails

**forms** — Operations on forms

- `scalify-cli forms list-forms` — GET /forms
- `scalify-cli forms list-submissions` — GET /forms/submissions

**funnels** — Operations on funnels

- `scalify-cli funnels list-funnels` — GET /funnels
- `scalify-cli funnels list-list` — GET /funnels/funnel/list
- `scalify-cli funnels list-page` — GET /funnels/page

**invoices** — Operations on invoices

- `scalify-cli invoices create-estimate` — POST /invoices/estimate
- `scalify-cli invoices create-invoices` — POST /invoices
- `scalify-cli invoices create-record-payment` — POST /invoices/{id}/record-payment
- `scalify-cli invoices create-send` — POST /invoices/{id}/send
- `scalify-cli invoices create-send-2` — POST /invoices/estimate/{id}/send
- `scalify-cli invoices create-void` — POST /invoices/{id}/void
- `scalify-cli invoices delete-estimate` — DELETE /invoices/estimate/{id}
- `scalify-cli invoices delete-invoices` — DELETE /invoices/{id}
- `scalify-cli invoices get-estimate` — GET /invoices/estimate/{id}
- `scalify-cli invoices get-invoices` — GET /invoices/{id}
- `scalify-cli invoices list-estimate` — GET /invoices/estimate
- `scalify-cli invoices list-invoices` — GET /invoices
- `scalify-cli invoices update-estimate` — PUT /invoices/estimate/{id}
- `scalify-cli invoices update-invoices` — PUT /invoices/{id}

**links** — Operations on links

- `scalify-cli links` — GET /links

**locations** — Operations on locations

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

**medias** — Operations on files

- `scalify-cli medias delete-medias` — DELETE /medias/{id}
- `scalify-cli medias list-files` — GET /medias/files

**objects** — Operations on objects

- `scalify-cli objects create-records` — POST /objects/{id}/records
- `scalify-cli objects delete-records` — DELETE /objects/{id}/records/{id}
- `scalify-cli objects get-objects` — GET /objects/{id}
- `scalify-cli objects get-records` — GET /objects/{id}/records
- `scalify-cli objects get-records-2` — GET /objects/{id}/records/{id}
- `scalify-cli objects list-objects` — GET /objects
- `scalify-cli objects update-records` — PUT /objects/{id}/records/{id}

**opportunities** — Operations on opportunities

- `scalify-cli opportunities create-opportunities` — POST /opportunities
- `scalify-cli opportunities delete-opportunities` — DELETE /opportunities/{id}
- `scalify-cli opportunities get-opportunities` — GET /opportunities/{id}
- `scalify-cli opportunities list-pipelines` — GET /opportunities/pipelines
- `scalify-cli opportunities list-search` — GET /opportunities/search
- `scalify-cli opportunities update-opportunities` — PUT /opportunities/{id}

**payments** — Operations on payments

- `scalify-cli payments create-coupons` — POST /payments/coupons
- `scalify-cli payments delete-coupons` — DELETE /payments/coupons/{id}
- `scalify-cli payments get-coupons` — GET /payments/coupons/{id}
- `scalify-cli payments get-orders` — GET /payments/orders/{id}
- `scalify-cli payments list-coupons` — GET /payments/coupons
- `scalify-cli payments list-orders` — GET /payments/orders
- `scalify-cli payments list-subscriptions` — GET /payments/subscriptions
- `scalify-cli payments list-transactions` — GET /payments/transactions
- `scalify-cli payments update-coupons` — PUT /payments/coupons/{id}

**social-media-posting** — Operations on social-media-posting

- `scalify-cli social-media-posting create-social-media-posting` — POST /social-media-posting
- `scalify-cli social-media-posting delete-social-media-posting` — DELETE /social-media-posting/{id}
- `scalify-cli social-media-posting get-social-media-posting` — GET /social-media-posting/{id}
- `scalify-cli social-media-posting list-social-media-posting` — GET /social-media-posting

**surveys** — Operations on surveys

- `scalify-cli surveys list-submissions` — GET /surveys/submissions
- `scalify-cli surveys list-surveys` — GET /surveys

**users** — Operations on users

- `scalify-cli users get-users` — GET /users/{id}
- `scalify-cli users list-users` — GET /users

**webhooks** — Operations on webhooks

- `scalify-cli webhooks create-webhooks` — POST /webhooks
- `scalify-cli webhooks delete-webhooks` — DELETE /webhooks/{id}
- `scalify-cli webhooks get-webhooks` — GET /webhooks/{id}
- `scalify-cli webhooks list-webhooks` — GET /webhooks
- `scalify-cli webhooks update-webhooks` — PUT /webhooks/{id}

**workflows** — Operations on workflows

- `scalify-cli workflows` — GET /workflows


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
scalify-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Auth Setup

Store your access token:

```bash
scalify-cli auth set-token YOUR_TOKEN_HERE
```

Or set `SCALIFY_TOKEN` as an environment variable.

Run `scalify-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color --yes`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  scalify-cli blogs get-posts mock-value --agent --select id,name,status
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
scalify-cli feedback "the --since flag is inclusive but docs say exclusive"
scalify-cli feedback --stdin < notes.txt
scalify-cli feedback list --json --limit 10
```

Entries are stored locally at `~/.config/scalify-pp-cli/feedback.jsonl`. They are never POSTed unless `SCALIFY_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `SCALIFY_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

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

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled agent calls the same command every run with the same configuration.

```
scalify-cli profile save briefing --json
scalify-cli --profile briefing blogs get-posts mock-value
scalify-cli profile list --json
scalify-cli profile show briefing
scalify-cli profile delete briefing --yes
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

1. **Empty, `help`, or `--help`** → show `scalify-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

Register the MCP server:

```bash
claude mcp add scalify-pp-mcp -- scalify-pp-mcp
```

Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which scalify-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   scalify-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `scalify-cli <command> --help`.
