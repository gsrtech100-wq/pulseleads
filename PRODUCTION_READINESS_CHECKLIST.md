# AZ PulseLeads — Production Readiness Checklist

Status: ✅ Code / Docs / Repo / Run / Publication (public) verified. ⚠ Pay-per-event pricing blocked by an Apify API defect (manual Console enablement required) — only remaining open item.

## Engineering
- [x] **Tests** — 7 offline tests pass (`pytest tests -q`); modules import cleanly.
- [x] **Build** — `apify push --version 1.0` succeeded; **build `1.0.1`**, image built and pushed.
- [x] **Docker** — `FROM apify/actor-python:3.12`, pinned deps, `CMD python -m src.main`.
- [x] **Dependencies** — `requirements.txt` pinned (`apify==3.4.1`, `httpx`, `beautifulsoup4`, `lxml`); dead `openpyxl`/exporter removed.
- [x] **Versioning** — actor `version 1.0`; CHANGELOG v0.1 → v1.0; repo tagged `v1.0.0`.

## Business
- [x] **Positioning** — outcome-first store title/description; buyer segments named (PR / influencer / recruiting).
- [x] **Pricing** — pay-per-lead (`LEAD_DISCOVERED` $0.00030); worked example ($0.08 / 100 leads) in README.
- [x] **Customer value** — discovery + qualification + clean export; pay only for reachable leads.
- [x] **Documentation** — README (problem/solution/install/config/example/pricing/ethics/troubleshooting), CHANGELOG, RELEASE_NOTES, architecture + product docs, examples, sample output, demo package.

## Operations
- [x] **GitHub** — `gsrtech100-wq/pulseleads` created, licensed (MIT), clean initial commit, pushed and tagged `v1.0.0`.
- [x] **Apify publication** — Actor `pure_matai~substack-outreach-leads` (`cHrRkLWSrR8QKYhH8`) pushed to **build `1.0.1`**, set **`isPublic=true`**, store title/SEO/categories set via API (`DEVELOPER_TOOLS, AI, NEWS`). Public URL: `https://console.apify.com/actors/cHrRkLWSrR8QKYhH8`.
- [x] **Verification run (seed)** — Run `cxSGgYvFyYBb5JnUu` (seed `lenny.substack.com`) → SUCCEEDED, exit 0, **4 leads** (Lenny Rachitsky, Claire Vo, Kiyani, Noam Segal).
- [x] **Verification run (keyword)** — Run `uTmYYLL9VQFIC744V` / `3TNF6QW3fV54jfdWz` SUCCEEDED but DuckDuckGo returned `202 Accepted` (intermittent external bot-blocking) → 0 sources. Seed-URL path is the reliable verification.
- [⚠] **Billing (PPE pricing)** — `LEAD_DISCOVERED` charge code is in place, but the Apify Update Actor API returns `internal-server-error` on every `pricingInfos` write (8+ payload variants attempted). **Manual Console (Monetization) enablement required** (platform defect, not a schema rejection).
- [x] **Release notes** — `RELEASE_NOTES.md` complete (what's new / benefits / limitations / known issues / roadmap).

## Verification
- [x] **Production run** — Run `cxSGgYvFyYBb5JnUu`: status SUCCEEDED, 4 leads from `lenny.substack.com`. (Earlier `tcgSwbc5txajohDPs`: 2 leads.)
- [x] **Dataset validation** — 4 rows, correct shape (`hasEmail`, `twitter`, `linkedin`, `website`, `relevanceScore`, `qualified`, `contactReady`); see `sample_output/run_cxSGgYvFyYBb5JnUu.json`.
- [x] **Log validation** — proxy/runtime correct; customer-friendly "no billable leads" message fired as designed.
- [⚠] **Billing verification** — `chargedEventCounts.LEAD_DISCOVERED` cannot be captured until PPE pricing is enabled in the Console (API blocked). Charge will register once enabled; re-run (seed URL with contact-ready authors) to capture the charge.
