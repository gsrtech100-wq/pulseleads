# AZ PulseLeads — Screenshots

This folder holds the demonstration screenshots. The 10 required captures are listed below with
exact navigation. Live UI PNGs are added manually (no browser automation in the build environment);
textual evidence (run log + dataset) is provided under `../sample_output/` and `../demo_data/` so
the demo can run before the PNGs exist.

## Required screenshots (capture from live UI)
1. **`github_repo.png`** — GitHub repo `gsrtech100-wq/pulseleads` home (shows AZ PulseLeads description, files, license).
2. **`readme.png`** — rendered README (logo + problem/solution + pricing).
3. **`architecture.png`** — `docs/architecture.md` (mermaid pipeline + connector table).
4. **`apify_store.png`** — Apify Store listing `pure_matai~substack-outreach-leads` (title, description, pricing).
5. **`product_input.png`** — Actor input form with prefilled `keywords: ["AI","finance"]` and proxy on.
6. **`running_actor.png`** — Actor run log in progress (proxy init, RSS fetch, "RUN SUMMARY").
7. **`output_dataset.png`** — Dataset table (authorName, hasEmail, twitter, linkedin, website, relevanceScore, contactReady).
8. **`qualified_leads.png`** — "Contact-Ready Leads" dataset view.
9. **`billing.png`** — Run billing / `chargedEventCounts` (after PPE enabled in Console).
10. **`successful_run.png`** — Successful run summary card.

## Branding assets (reuse, don't recreate)
- Logo + lockups: `../branding/az_logo_master_1024.png`, `../branding/az_pulseleads_light.png`,
  `../branding/az_pulseleads_dark.png`, `../branding/az_pulseleads_banner.png`.

## Textual evidence (already captured)
- Real run log: `../sample_output/run_tcgSwbc5txajohDPs.json` (dataset) + run `tcgSwbc5txajohDPs`
  log snippet in `../RELEASE_NOTES.md` / `FINAL_REPORT.md`.
- Illustrative contact-ready example: `../sample_output/contact_ready_example.json`.
