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

**associations** — Manage associations

- `scalify-cli associations list` — Get all associations for a sub-account / location
- `scalify-cli associations list-relations` — Get all relations by record Id

**blogs** — Manage blogs

- `scalify-cli blogs check-url-slug` — The 'Check url slug' API checks whether a blog post url slug is already in use for the location. Call it before...
- `scalify-cli blogs get-all-authors` — The 'Get all blog authors' API returns the blog authors for a given location ID.
- `scalify-cli blogs get-all-categories` — The 'Get all blog categories' API returns the blog categories for a given location ID.
- `scalify-cli blogs get-post` — The 'Get Blog Post by ID' API returns a single published blog post, including its content/body, for the given location.
- `scalify-cli blogs list` — The 'Get Blogs by Location ID' API allows you get blogs using Location ID.
- `scalify-cli blogs list-posts` — The 'Get Blog posts by Blog ID' API returns the blog posts for a given blog site. Use searchTerm to search across...

**businesses** — Manage businesses

- `scalify-cli businesses create` — Create Business
- `scalify-cli businesses delete` — Delete Business
- `scalify-cli businesses get` — Get Business
- `scalify-cli businesses list` — Get Businesses by Location
- `scalify-cli businesses update` — Update Business

**calendars** — Manage calendars

- `scalify-cli calendars create` — Create calendar in a location.
- `scalify-cli calendars create-appointment` — Create appointment
- `scalify-cli calendars delete` — Delete calendar by ID
- `scalify-cli calendars get` — Get calendar by ID
- `scalify-cli calendars get-appointment` — Get appointment by ID
- `scalify-cli calendars get-blocked-slots` — Get Blocked Slots. calendarId finds blocks set on an event calendar only. Blocks set on a host (assignedUserId) are...
- `scalify-cli calendars list` — Get all calendars in a location.
- `scalify-cli calendars list-appointment-notes` — Get Appointment Notes
- `scalify-cli calendars list-events` — Get Calendar Events
- `scalify-cli calendars list-groups` — Get all calendar groups in a location.
- `scalify-cli calendars update` — Update calendar by ID: name, description, duration, slot interval, buffers, minimum notice, booking window, daily...

**campaigns** — Manage campaigns

- `scalify-cli campaigns` — Get Campaigns

**contacts** — Manage contacts

- `scalify-cli contacts count` — Count the contacts that match a search, without returning them. Takes the same `query` and `filters` as Search...
- `scalify-cli contacts create` — Create a new contact
- `scalify-cli contacts delete` — Delete Contact
- `scalify-cli contacts get` — Retrieves a contact by its unique identifier.
- `scalify-cli contacts get-duplicate` — Get Duplicate Contact. If `Allow Duplicate Contact` is disabled under Settings, the global unique identifier will be...
- `scalify-cli contacts lookup-by-email-or-phone` — Look up contacts matching an exact `email` or `phone`, scoped to a location, up to `limit` contacts (max 20) per...
- `scalify-cli contacts search` — Search contacts based on combinations of advanced filters.
- `scalify-cli contacts update` — Update a contact using contactId > ⚠️ **When updating additional emails/phones, always include the current...
- `scalify-cli contacts update-tags` — Allows you to update tags to multiple contacts at once, you can add or remove tags from the contacts
- `scalify-cli contacts upsert` — The Upsert API will adhere to the configuration defined under the 'Allow Duplicate Contact' setting at the Location...

**conversations** — Manage conversations

- `scalify-cli conversations add-inbound-message` — Post the necessary fields for the API to add a new inbound message. **Note:** Either `conversationId` or `contactId`...
- `scalify-cli conversations create` — Creates a new conversation with the data provided
- `scalify-cli conversations export-messages` — Export messages for a specific location with cursor-based pagination support. **Channel Filtering Behavior:** -...
- `scalify-cli conversations get` — Get the conversation details based on the conversation ID
- `scalify-cli conversations get-email` — Get email by Id
- `scalify-cli conversations get-message` — Get message by message id.
- `scalify-cli conversations get-recording` — Get the recording for a message by passing the message id
- `scalify-cli conversations get-transcription` — Get the recording transcription for a message by passing the message id
- `scalify-cli conversations search` — Returns a list of all conversations matching the search criteria along with the sort and filter options selected.
- `scalify-cli conversations send-message` — Post the necessary fields for the API to send a new message.
- `scalify-cli conversations update-message-status` — Post the necessary fields for the API to update message status.

**courses** — Manage courses

- `scalify-cli courses` — List courses in the location. Requires a Location token with courses.readonly. Send Version: v3. Each item is the...

**custom-fields** — Manage custom fields

- `scalify-cli custom-fields create` — Create Custom Field :::info Only supports Custom Objects and Company (Business) today. Will be extended to other...
- `scalify-cli custom-fields create-folder` — Create Custom Field Folder :::info Only supports Custom Objects and Company (Business) today. Will be extended to...
- `scalify-cli custom-fields delete` — Delete Custom Field By Id :::info Only supports Custom Objects and Company (Business) today. Will be extended to...
- `scalify-cli custom-fields delete-folder` — Create Custom Field Folder :::info Only supports Custom Objects and Company (Business) today. Will be extended to...
- `scalify-cli custom-fields get` — Get Custom Field / Folder By Id. :::info Only supports Custom Objects and Company (Business) today. Will be extended...
- `scalify-cli custom-fields get-by-object-key` — Get Custom Fields By Object Key :::info Only supports Custom Objects and Company (Business) today. Will be extended...
- `scalify-cli custom-fields rename-folder` — Create Custom Field Folder :::info Only supports Custom Objects and Company (Business) today. Will be extended to...
- `scalify-cli custom-fields update` — Update Custom Field By Id :::info Only supports Custom Objects and Company (Business) today. Will be extended to...

**emails** — Manage emails

- `scalify-cli emails create-template` — Create a new email template
- `scalify-cli emails create-template-folder` — Create a new template folder
- `scalify-cli emails delete-template` — Delete a template
- `scalify-cli emails get-bulk-action-campaign` — Get a single bulk action campaign by its ID
- `scalify-cli emails get-campaign` — Get a single email campaign by its ID
- `scalify-cli emails get-campaign-stats` — Get statistics for email campaigns, workflows, or bulk actions
- `scalify-cli emails get-template` — Get a single email template by its ID
- `scalify-cli emails get-workflow-campaign` — Get a single workflow campaign by its ID
- `scalify-cli emails import-template` — Import a template from a provider URL
- `scalify-cli emails list-bulk-action-campaigns` — Get list of bulk action campaigns for a location
- `scalify-cli emails list-campaigns` — Get list of email campaigns for a location
- `scalify-cli emails list-templates` — Get list of templates by location
- `scalify-cli emails list-workflow-campaigns` — Get list of workflow campaigns for a location
- `scalify-cli emails update-template` — Update an email template

**forms** — Manage forms

- `scalify-cli forms get-submissions` — Get Forms Submissions
- `scalify-cli forms list` — Get Forms

**funnels** — Manage funnels

- `scalify-cli funnels count-pages` — Retrieves count of all funnel pages based on the given query parameters.
- `scalify-cli funnels create-redirect` — The 'Create Redirect' API Allows adding a new url redirect to the system. Use this endpoint to create a url redirect...
- `scalify-cli funnels delete-redirect` — The 'Delete Redirect By Id' API Allows deletion of a URL redirect from the system using its unique identifier. Use...
- `scalify-cli funnels list` — Retrieves a list of all funnels based on the given query parameters.
- `scalify-cli funnels list-pages` — Retrieves a list of all funnel pages based on the given query parameters.
- `scalify-cli funnels list-redirects` — Retrieves a list of all URL redirects based on the given query parameters.
- `scalify-cli funnels update-redirect` — The 'Update Redirect By Id' API Allows updating an existing URL redirect in the system. Use this endpoint to modify...

**invoices** — Manage invoices

- `scalify-cli invoices create` — API to create an invoice
- `scalify-cli invoices create-estimate` — Create a new estimate with the provided details
- `scalify-cli invoices delete` — API to delete invoice by invoice id
- `scalify-cli invoices delete-estimate` — Delete an existing estimate
- `scalify-cli invoices get` — API to get invoice by invoice id
- `scalify-cli invoices get-settings` — Get the invoice settings for the given location
- `scalify-cli invoices list` — API to get list of invoices
- `scalify-cli invoices list-estimate-templates` — Get a list of estimate templates or a specific template by ID
- `scalify-cli invoices list-estimates` — Get a paginated list of estimates
- `scalify-cli invoices list-schedules` — API to get list of schedules
- `scalify-cli invoices list-templates` — API to get list of templates
- `scalify-cli invoices send-estimate` — API to send estimate by estimate id
- `scalify-cli invoices update` — API to update invoice by invoice id
- `scalify-cli invoices update-estimate` — Update an existing estimate with new details

**links** — Manage links

- `scalify-cli links` — Get Links

**locations** — Manage locations

- `scalify-cli locations get` — Get details of a Sub-Account (Formerly Location) by passing the sub-account id
- `scalify-cli locations search` — Search Sub-Account (Formerly Location)
- `scalify-cli locations update` — Update a Sub-Account (Formerly Location) based on the data provided

**medias** — Manage medias

- `scalify-cli medias delete-file` — Deletes specific file or folder from the media storage
- `scalify-cli medias list-files` — Fetches list of files and folders from the media storage

**notes** — Manage notes

- `scalify-cli notes` — Search Notes

**objects** — Manage objects

- `scalify-cli objects get-schema` — Retrieve Object Schema by key or ID. This will return the schema of the custom object, including all its fields and...
- `scalify-cli objects list` — Get all objects for a location. Supported Objects are contact, opportunity, business and custom objects.To...

**opportunities** — Manage opportunities

- `scalify-cli opportunities create` — Create an opportunity. `contactId` is optional. Unless the location allows duplicate opportunities...
- `scalify-cli opportunities delete` — Delete Opportunity
- `scalify-cli opportunities get` — Get Opportunity
- `scalify-cli opportunities get-lost-reason` — Get lost reason
- `scalify-cli opportunities get-pipeline` — Retrieves a single pipeline by its ID, including all its stages and configuration.
- `scalify-cli opportunities list-pipelines` — Get Pipelines
- `scalify-cli opportunities search` — Search Opportunities based on combinations of advanced filters. Send `filters` (each with `field`, `operator` and...
- `scalify-cli opportunities search-legacy` — Search Opportunity
- `scalify-cli opportunities update` — Update an opportunity. Unless the location allows duplicate opportunities (`allowDuplicateOpportunity`), a contact...

**payments** — Manage payments

- `scalify-cli payments get-coupon` — The 'Get Coupon Details' API enables you to retrieve comprehensive information about a specific coupon using either...
- `scalify-cli payments get-order` — The 'Get Order by ID' API allows to retrieve information for a specific order using its unique identifier. Use this...
- `scalify-cli payments get-subscription` — The 'Get Subscription by ID' API allows to retrieve information for a specific subscription using its unique...
- `scalify-cli payments get-transaction` — The 'Get Transaction by ID' API allows to retrieve information for a specific transaction using its unique...
- `scalify-cli payments list-coupons` — The 'List Coupons' API allows you to retrieve a list of all coupons available in your location. Use this endpoint to...
- `scalify-cli payments list-fulfillments` — List all fulfillment history of an order
- `scalify-cli payments list-order-notes` — List all notes of an order
- `scalify-cli payments list-orders` — The 'List Orders' API allows to retrieve a paginated list of orders. Customize your results by filtering orders...
- `scalify-cli payments list-subscriptions` — The 'List Subscriptions' API allows to retrieve a paginated list of subscriptions. Customize your results by...
- `scalify-cli payments list-transactions` — The 'List Transactions' API allows to retrieve a paginated list of transactions. Customize your results by filtering...

**products** — Manage products

- `scalify-cli products get` — The 'Get Product by ID' API allows to retrieve information for a specific product using its unique identifier. Use...
- `scalify-cli products list` — The 'List Products' API allows to retrieve a paginated list of products. Customize your results by filtering...
- `scalify-cli products list-collections` — Internal API to fetch the Product Collections
- `scalify-cli products list-inventory` — The 'List Inventory API allows the user to retrieve a paginated list of inventory items. Use this endpoint to fetch...

**proposals** — Manage proposals

- `scalify-cli proposals list-documents` — List documents for a location
- `scalify-cli proposals list-templates` — List document contract templates for a location

**social-media-posting** — Manage social media posting

- `scalify-cli social-media-posting` — Retrieve analytics data for multiple social media accounts. Supports custom date ranges for both the current period...

**surveys** — Manage surveys

- `scalify-cli surveys get-submissions` — Get Surveys Submissions
- `scalify-cli surveys list` — Get Surveys

**users** — Manage users

- `scalify-cli users filter-by-email` — Filter users by company ID, deleted status, and email array
- `scalify-cli users get` — Get User
- `scalify-cli users search` — Search Users

**workflows** — Manage workflows

- `scalify-cli workflows create` — **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other...
- `scalify-cli workflows delete` — **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other...
- `scalify-cli workflows list` — Get Workflow
- `scalify-cli workflows list-step-types` — **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other...
- `scalify-cli workflows search` — **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other...
- `scalify-cli workflows validate-definition` — **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other...


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
scalify-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

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
