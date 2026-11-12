#!/usr/bin/env python3
"""Create/read/update/delete test of every scalify-cli write route, against the Scalify Demo sub-account.

Every record it makes is named e2e-<run id> and deleted at the end, even when a step fails. A few routes
reach a real person (send email/SMS, send invoice/estimate, add to workflow): they only ever target the
test contact this script creates, with the email (and phone) you pass in.

  python3 scripts/e2e/crud.py --contact-email will@... [--contact-phone +66...] [--workflow-id ...]
  python3 scripts/e2e/crud.py --dry-run --contact-email will@...     # print every request, send nothing

Needs: Scalify Demo's location token saved (scalify-cli location add OGpQQmmQzXMpwEkaNxHr --token ...).
Writes results to scripts/e2e/last-run.json (git-ignored).
"""
import argparse, datetime, json, os, re, subprocess, sys, time, tomllib

DEMO = "OGpQQmmQzXMpwEkaNxHr"
ALLOWED_EMAIL = re.compile(r"^(will|wrankin1101)@", re.I)
HERE = os.path.dirname(os.path.abspath(__file__))

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--bin", default="scalify-cli", help="CLI binary (default: scalify-cli on PATH)")
ap.add_argument("--mcp-bin", default="scalify-pp-mcp", help="MCP server binary, for the MCP slice ('' to skip)")
ap.add_argument("--contact-email", required=True, help="test contact's email: will@… or wrankin1101@…")
ap.add_argument("--contact-phone", help="test contact's phone, for the SMS test (skipped without it)")
ap.add_argument("--workflow-id", help="a Scalify Demo workflow that is safe to enrol the test contact in")
ap.add_argument("--only", help="comma-separated groups to run (default: all)")
ap.add_argument("--dry-run", action="store_true", help="print each request instead of sending it")
ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
a = ap.parse_args()

if not ALLOWED_EMAIL.match(a.contact_email):
    sys.exit("--contact-email must be a will@ or wrankin1101@ address: it receives real emails")

cfg = tomllib.load(open(os.path.expanduser("~/.config/scalify-pp-cli/config.toml"), "rb"))
if DEMO not in (cfg.get("location_tokens") or {}):
    sys.exit(f"No token saved for Scalify Demo ({DEMO}). Run: scalify-cli location add {DEMO} --token <pit>")

RUN = "e2e-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
NOW = datetime.datetime.now(datetime.timezone.utc)
ENV = {**os.environ, "SCALIFY_LOCATION_ID": DEMO}
ENV.pop("SCALIFY_TOKEN", None)  # use the location token, not an agency one

# Route -> command, from the CLI itself, so renames don't break the suite.
ctx = json.loads(subprocess.run([a.bin, "agent-context"], capture_output=True, text=True, env=ENV, check=True).stdout)
CMD, WRITES = {}, set()
def walk(c, pre):
    p, an = pre + [c["name"]], c.get("annotations", {})
    if "pp:method" in an:
        key = an["pp:method"] + " " + an["pp:path"]
        CMD.setdefault(key, p)
        if an["pp:method"] != "GET":
            WRITES.add(key)
    for s in c.get("subcommands") or []:
        walk(s, p)
for c in ctx["commands"]:
    walk(c, [])

results, cleanup, covered = [], [], set()

def find_id(o, prefer=("id", "_id")):
    """First id in a create response: breadth-first, skipping the CLI's meta envelope."""
    queue = [o]
    while queue:
        cur = queue.pop(0)
        if isinstance(cur, dict):
            for k in prefer:
                if isinstance(cur.get(k), str) and cur[k]:
                    return cur[k]
            queue += [v for k, v in cur.items() if k != "meta"]
        elif isinstance(cur, list):
            queue += cur[:1]
    return None

def unwrap(d):
    if isinstance(d, dict) and "meta" in d and "results" in d:
        return d["results"]
    if isinstance(d, dict) and "action" in d and "data" in d:
        return d["data"]
    return d

def call(step, route, args=(), body=None, flags=(), expect_ok=True):
    """Run one CLI command. Returns the parsed response (or {} on dry-run / failure)."""
    covered.add(route)
    cmd = [a.bin] + CMD[route] + list(args) + list(flags) + ["--json", "--no-input", "--yes", "--no-cache", "--data-source", "live"]
    if body is not None:
        cmd.append("--stdin")
    if a.dry_run:
        cmd.append("--dry-run")
    p = subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=90,
                       input=json.dumps(body) if body is not None else None)
    out = (p.stderr + p.stdout).strip()
    if a.dry_run:
        req = [l.strip() for l in out.splitlines() if re.match(r"\s*(GET|POST|PUT|PATCH|DELETE) ", l)]
        results.append({"step": step, "route": route, "status": "dry-run", "detail": req[0] if req else out[:200]})
        print(f"  dry   {step:<34} {req[0] if req else ''}")
        return {}
    if p.returncode == 0:
        try:
            d = unwrap(json.loads(p.stdout))
        except ValueError:
            d = {}
        results.append({"step": step, "route": route, "status": "ok", "detail": ""})
        print(f"  ok    {step}")
        return d
    msg = next((l for l in out.splitlines() if "HTTP" in l or "rror" in l), out[:300])[:300]
    status = ("not enabled" if "NOT_ENABLED" in msg else "no scope" if "authorized for this scope" in msg else "broken")
    results.append({"step": step, "route": route, "status": status, "detail": msg})
    print(f"  {status:<5} {step}: {msg[:160]}")
    return None

def created(step, route, args=(), body=None, flags=(), undo=None):
    """Create something, remember how to delete it, return its id."""
    d = call(step, route, args, body, flags)
    rid = "dry-" + step.replace(" ", "-") if a.dry_run else (find_id(d) if d is not None else None)
    if rid and undo:
        cleanup.append((step, undo, rid))
    return rid

def undone(step):
    """Mark a create as already deleted by its own test."""
    for i, (s, _, _) in enumerate(cleanup):
        if s == step:
            cleanup.pop(i)
            return

def skip(route, why):
    covered.add(route)
    results.append({"step": route, "route": route, "status": "skipped", "detail": why})
    print(f"  skip  {route}: {why}")

def group(name):
    return not a.only or name in a.only.split(",")

def get(route, args=(), flags=()):
    """A read used for setup (not counted as a test)."""
    if a.dry_run:
        return {}
    p = subprocess.run([a.bin] + CMD[route] + list(args) + list(flags) + ["--json", "--no-input", "--no-cache", "--data-source", "live"],
                       capture_output=True, text=True, env=ENV, timeout=90)
    try:
        return unwrap(json.loads(p.stdout))
    except ValueError:
        return {}

def dig(o, *paths):
    for path in paths:
        cur = o
        for part in path.split("."):
            if isinstance(cur, list):
                cur = cur[int(part)] if part.isdigit() and len(cur) > int(part) else None
            elif isinstance(cur, dict):
                cur = cur.get(part)
            else:
                cur = None
        if cur:
            return cur
    return None

# ---------------------------------------------------------------- confirm
print(f"Scalify Demo ({DEMO}), run {RUN}{' (dry run: nothing is sent)' if a.dry_run else ''}")
print(f"Test contact: {a.contact_email}{' / ' + a.contact_phone if a.contact_phone else ' (no phone: SMS skipped)'}")
print("Real messages: 1 email" + (" + 1 SMS" if a.contact_phone else "") + ", 1 invoice email, 1 estimate email"
      + (f", enrolment in workflow {a.workflow_id}" if a.workflow_id else " (no --workflow-id: enrolment skipped)"))
if not a.dry_run and not a.yes and input("Run against Scalify Demo? [y/N] ").strip().lower() != "y":
    sys.exit("Cancelled.")

loc = get("GET /locations/{locationId}", [DEMO])
company_id = dig(loc, "location.companyId")
users = get("GET /users/search", flags=["--company-id", company_id, "--location-id", DEMO, "--limit", "5"]) if company_id else {}
user_id = "dry-user" if a.dry_run else dig(users, "users.0.id")
contact_id = None

try:
    # ------------------------------------------------------------ contacts
    if group("contacts") or group("conversations") or group("calendars") or group("opportunities") or group("payments"):
        print("contacts")
        body = {"locationId": DEMO, "firstName": "e2e", "lastName": RUN, "email": a.contact_email, "source": RUN}
        if a.contact_phone:
            body["phone"] = a.contact_phone
        contact_id = created("contact create", "POST /contacts/", body=body,
                             undo=lambda i: call("cleanup contact", "DELETE /contacts/{contactId}", [i]))
    if group("contacts") and contact_id:
        call("contact get", "GET /contacts/{contactId}", [contact_id])
        call("contact update", "PUT /contacts/{contactId}", [contact_id], {"lastName": RUN + "-updated"})
        call("contact upsert", "POST /contacts/upsert", body={"locationId": DEMO, "email": a.contact_email, "firstName": "e2e-upsert"})
        call("contact tags add", "POST /contacts/{contactId}/tags", [contact_id], {"tags": [RUN]})
        call("contact tags remove", "DELETE /contacts/{contactId}/tags", [contact_id], flags=["--tags", json.dumps([RUN])])
        call("bulk tags add", "POST /contacts/bulk/tags/update/{type}", ["add"], {"contacts": [contact_id], "tags": [RUN + "-bulk"], "locationId": DEMO})
        call("bulk tags remove", "POST /contacts/bulk/tags/update/{type}", ["remove"], {"contacts": [contact_id], "tags": [RUN + "-bulk"], "locationId": DEMO})
        note = created("note create", "POST /contacts/{contactId}/notes", [contact_id], {"body": RUN})
        if note:
            call("note get", "GET /contacts/{contactId}/notes/{id}", [contact_id, note])
        due = (NOW + datetime.timedelta(days=7)).isoformat().replace("+00:00", "Z")
        task = created("task create", "POST /contacts/{contactId}/tasks", [contact_id], {"title": RUN, "dueDate": due, "completed": False})
        if task:
            call("task get", "GET /contacts/{contactId}/tasks/{taskId}", [contact_id, task])
        call("contact search", "POST /contacts/search", body={"locationId": DEMO, "pageLimit": 1, "query": a.contact_email})
        call("contact count", "POST /contacts/search/count", body={"locationId": DEMO, "query": RUN})
        call("notes search", "POST /notes/search", flags=["--relations", json.dumps([{"objectKey": "contact", "recordId": contact_id}]), "--limit", "5"])
        if a.workflow_id:
            call("workflow enrol", "POST /contacts/{contactId}/workflow/{workflowId}", [contact_id, a.workflow_id], {})
            call("workflow unenrol", "DELETE /contacts/{contactId}/workflow/{workflowId}", [contact_id, a.workflow_id])
        else:
            skip("POST /contacts/{contactId}/workflow/{workflowId}", "no --workflow-id")
            skip("DELETE /contacts/{contactId}/workflow/{workflowId}", "no --workflow-id")

    # ------------------------------------------------------------ conversations
    if group("conversations") and contact_id:
        print("conversations")
        conv = created("conversation create", "POST /conversations/", body={"locationId": DEMO, "contactId": contact_id})
        msg = call("send email", "POST /conversations/messages", body={
            "type": "Email", "contactId": contact_id, "status": "pending", "emailTo": a.contact_email,
            "subject": f"Scalify CLI test {RUN}", "html": f"<p>Automated test from scalify-cli ({RUN}). Ignore.</p>"})
        msg_id = dig(msg, "messageId", "id") if msg else None
        if a.contact_phone:
            call("send SMS", "POST /conversations/messages", body={
                "type": "SMS", "contactId": contact_id, "status": "pending", "message": f"Scalify CLI test {RUN}. Ignore."})
        if msg_id:
            call("message status update", "PUT /conversations/messages/{messageId}/status", [msg_id], {"status": "read"})
        skip("POST /conversations/messages/inbound", "needs a custom conversation provider")

    # ------------------------------------------------------------ opportunities
    if group("opportunities") and contact_id:
        print("opportunities")
        pipes = get("GET /opportunities/pipelines", flags=["--location-id", DEMO])
        pipe, stage = dig(pipes, "pipelines.0.id"), dig(pipes, "pipelines.0.stages.0.id")
        if pipe or a.dry_run:
            opp = created("opportunity create", "POST /opportunities/", body={
                "locationId": DEMO, "pipelineId": pipe, "pipelineStageId": stage, "name": RUN, "status": "open", "contactId": contact_id},
                undo=lambda i: call("cleanup opportunity", "DELETE /opportunities/{id}", [i]))
            if opp:
                call("opportunity get", "GET /opportunities/{id}", [opp])
                call("opportunity update", "PUT /opportunities/{id}", [opp], {"name": RUN + "-updated", "monetaryValue": 1})
                call("opportunity status", "PUT /opportunities/{id}/status", [opp], {"status": "won"})
                call("opportunity search", "POST /opportunities/search", body={"locationId": DEMO, "limit": 1, "query": RUN})
                call("opportunity delete", "DELETE /opportunities/{id}", [opp]); undone("opportunity create")
        else:
            skip("POST /opportunities/", "Scalify Demo has no pipeline")

    # ------------------------------------------------------------ calendars
    if group("calendars"):
        print("calendars")
        team = [{"userId": user_id, "priority": 1, "isPrimary": True}] if user_id else []
        cal = created("calendar create", "POST /calendars/", body={
            "locationId": DEMO, "name": RUN, "calendarType": "event", "teamMembers": team, "slotDuration": 30, "slotDurationUnit": "mins"},
            undo=lambda i: call("cleanup calendar", "DELETE /calendars/{calendarId}", [i]))
        if cal:
            call("calendar get", "GET /calendars/{calendarId}", [cal])
            call("calendar update", "PUT /calendars/{calendarId}", [cal], {"name": RUN + "-updated"})
            if contact_id:
                start = (NOW + datetime.timedelta(days=30)).replace(hour=3, minute=0, second=0, microsecond=0)
                appt = created("appointment create", "POST /calendars/events/appointments", body={
                    "calendarId": cal, "locationId": DEMO, "contactId": contact_id, "title": RUN, "toNotify": False,
                    "ignoreFreeSlotValidation": True, "ignoreDateRange": True,
                    "startTime": start.isoformat(), "endTime": (start + datetime.timedelta(minutes=30)).isoformat()})
                if appt:
                    call("appointment get", "GET /calendars/events/appointments/{eventId}", [appt])
                    call("appointment notes list", "GET /calendars/appointments/{appointmentId}/notes", [appt], flags=["--limit", "5", "--offset", "0"])
            call("calendar delete", "DELETE /calendars/{calendarId}", [cal]); undone("calendar create")

    # ------------------------------------------------------------ location settings
    if group("location"):
        print("location settings")
        cf = created("location custom field create", "POST /locations/{locationId}/customFields", [DEMO],
                     {"name": RUN, "dataType": "TEXT", "model": "contact"},
                     undo=lambda i: call("cleanup custom field", "DELETE /locations/{locationId}/customFields/{id}", [DEMO, i]))
        if cf:
            call("location custom field get", "GET /locations/{locationId}/customFields/{id}", [DEMO, cf])
            call("location custom field update", "PUT /locations/{locationId}/customFields/{id}", [DEMO, cf], {"name": RUN + "-updated"})
            call("location custom field delete", "DELETE /locations/{locationId}/customFields/{id}", [DEMO, cf]); undone("location custom field create")
        cv = created("custom value create", "POST /locations/{locationId}/customValues", [DEMO], {"name": RUN, "value": "1"},
                     undo=lambda i: call("cleanup custom value", "DELETE /locations/{locationId}/customValues/{id}", [DEMO, i]))
        if cv:
            call("custom value get", "GET /locations/{locationId}/customValues/{id}", [DEMO, cv])
            call("custom value update", "PUT /locations/{locationId}/customValues/{id}", [DEMO, cv], {"name": RUN, "value": "2"})
            call("custom value delete", "DELETE /locations/{locationId}/customValues/{id}", [DEMO, cv]); undone("custom value create")
        tag = created("tag create", "POST /locations/{locationId}/tags", [DEMO], {"name": RUN},
                      undo=lambda i: call("cleanup tag", "DELETE /locations/{locationId}/tags/{tagId}", [DEMO, i]))
        if tag:
            call("tag update", "PUT /locations/{locationId}/tags/{tagId}", [DEMO, tag], {"name": RUN + "-updated"})
            call("tag delete", "DELETE /locations/{locationId}/tags/{tagId}", [DEMO, tag]); undone("tag create")
        call("task search", "POST /locations/{locationId}/tasks/search", [DEMO], {})
        skip("PUT /locations/{locationId}", "changes the sub-account itself and needs an agency token")

    # ------------------------------------------------------------ custom objects
    if group("objects"):
        print("custom objects")
        objs = get("GET /objects/", flags=["--location-id", DEMO])
        custom = [o for o in (objs.get("objects") or []) if str(o.get("key", "")).startswith("custom_objects.")] if objs else []
        key = custom[0]["key"] if custom else ("custom_objects.dry" if a.dry_run else None)
        if key:
            folder = created("field folder create", "POST /custom-fields/folder", body={"objectKey": key, "name": RUN, "locationId": DEMO},
                             undo=lambda i: call("cleanup field folder", "DELETE /custom-fields/folder/{id}", [i], flags=["--location-id", DEMO]))
            if folder:
                call("field folder rename", "PUT /custom-fields/folder/{id}", [folder], {"name": RUN + "-renamed", "locationId": DEMO})
                fld = created("field create", "POST /custom-fields/", body={
                    "locationId": DEMO, "name": RUN, "showInForms": False, "dataType": "TEXT", "objectKey": key, "parentId": folder,
                    "fieldKey": key + "." + RUN.replace("-", "_")},
                    undo=lambda i: call("cleanup field", "DELETE /custom-fields/{id}", [i]))
                if fld:
                    call("field get", "GET /custom-fields/{id}", [fld])
                    call("field update", "PUT /custom-fields/{id}", [fld], {"locationId": DEMO, "showInForms": False, "name": RUN + "-updated"})
                    call("field delete", "DELETE /custom-fields/{id}", [fld]); undone("field create")
                call("field folder delete", "DELETE /custom-fields/folder/{id}", [folder], flags=["--location-id", DEMO]); undone("field folder create")
            schema = get("GET /objects/{key}", [key], flags=["--location-id", DEMO])
            prim = dig(schema, "object.primaryDisplayProperty") or "name"
            prop = prim.split(".")[-1]
            rec = created("record create", "POST /objects/{schemaKey}/records", [key], {"locationId": DEMO, "properties": {prop: RUN}},
                          undo=lambda i: call("cleanup record", "DELETE /objects/{schemaKey}/records/{id}", [key, i]))
            if rec:
                call("record get", "GET /objects/{schemaKey}/records/{id}", [key, rec])
                call("record update", "PUT /objects/{schemaKey}/records/{id}", [key, rec], {"properties": {prop: RUN + "-updated"}}, flags=["--location-id", DEMO])
                call("record search", "POST /objects/{schemaKey}/records/search", [key], {"locationId": DEMO, "page": 1, "pageLimit": 5, "query": RUN})
                call("record delete", "DELETE /objects/{schemaKey}/records/{id}", [key, rec]); undone("record create")
        else:
            skip("POST /objects/{schemaKey}/records", "Scalify Demo has no custom object")

    # ------------------------------------------------------------ emails
    if group("emails"):
        print("email templates")
        folder = created("template folder create", "POST /emails/locations/{locationId}/templates/folders", [DEMO], {"name": RUN},
                         undo=lambda i: call("cleanup template folder", "DELETE /emails/locations/{locationId}/templates/{templateId}", [DEMO, i]))
        tpl = created("template create", "POST /emails/locations/{locationId}/templates", [DEMO], {
            "name": RUN, "editorType": "html", "editorContent": f"<p>{RUN}</p>", "subjectLine": RUN, **({"parentFolderId": folder} if folder else {})},
            undo=lambda i: call("cleanup template", "DELETE /emails/locations/{locationId}/templates/{templateId}", [DEMO, i]))
        if tpl:
            call("template get", "GET /emails/locations/{locationId}/templates/{templateId}", [DEMO, tpl])
            call("template update", "PATCH /emails/locations/{locationId}/templates/{templateId}", [DEMO, tpl], {"name": RUN + "-updated"})
            call("template delete", "DELETE /emails/locations/{locationId}/templates/{templateId}", [DEMO, tpl]); undone("template create")
        if folder:
            call("template folder delete", "DELETE /emails/locations/{locationId}/templates/{templateId}", [DEMO, folder]); undone("template folder create")
        skip("POST /emails/locations/{locationId}/templates/import", "needs a Mailchimp/ActiveCampaign share URL")

    # ------------------------------------------------------------ payments
    if group("payments") and contact_id:
        print("invoices and estimates")
        today = NOW.date().isoformat()
        common = {"altId": DEMO, "altType": "location", "currency": "USD", "name": RUN,
                  "businessDetails": {"name": "Scalify Demo"}, "discount": {"type": "fixed", "value": 0},
                  "contactDetails": {"id": contact_id, "name": "e2e " + RUN, "email": a.contact_email, "phoneNo": a.contact_phone or ""}}
        item = {"name": RUN, "currency": "USD", "amount": 1, "qty": 1, "type": "one_time"}
        inv = created("invoice create", "POST /invoices/", body={**common, "items": [item], "issueDate": today,
                      "dueDate": (NOW + datetime.timedelta(days=7)).date().isoformat(), "sentTo": {"email": [a.contact_email]}, "liveMode": False},
                      undo=lambda i: call("cleanup invoice", "DELETE /invoices/{invoiceId}", [i], flags=["--alt-id", DEMO, "--alt-type", "location"]))
        if inv:
            call("invoice get", "GET /invoices/{invoiceId}", [inv], flags=["--alt-id", DEMO, "--alt-type", "location"])
            call("invoice update", "PUT /invoices/{invoiceId}", [inv], {**common, "name": RUN + "-updated", "invoiceItems": [item],
                 "issueDate": today, "dueDate": (NOW + datetime.timedelta(days=14)).date().isoformat()})
            if user_id:
                call("invoice send", "POST /invoices/{invoiceId}/send", [inv], {"altId": DEMO, "altType": "location", "userId": user_id, "action": "email", "liveMode": False})
            call("invoice record payment", "POST /invoices/{invoiceId}/record-payment", [inv], {
                "altId": DEMO, "altType": "location", "mode": "cash", "card": {"brand": "", "last4": ""}, "cheque": {"number": ""}, "notes": RUN, "amount": 1})
        inv2 = created("invoice 2 create", "POST /invoices/", body={**common, "items": [item], "issueDate": today, "sentTo": {"email": [a.contact_email]}, "liveMode": False},
                       undo=lambda i: call("cleanup invoice 2", "DELETE /invoices/{invoiceId}", [i], flags=["--alt-id", DEMO, "--alt-type", "location"]))
        if inv2:
            call("invoice void", "POST /invoices/{invoiceId}/void", [inv2], {"altId": DEMO, "altType": "location"})
            call("invoice delete", "DELETE /invoices/{invoiceId}", [inv2], flags=["--alt-id", DEMO, "--alt-type", "location"]); undone("invoice 2 create")
        est_body = {**common, "items": [item], "liveMode": False, "frequencySettings": {"enabled": False}, "issueDate": today}
        est = created("estimate create", "POST /invoices/estimate", body=est_body,
                      undo=lambda i: call("cleanup estimate", "DELETE /invoices/estimate/{estimateId}", [i], flags=["--alt-id", DEMO, "--alt-type", "location"]))
        if est:
            call("estimate update", "PUT /invoices/estimate/{estimateId}", [est], {**est_body, "name": RUN + "-updated"})
            if user_id:
                call("estimate send", "POST /invoices/estimate/{estimateId}/send", [est], {"altId": DEMO, "altType": "location", "userId": user_id, "action": "email", "liveMode": False})
            call("estimate delete", "DELETE /invoices/estimate/{estimateId}", [est], flags=["--alt-id", DEMO, "--alt-type", "location"]); undone("estimate create")

    # ------------------------------------------------------------ businesses
    if group("businesses"):
        print("businesses")
        biz = created("business create", "POST /businesses/", body={"name": RUN, "locationId": DEMO},
                      undo=lambda i: call("cleanup business", "DELETE /businesses/{businessId}", [i]))
        if biz:
            call("business get", "GET /businesses/{businessId}", [biz])
            call("business update", "PUT /businesses/{businessId}", [biz], {"name": RUN + "-updated"})
            call("business delete", "DELETE /businesses/{businessId}", [biz]); undone("business create")

    # ------------------------------------------------------------ funnels
    if group("funnels"):
        print("funnel redirects")
        existing = get("GET /funnels/lookup/redirect/list", flags=["--location-id", DEMO, "--limit", "5", "--offset", "0"])
        domain = dig(existing, "data.0.domain", "redirects.0.domain") or ("dry.example.com" if a.dry_run else None)
        if domain:
            red = created("redirect create", "POST /funnels/lookup/redirect", body={
                "locationId": DEMO, "domain": domain, "path": "/" + RUN, "target": "https://example.com/", "action": "url"},
                undo=lambda i: call("cleanup redirect", "DELETE /funnels/lookup/redirect/{id}", [i], flags=["--location-id", DEMO]))
            if red:
                call("redirect update", "PATCH /funnels/lookup/redirect/{id}", [red], {"target": "https://example.org/", "action": "url", "locationId": DEMO})
                call("redirect delete", "DELETE /funnels/lookup/redirect/{id}", [red], flags=["--location-id", DEMO]); undone("redirect create")
        else:
            skip("POST /funnels/lookup/redirect", "no existing redirect to borrow a connected domain from")

    # ------------------------------------------------------------ social
    if group("social"):
        print("social posts (draft, scheduled a year out)")
        when = (NOW + datetime.timedelta(days=365)).isoformat().replace("+00:00", "Z")
        post_body = {"type": "post", "status": "draft", "summary": f"{RUN} automated test, never published", "scheduleDate": when}
        post = created("post create", "POST /social-media-posting/{locationId}/posts", [DEMO], post_body,
                       undo=lambda i: call("cleanup post", "DELETE /social-media-posting/{locationId}/posts/{id}", [DEMO, i]))
        if post:
            call("post get", "GET /social-media-posting/{locationId}/posts/{id}", [DEMO, post])
            call("post edit", "PUT /social-media-posting/{locationId}/posts/{id}", [DEMO, post], {**post_body, "summary": RUN + " edited"})
            call("post delete", "DELETE /social-media-posting/{locationId}/posts/{id}", [DEMO, post]); undone("post create")
        call("posts list", "POST /social-media-posting/{locationId}/posts/list", [DEMO], {"limit": "5", "skip": "0"})
        post2 = created("post 2 create", "POST /social-media-posting/{locationId}/posts", [DEMO], post_body,
                        undo=lambda i: call("cleanup post 2", "DELETE /social-media-posting/{locationId}/posts/{id}", [DEMO, i]))
        if post2:
            call("posts bulk delete", "POST /social-media-posting/{locationId}/posts/bulk-delete", [DEMO], {"postIds": [post2]}); undone("post 2 create")

    # ------------------------------------------------------------ workflows (limited availability)
    if group("workflows"):
        print("workflows (only where the workflow API is enabled)")
        wf_body = {"name": RUN, "source": {"type": "api"}, "triggers": [], "actions": [], "edges": []}
        call("workflow validate", "POST /workflows/definition/validate", body=wf_body, flags=["--location-id", DEMO])
        wf = created("workflow create", "POST /workflows/", body=wf_body, flags=["--location-id", DEMO],
                     undo=lambda i: call("cleanup workflow", "DELETE /workflows/{workflowId}", [i], flags=["--location-id", DEMO]))
        if wf:
            call("workflow definition update", "PUT /workflows/{workflowId}/definition", [wf], {**wf_body, "version": 1}, flags=["--location-id", DEMO])
            call("workflow status", "PUT /workflows/{workflowId}/status", [wf], {"status": "draft"}, flags=["--location-id", DEMO])
            call("workflow delete", "DELETE /workflows/{workflowId}", [wf], flags=["--location-id", DEMO]); undone("workflow create")
        call("workflow search", "POST /workflows/search", body={}, flags=["--location-id", DEMO])

    for route, why in [("DELETE /medias/{id}", "no upload route to make a file to delete"),
                       ("POST /social-media-posting/statistics", "a read, covered by the read sweep"),
                       ("POST /users/search/filter-by-email", "a read that needs an agency token"),
                       ("PUT /locations/{locationId}", "changes the sub-account itself and needs an agency token")]:
        if route not in covered:
            skip(route, why)

    # ------------------------------------------------------------ MCP slice
    if a.mcp_bin and not a.dry_run and group("mcp"):
        print("MCP (scalify_execute)")
        p = subprocess.Popen([a.mcp_bin], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, env=ENV)
        n = [0]
        def rpc(method, params=None):
            n[0] += 1
            p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": n[0], "method": method, "params": params or {}}) + "\n"); p.stdin.flush()
            return json.loads(p.stdout.readline())
        def ex(step, endpoint, params):
            r = rpc("tools/call", {"name": "scalify_execute", "arguments": {"endpoint_id": endpoint, "params": params}})["result"]
            text = r["content"][0]["text"]
            ok = not r.get("isError")
            results.append({"step": "mcp " + step, "route": "mcp " + endpoint, "status": "ok" if ok else "broken", "detail": "" if ok else text[:300]})
            print(f"  {'ok' if ok else 'broken':<5} mcp {step}{'' if ok else ': ' + text[:160]}")
            return json.loads(text) if ok else None
        rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "e2e", "version": "0"}})
        tag = find_id(ex("tag create", "locations.tags.create", {"name": RUN + "-mcp"}) or {})
        if tag:
            ex("tag update", "locations.tags.update", {"tagId": tag, "name": RUN + "-mcp-updated"})
            ex("tag delete", "locations.tags.delete", {"tagId": tag})
        cv = find_id(ex("custom value create", "locations.custom-values.create", {"name": RUN + "-mcp", "value": "1"}) or {})
        if cv:
            ex("custom value delete", "locations.custom-values.delete", {"id": cv})
        if contact_id:
            ex("contact tags add", "contacts.tags.add", {"contactId": contact_id, "tags": [RUN + "-mcp"]})
            ex("contact tags remove (DELETE with body)", "contacts.tags.remove", {"contactId": contact_id, "tags": [RUN + "-mcp"]})
            ex("contact search", "contacts.search", {"pageLimit": 1, "query": a.contact_email})
        p.kill()

    if contact_id:
        call("contact delete", "DELETE /contacts/{contactId}", [contact_id]); undone("contact create")
finally:
    # ------------------------------------------------------------ cleanup
    if cleanup and not a.dry_run:
        print("cleanup")
        for step, undo, rid in reversed(cleanup):
            undo(rid)

# ---------------------------------------------------------------- report
untested = sorted(WRITES - covered)
for r in untested:
    results.append({"step": r, "route": r, "status": "not covered", "detail": ""})
counts = {}
for r in results:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
print("\n" + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
for r in results:
    if r["status"] not in ("ok", "dry-run", "skipped"):
        print(f"  {r['status']:<12} {r['step']:<34} {r['detail'][:150]}")
json.dump({"run": RUN, "dry_run": a.dry_run, "results": results}, open(os.path.join(HERE, "last-run.json"), "w"), indent=1)
sys.exit(1 if counts.get("broken") else 0)
