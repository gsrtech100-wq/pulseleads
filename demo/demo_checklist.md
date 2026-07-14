# AZ PulseLeads — Demo Checklist

Run through this before every live demonstration.

## Pre-demo (5 min before)
- [ ] Apify Actor `pure_matai~substack-outreach-leads` is pushed and built (build `0.1.2`+).
- [ ] Pay-per-event (PPE) is enabled in the Apify Console (Monetization) with
      `LEAD_DISCOVERED` $0.00030 (if billing is to be shown live).
- [ ] `demo_data/demo_input.json` is ready to paste.
- [ ] Screenshots from a previous run are available in `demo/screenshots/` as backup.
- [ ] Internet + Apify proxy working.

## During demo
- [ ] Show logo/banner (`demo/branding/az_pulseleads_banner.png`).
- [ ] Show customer problem (manual Substack discovery pain).
- [ ] Show architecture (`docs/architecture.md` or `demo/screenshots/architecture.png`).
- [ ] Paste input and run.
- [ ] Show run log (proxy, RSS fetch, RUN SUMMARY).
- [ ] Show output dataset with `hasEmail` / `twitter` / `linkedin` / `website`.
- [ ] Switch to "Contact-Ready Leads" view.
- [ ] Show pricing / per-lead cost.
- [ ] Handle objections using `faq.md`.

## Post-demo
- [ ] Save new screenshots/videos into `demo/screenshots/` and `demo/videos/`.
- [ ] Note any customer questions in `release_demo_notes.md`.
- [ ] If PPE shown live, capture `chargedEventCounts.LEAD_DISCOVERED > 0` for proof.

## Screenshot capture list (store in `demo/screenshots/`)
- [ ] `github_repo.png` — GitHub repository home.
- [ ] `readme.png` — README rendered.
- [ ] `architecture.png` — architecture diagram.
- [ ] `apify_store.png` — Apify Store listing.
- [ ] `product_input.png` — input form with prefilled keywords.
- [ ] `running_actor.png` — actor run in progress / log.
- [ ] `output_dataset.png` — dataset table.
- [ ] `qualified_leads.png` — "Contact-Ready Leads" view.
- [ ] `billing.png` — billing / charged events (after PPE enabled).
- [ ] `successful_run.png` — successful run summary.
