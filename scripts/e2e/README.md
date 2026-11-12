# End-to-end write test

`crud.py` creates, reads, updates and deletes one of everything the CLI can write, on the **Scalify Demo**
sub-account (`OGpQQmmQzXMpwEkaNxHr`) only, plus a few writes through the MCP server's `scalify_execute`.
Run it before a release.

```shell
python3 scripts/e2e/crud.py --dry-run --contact-email will@…            # print every request, send nothing
python3 scripts/e2e/crud.py --contact-email will@… [--contact-phone +66…] [--workflow-id <safe demo workflow>]
```

- Asks before it sends anything (`--yes` skips the prompt). Ask whoever owns the test email first: it gets
  real messages (1 email, 1 invoice, 1 estimate; 1 SMS with `--contact-phone`).
- Everything it makes is named `e2e-<run id>` and is deleted at the end, even if a step fails.
- `--only contacts,payments` runs some groups: contacts, conversations, opportunities, calendars, location,
  objects, emails, payments, businesses, funnels, social, workflows, mcp.
- Results: one line per step (ok / broken / not enabled / no scope / skipped), any write route the run didn't
  reach ("not covered"), and `scripts/e2e/last-run.json`. Exit code 1 if anything is broken.
- Needs Scalify Demo's location token saved: `scalify-cli location add OGpQQmmQzXMpwEkaNxHr --token <pit>`.
- Workflow create/update/delete only work where the workflow API is enabled; elsewhere they show "not enabled".
