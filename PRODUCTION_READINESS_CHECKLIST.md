# AZ PulseLeads — Production Readiness Checklist

Status: ✅ Code / Docs / Repo / Run verified. ⚠ One manual step (Console PPE enablement) before public billing goes live.

## Engineering
- [x] **Tests** — 7 offline tests pass (`pytest tests -q`); modules import cleanly.
- [x] **Build** — `apify push` succeeded; build `0.1.1`, image built and pushed.
- [x] **Docker** — `FROM apify/actor-python:3.12`, pinned deps, `CMD python -m src.main`.
- [x] **Dependencies** — `requirements.txt` pinned (`apify==3.4.1`, `httpx`, `beautifulsoup4`, `lxml`); dead `openpyxl`/exporter removed.
- [x] **Versioning** — actor `version 0.1`; CHANGELOG v0.1 → v1.0; repo tagged via commit.

## Business
- [x] **Positioning** — outcome-first store title/description; buyer segments named (PR / influencer / recruiting).
- [x] **Pricing** — pay-per-lead (`LEAD_DISCOVERED` $0.00030); worked example ($0.08 / 100 leads) in README.
- [x] **Customer value** — discovery + qualification + clean export; pay only for reachable leads.
- [x] **Documentation** — README (problem/solution/install/config/example/pricing/ethics/troubleshooting), CHANGELOG, RELEASE_NOTES, architecture + product docs, examples, sample output.

## Operations
- [x] **GitHub** — `gsrtech100-wq/pulseleads` created, licensed (MIT), clean initial commit, push verified.
- [x] **Apify** — Actor `pure_matai~substack-outreach-leads` pushed, built, run verified (Run `tcgSwbc5txajohDPs`).
- [⚠] **Billing** — `LEAD_DISCOVERED` charge code in place; **PPE must be enabled in the Apify Console (Monetization)** because the actor-PUT API on the build account rejects pricing fields. One manual step before public billing.
- [x] **Release notes** — `RELEASE_NOTES.md` complete (what's new / benefits / limitations / known issues / roadmap).

## Verification
- [x] **Production run** — Run `tcgSwbc5txajohDPs`, status SUCCEEDED, 2 leads extracted from `lenny.substack.com`.
- [x] **Dataset validation** — 2 rows, correct shape (`hasEmail`, `twitter`, `linkedin`, `website`, `relevanceScore`, `qualified`, `contactReady`); see `sample_output/run_tcgSwbc5txajohDPs.json`.
- [x] **Log validation** — proxy/runtime correct; customer-friendly "no billable leads" message fired as designed.
- [⚠] **Billing verification** — `chargedEventCounts` is null because PPE is not yet enabled (API restriction). Charge will register once Console PPE is enabled; re-run to capture `chargedEventCounts.LEAD_DISCOVERED > 0`.
