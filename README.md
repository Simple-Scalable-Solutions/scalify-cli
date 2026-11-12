# Scalify CLI

Command-line interface to the Scalify Platform. Manage contacts, conversations, calendars,
opportunities, invoices, and more — directly from your terminal or AI agent.

## Install

### CLI

**macOS / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
```
Installs to `/usr/local/bin`. Open a new shell (or run `hash -r`) after install.

**Windows** (PowerShell)
```powershell
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.ps1 | iex
```
Installs to `%LOCALAPPDATA%\Programs\scalify-cli` and adds it to your user PATH. Restart your terminal after install.

Verify on any platform:
```bash
scalify-cli --version
```

### Claude Code Skill

Install the companion skill so Claude Code understands how to use the CLI on your behalf:

**macOS / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.sh | bash
```

**Windows** (PowerShell)
```powershell
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.ps1 | iex
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

Checks configuration, credentials, API connectivity, and whether a newer version is available. If an update exists, the output will show:

```
  WARN Update available: v1.x.x
    CLI:   curl -fsSL .../install.sh | bash
    Skill: curl -fsSL .../install-skill.sh | bash
```

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

### associations

Manage associations

- **`scalify-cli associations list`** - Get all associations for a sub-account / location
- **`scalify-cli associations list-relations`** - Get all relations by record Id

### blogs

Manage blogs

- **`scalify-cli blogs check-url-slug`** - The "Check url slug" API checks whether a blog post url slug is already in use for the location. Call it before publishing a blog post.
- **`scalify-cli blogs get-all-authors`** - The "Get all blog authors" API returns the blog authors for a given location ID.
- **`scalify-cli blogs get-all-categories`** - The "Get all blog categories" API returns the blog categories for a given location ID.
- **`scalify-cli blogs get-post`** - The "Get Blog Post by ID" API returns a single published blog post, including its content/body, for the given location.
- **`scalify-cli blogs list`** - The "Get Blogs by Location ID" API allows you get blogs using Location ID.
- **`scalify-cli blogs list-posts`** - The "Get Blog posts by Blog ID" API returns the blog posts for a given blog site. Use searchTerm to search across post title, description, url slug and category name.

### businesses

Manage businesses

- **`scalify-cli businesses create`** - Create Business
- **`scalify-cli businesses delete`** - Delete Business
- **`scalify-cli businesses get`** - Get Business
- **`scalify-cli businesses list`** - Get Businesses by Location
- **`scalify-cli businesses update`** - Update Business

### calendars

Manage calendars

- **`scalify-cli calendars create`** - Create calendar in a location.
- **`scalify-cli calendars create-appointment`** - Create appointment
- **`scalify-cli calendars delete`** - Delete calendar by ID
- **`scalify-cli calendars get`** - Get calendar by ID
- **`scalify-cli calendars get-appointment`** - Get appointment by ID
- **`scalify-cli calendars get-blocked-slots`** - Get Blocked Slots. calendarId finds blocks set on an event calendar only. Blocks set on a host (assignedUserId) are found by userId: the host whose blocks to list, including blocks made for personal, round robin and collective calendars.
- **`scalify-cli calendars list`** - Get all calendars in a location.
- **`scalify-cli calendars list-appointment-notes`** - Get Appointment Notes
- **`scalify-cli calendars list-events`** - Get Calendar Events
- **`scalify-cli calendars list-groups`** - Get all calendar groups in a location.
- **`scalify-cli calendars update`** - Update calendar by ID: name, description, duration, slot interval, buffers, minimum notice, booking window, daily limit, seats, auto-confirm, reschedule/cancel, meeting location, booking link (widgetSlug) and team members (hosts). teamMembers replaces the whole list. Collective calendars: every update must include teamMembers, with at least one host isPrimary: true.

### campaigns

Manage campaigns

- **`scalify-cli campaigns list`** - Get Campaigns

### contacts

Manage contacts

- **`scalify-cli contacts count`** - Count the contacts that match a search, without returning them. Takes the same `query` and `filters` as Search Contacts. Large counts can take up to 35 seconds. If the count does not finish in time, the response is `{ "count": null }`; retry the request.
- **`scalify-cli contacts create`** - Create a new contact
- **`scalify-cli contacts delete`** - Delete Contact
- **`scalify-cli contacts get`** - Retrieves a contact by its unique identifier.
- **`scalify-cli contacts get-duplicate`** - Get Duplicate Contact.  If `Allow Duplicate Contact` is disabled under Settings, the global unique identifier will be used for searching the contact. If the setting is enabled, first priority for search is `email` and the second priority will be `phone`.
- **`scalify-cli contacts lookup-by-email-or-phone`** - Look up contacts matching an exact `email` or `phone`, scoped to a location, up to `limit` contacts (max 20) per page. Also matches against a contact's additional emails and additional phone numbers. Exactly one of `email` or `phone` must be provided. Paginate with `nextCursor`. Returns an empty `contacts` array if no contact matches. OAuth channel only.
- **`scalify-cli contacts search`** - Search contacts based on combinations of advanced filters.
- **`scalify-cli contacts update`** - Update a contact using contactId

> ⚠️ **When updating additional emails/phones, always include the current primary `email`/`phone` in the same request. Otherwise, the existing primary value may be lost.**
- **`scalify-cli contacts update-tags`** - Allows you to update tags to multiple contacts at once, you can add or remove tags from the contacts
- **`scalify-cli contacts upsert`** - The Upsert API will adhere to the configuration defined under the "Allow Duplicate Contact" setting at the Location level. If the setting is configured to check both Email and Phone, the API will attempt to identify an existing contact based on the priority sequence specified in the setting, and will create or update the contact accordingly.  If two separate contacts already exist—one with the same email and another with the same phone—and an upsert request includes both the email and phone, the API will update the contact that matches the first field in the configured sequence, and ignore the second field to prevent duplication.

### conversations

Manage conversations

- **`scalify-cli conversations add-inbound-message`** - Post the necessary fields for the API to add a new inbound message.   **Note:** Either `conversationId` or `contactId` is required
- **`scalify-cli conversations create`** - Creates a new conversation with the data provided
- **`scalify-cli conversations export-messages`** - Export messages for a specific location with cursor-based pagination support.

**Channel Filtering Behavior:**
- **When channel is omitted:** Returns all non-email message types, including messages that don't belong to any specific channel.
- **When channel=Email:** Returns email messages only.
- **When channel is specified (SMS, Call, WhatsApp, etc.):** Returns messages for that specific channel.

**Limitations:**
- Group Chat and SMS Review Request message types are not supported.
- Activity messages (opportunity updates, appointments, etc.) are not included in the export. Use `GET /conversations/{conversationId}/messages` (Get messages by conversation id) to fetch them.
- Cursor validity is 2 minutes from the last request made.
- **`scalify-cli conversations get`** - Get the conversation details based on the conversation ID
- **`scalify-cli conversations get-email`** - Get email by Id
- **`scalify-cli conversations get-message`** - Get message by message id.
- **`scalify-cli conversations get-recording`** - Get the recording for a message by passing the message id
- **`scalify-cli conversations get-transcription`** - Get the recording transcription for a message by passing the message id
- **`scalify-cli conversations search`** - Returns a list of all conversations matching the search criteria along with the sort and filter options selected.
- **`scalify-cli conversations send-message`** - Post the necessary fields for the API to send a new message.
- **`scalify-cli conversations update-message-status`** - Post the necessary fields for the API to update message status.

### courses

Manage courses

- **`scalify-cli courses list`** - List courses in the location. Requires a Location token with courses.readonly. Send Version: v3. Each item is the full course object including customizations.

### custom-fields

Manage custom fields

- **`scalify-cli custom-fields create`** - Create Custom Field  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields create-folder`** - Create Custom Field Folder  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields delete`** - Delete Custom Field By Id  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields delete-folder`** - Create Custom Field Folder  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields get`** - Get Custom Field / Folder By Id. 
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields get-by-object-key`** - Get Custom Fields By Object Key  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields rename-folder`** - Create Custom Field Folder  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::
- **`scalify-cli custom-fields update`** - Update Custom Field By Id  
  
 :::info
 Only supports Custom Objects and Company (Business) today. Will be extended to other Standard Objects in the future.
 :::

### emails

Manage emails

- **`scalify-cli emails create-template`** - Create a new email template
- **`scalify-cli emails create-template-folder`** - Create a new template folder
- **`scalify-cli emails delete-template`** - Delete a template
- **`scalify-cli emails get-bulk-action-campaign`** - Get a single bulk action campaign by its ID
- **`scalify-cli emails get-campaign`** - Get a single email campaign by its ID
- **`scalify-cli emails get-campaign-stats`** - Get statistics for email campaigns, workflows, or bulk actions
- **`scalify-cli emails get-template`** - Get a single email template by its ID
- **`scalify-cli emails get-workflow-campaign`** - Get a single workflow campaign by its ID
- **`scalify-cli emails import-template`** - Import a template from a provider URL
- **`scalify-cli emails list-bulk-action-campaigns`** - Get list of bulk action campaigns for a location
- **`scalify-cli emails list-campaigns`** - Get list of email campaigns for a location
- **`scalify-cli emails list-templates`** - Get list of templates by location
- **`scalify-cli emails list-workflow-campaigns`** - Get list of workflow campaigns for a location
- **`scalify-cli emails update-template`** - Update an email template

### forms

Manage forms

- **`scalify-cli forms get-submissions`** - Get Forms Submissions
- **`scalify-cli forms list`** - Get Forms

### funnels

Manage funnels

- **`scalify-cli funnels count-pages`** - Retrieves count of all funnel pages based on the given query parameters.
- **`scalify-cli funnels create-redirect`** - The "Create Redirect" API Allows adding a new url redirect to the system. Use this endpoint to create a url redirect with the specified details. Ensure that the required information is provided in the request payload.
- **`scalify-cli funnels delete-redirect`** - The "Delete Redirect By Id" API Allows deletion of a URL redirect from the system using its unique identifier. Use this endpoint to delete a URL redirect with the specified ID using details provided in the request payload.
- **`scalify-cli funnels list`** - Retrieves a list of all funnels based on the given query parameters.
- **`scalify-cli funnels list-pages`** - Retrieves a list of all funnel pages based on the given query parameters.
- **`scalify-cli funnels list-redirects`** - Retrieves a list of all URL redirects based on the given query parameters.
- **`scalify-cli funnels update-redirect`** - The "Update Redirect By Id" API Allows updating an existing URL redirect in the system. Use this endpoint to modify a URL redirect with the specified ID using details provided in the request payload.

### invoices

Manage invoices

- **`scalify-cli invoices create`** - API to create an invoice
- **`scalify-cli invoices create-estimate`** - Create a new estimate with the provided details
- **`scalify-cli invoices delete`** - API to delete invoice by invoice id
- **`scalify-cli invoices delete-estimate`** - Delete an existing estimate
- **`scalify-cli invoices get`** - API to get invoice by invoice id
- **`scalify-cli invoices get-settings`** - Get the invoice settings for the given location
- **`scalify-cli invoices list`** - API to get list of invoices
- **`scalify-cli invoices list-estimate-templates`** - Get a list of estimate templates or a specific template by ID
- **`scalify-cli invoices list-estimates`** - Get a paginated list of estimates
- **`scalify-cli invoices list-schedules`** - API to get list of schedules
- **`scalify-cli invoices list-templates`** - API to get list of templates
- **`scalify-cli invoices send-estimate`** - API to send estimate by estimate id
- **`scalify-cli invoices update`** - API to update invoice by invoice id
- **`scalify-cli invoices update-estimate`** - Update an existing estimate with new details

### links

Manage links

- **`scalify-cli links list`** - Get Links

### locations

Manage locations

- **`scalify-cli locations get`** - Get details of a Sub-Account (Formerly Location) by passing the sub-account id
- **`scalify-cli locations search`** - Search Sub-Account (Formerly Location)
- **`scalify-cli locations update`** - Update a Sub-Account (Formerly Location) based on the data provided

### medias

Manage medias

- **`scalify-cli medias delete-file`** - Deletes specific file or folder from the media storage
- **`scalify-cli medias list-files`** - Fetches list of files and folders from the media storage

### notes

Manage notes

- **`scalify-cli notes search`** - Search Notes

### objects

Manage objects

- **`scalify-cli objects get-schema`** - Retrieve Object Schema by key or ID. This will return the schema of the custom object, including all its fields and properties. Supported objects include contact, opportunity, business and custom objects.To understand objects and records, please have a look the documentation here : https://doc.clickup.com/8631005/d/h/87cpx-277156/93bf0c2e23177b0
- **`scalify-cli objects list`** - Get all objects for a location. Supported Objects are contact, opportunity, business and custom objects.To understand objects and records, please have a look at the documentation here : https://doc.clickup.com/8631005/d/h/87cpx-277156/93bf0c2e23177b0

### opportunities

Manage opportunities

- **`scalify-cli opportunities create`** - Create an opportunity. `contactId` is optional. Unless the location allows duplicate opportunities (`allowDuplicateOpportunity`), a contact can have only one opportunity per pipeline. Opportunities without a contact are never treated as duplicates. Creating a second opportunity for the same contact in the same pipeline returns 400 with `code: OPPORTUNITY_NO_DUPLICATE` and the existing opportunity id in `meta.existingId`.
- **`scalify-cli opportunities delete`** - Delete Opportunity
- **`scalify-cli opportunities get`** - Get Opportunity
- **`scalify-cli opportunities get-lost-reason`** - Get lost reason
- **`scalify-cli opportunities get-pipeline`** - Retrieves a single pipeline by its ID, including all its stages and configuration.
- **`scalify-cli opportunities list-pipelines`** - Get Pipelines
- **`scalify-cli opportunities search`** - Search Opportunities based on combinations of advanced filters. Send `filters` (each with `field`, `operator` and `value`, or a `group` of `AND`/`OR` filters) and `sort` (`field` and `direction`). `page` starts at 1 (0 is treated as 1) and works with `limit`; `page * limit` cannot exceed 10,000, so use `searchAfter` without `page` to read further.
- **`scalify-cli opportunities search-legacy`** - Search Opportunity
- **`scalify-cli opportunities update`** - Update an opportunity. Unless the location allows duplicate opportunities (`allowDuplicateOpportunity`), a contact can have only one opportunity per pipeline. Opportunities without a contact are never treated as duplicates. Moving an opportunity to a pipeline where its contact already has an opportunity returns 400 with `code: OPPORTUNITY_NO_DUPLICATE`.

### payments

Manage payments

- **`scalify-cli payments get-coupon`** - The "Get Coupon Details" API enables you to retrieve comprehensive information about a specific coupon using either its unique identifier or promotional code. Use this endpoint to view coupon parameters, usage statistics, validity periods, and other promotional details.
- **`scalify-cli payments get-order`** - The "Get Order by ID" API allows to retrieve information for a specific order using its unique identifier. Use this endpoint to fetch details for a single order based on the provided order ID.
- **`scalify-cli payments get-subscription`** - The "Get Subscription by ID" API allows to retrieve information for a specific subscription using its unique identifier. Use this endpoint to fetch details for a single subscription based on the provided subscription ID.
- **`scalify-cli payments get-transaction`** - The "Get Transaction by ID" API allows to retrieve information for a specific transaction using its unique identifier. Use this endpoint to fetch details for a single transaction based on the provided transaction ID.
- **`scalify-cli payments list-coupons`** - The "List Coupons" API allows you to retrieve a list of all coupons available in your location. Use this endpoint to view all promotional offers and special discounts for your customers.
- **`scalify-cli payments list-fulfillments`** - List all fulfillment history of an order
- **`scalify-cli payments list-order-notes`** - List all notes of an order
- **`scalify-cli payments list-orders`** - The "List Orders" API allows to retrieve a paginated list of orders. Customize your results by filtering orders based on name, alt type, order status, payment mode, date range, type of source, contact, funnel products or paginate through the list using the provided query parameters. This endpoint provides a straightforward way to explore and retrieve order information.
- **`scalify-cli payments list-subscriptions`** - The "List Subscriptions" API allows to retrieve a paginated list of subscriptions. Customize your results by filtering subscriptions based on name, alt type, subscription status, payment mode, date range, type of source, contact, subscription id, entity id, contact or paginate through the list using the provided query parameters. This endpoint provides a straightforward way to explore and retrieve subscription information.
- **`scalify-cli payments list-transactions`** - The "List Transactions" API allows to retrieve a paginated list of transactions. Customize your results by filtering transactions based on name, alt type, transaction status, payment mode, date range, type of source, contact, subscription id, entity id or paginate through the list using the provided query parameters. This endpoint provides a straightforward way to explore and retrieve transaction information.

### products

Manage products

- **`scalify-cli products get`** - The "Get Product by ID" API allows to retrieve information for a specific product using its unique identifier. Use this endpoint to fetch details for a single product based on the provided product ID.
- **`scalify-cli products list`** - The "List Products" API allows to retrieve a paginated list of products. Customize your results by filtering products based on name or paginate through the list using the provided query parameters. This endpoint provides a straightforward way to explore and retrieve product information.
- **`scalify-cli products list-collections`** - Internal API to fetch the Product Collections
- **`scalify-cli products list-inventory`** - The "List Inventory API allows the user to retrieve a paginated list of inventory items. Use this endpoint to fetch details for multiple items in the inventory based on the provided query parameters.

### proposals

Manage proposals

- **`scalify-cli proposals list-documents`** - List documents for a location
- **`scalify-cli proposals list-templates`** - List document contract templates for a location

### social-media-posting

Manage social media posting

- **`scalify-cli social-media-posting get-statistics`** - Retrieve analytics data for multiple social media accounts. Supports custom date ranges for both the current period and a comparison period. If no date ranges are provided, defaults to the last 7 days (excluding today) with comparison to the previous 7 days.

### surveys

Manage surveys

- **`scalify-cli surveys get-submissions`** - Get Surveys Submissions
- **`scalify-cli surveys list`** - Get Surveys

### users

Manage users

- **`scalify-cli users filter-by-email`** - Filter users by company ID, deleted status, and email array
- **`scalify-cli users get`** - Get User
- **`scalify-cli users search`** - Search Users

### workflows

Manage workflows

- **`scalify-cli workflows create`** - **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other sub-account receives 403 `WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`.

Create a workflow from a complete definition. The definition is validated in full before anything is persisted, so a rejected request creates nothing. Workflows are always created in `draft`; use Update Workflow Status to publish.
- **`scalify-cli workflows delete`** - **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other sub-account receives 403 `WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`.

Delete a workflow. This also ends any enrollments in progress, so contacts currently moving through the workflow stop where they are. Treat it as permanent.
- **`scalify-cli workflows list`** - Get Workflow
- **`scalify-cli workflows list-step-types`** - **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other sub-account receives 403 `WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`.

Browse or fetch the action and trigger schemas available to a sub-account, so a definition can be built against real field names before saving.

Every response is paged and every entry carries its full field schema, including the `assetReferences` that say which fields must hold IDs of assets that already exist. Default page size is 20.

Narrow with `types`, which matches on the step type **key** and matches partially — `email` returns `send_email` as well as `email`. Use `query` instead to match names and descriptions too. Page with `limit` and `skip`.
- **`scalify-cli workflows search`** - **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other sub-account receives 403 `WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`.

Find workflows in a sub-account by name, status, folder or timestamp. Returns summaries only — pass an ID to Get Workflow Definition for the full definition.

Filters are combined with AND. Page with `offset` for the first few pages and switch to the `searchAfter` cursor for deeper paging; sending both is rejected.
- **`scalify-cli workflows validate-definition`** - **Limited availability.** The workflow API is currently enabled for selected sub-accounts only; any other sub-account receives 403 `WORKFLOW_API_NOT_ENABLED_FOR_LOCATION`.

Run the full save pipeline against a definition and report what a real save would do. Nothing is persisted. Returns 200 with `valid: false` when the definition is rejected — a 4xx here means the request itself was malformed.


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

**macOS / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.sh | bash
```

**Windows** (PowerShell)
```powershell
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.ps1 | iex
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

## Staying Up to Date

`scalify-cli doctor` automatically checks for newer releases on every run. When an update is available it prints the upgrade commands directly in the output — no manual version checking needed.

**Upgrade the CLI binary:**

macOS / Linux:
```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.sh | bash
```
Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install.ps1 | iex
```

**Upgrade the Claude Code skill:**

macOS / Linux:
```bash
curl -fsSL https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.sh | bash
```
Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/Simple-Scalable-Solutions/scalify-cli/main/install-skill.ps1 | iex
```

Then start a new Claude Code session for the skill update to take effect.

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
