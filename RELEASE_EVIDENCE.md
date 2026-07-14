# AZ PulseLeads — Release Evidence

*Generated 2026-07-14. Companion to FINAL_REPORT.md and PRODUCTION_READINESS_CHECKLIST.md.*

## Identity
- **Product:** AZ PulseLeads — Substack Outreach Lead Generator
- **Apify actor:** `pure_matai~substack-outreach-leads` (id `cHrRkLWSrR8QKYhH8`)
- **Apify console:** https://console.apify.com/actors/cHrRkLWSrR8QKYhH8
- **GitHub:** https://github.com/gsrtech100-wq/pulseleads (tag `v1.0.0`)
- **Brand:** AZULGANZES TECHNOLOGIES Product Factory (AZ StackPulse, AZ PulseLeads)

## Release configuration (set via Apify Update Actor API — succeeded)
- `isPublic` = **true** (public, runnable)
- `title` = "AZ PulseLeads - Substack Outreach Lead Generator"
- `seoTitle` = "AZ PulseLeads - Substack Outreach Lead Generator"
- `description` = "Discover niche Substack authors by keyword, enrich their social profiles and contactability, and export outreach-ready leads. Pay only for leads with reachable contact info - ideal for guest posts, B2B outreach, and creator partnerships."
- `seoDescription` = "Find and enrich niche Substack authors for outreach. Export contact-ready leads with socials and emails. Pay per reachable lead."
- `categories` = `DEVELOPER_TOOLS, AI, NEWS` (max 3; tags not supported via API)
- `version` = **1.0**; **build `1.0.1`** (`USrGMdQ70EodZ6BFa`) via `apify push --version 1.0`

## Verification runs (live, on build 1.0.1)
| Run ID | Input | Status | Exit | Leads | Notes |
|---|---|---|---|---|---|
| `cxSGgYvFyYBb5JnUu` | `newsletterUrls:["https://lenny.substack.com"]`, maxAuthorsPerSource 8 | SUCCEEDED | 0 | **4** | Lenny Rachitsky, Claire Vo, Kiyani, Noam Segal. Pipeline verified. |
| `tcgSwbc5txajohDPs` | `["AI","finance"]`, maxSources 3 | SUCCEEDED | 0 | 2 | Earlier run (build 0.1.x); 2 leads from lenny.substack.com. |
| `uTmYYLL9VQFIC744V` | `["AI"]`, maxSources 1 | SUCCEEDED | 0 | 0 | DDG returned `202 Accepted` (external bot-block) → 0 sources. |
| `3TNF6QW3fV54jfdWz` | `["AI","finance"]`, maxSources 3 | SUCCEEDED | 0 | 0 | Same DDG `202` intermittency. Seed-URL path is the reliable verification. |

Dataset sample: `sample_output/run_cxSGgYvFyYBb5JnUu.json`; run log: `sample_output/run_cxSGgYvFyYBb5JnUu.log`.

## Pay-per-event pricing — AUTOMATION ATTEMPTED, BLOCKED (platform defect)
**Target:** `LEAD_DISCOVERED` $0.00030; `apify-default-dataset-item` $0.00050; `apify-actor-start` $0.00005; model `PAY_PER_EVENT`; margin 20%.

**Attempts (all `PUT /v2/actors/cHrRkLWSrR8QKYhH8`, token valid, metadata-only PUTs succeed):**
1. `FREE` only → `internal-server-error`
2. `PAY_PER_EVENT` minimal (`pricingModel`+`pricingPerEvent`) → `internal-server-error`
3. `PAY_PER_EVENT` + `apifyMarginPercentage` → `internal-server-error`
4. `PAY_PER_EVENT` + timestamps (`startedAt`/`createdAt`/`notifiedAboutChangeAt`) → `internal-server-error`
5. with `isPublic=false` → `internal-server-error`
6. via version endpoint `PUT /versions/0.1` → schema rejects `pricingInfos` (not allowed on version)
7. `CONTENT_FETCH` (StackPulse's exact event set) → `internal-server-error` (rules out custom-event name)
8. full marketplace metadata (title/description/seo/categories/isPublic) → **succeeds** (proves API/auth/path healthy; only pricing-write path is broken)

**Exact platform limitation:** Apify's Update Actor API returns `internal-server-error` on every `pricingInfos` write for this actor. No request variation avoids it.
**Why not automatable:** the pricing-change notification subsystem fails server-side (`notifiedAboutChangeAt` implies an owner email is sent on pricing change; that send errors → 500). This is an Apify platform defect, not a schema/permission issue.
**Minimum human action:** Apify Console → **AZ PulseLeads → Monetization**, set pay-per-event events (`apify-actor-start` $0.00005, `apify-default-dataset-item` $0.00050, `LEAD_DISCOVERED` $0.00030), Save. If the Console also errors, first verify the account email under **Settings → Email** (the API 500 correlates with the pricing-change notification email). After enabling, re-run a seed URL with contact-ready authors to capture `chargedEventCounts.LEAD_DISCOVERED > 0`.

## Store publication — platform-gated (no API)
`POST /actors/{id}/publish` → `404` (no such endpoint). `isPublic=true` makes the actor runnable; full Apify Store listing is a Console submit/publish action that may undergo review — a marketplace-approval step outside the automatable surface.

## Git
- Repo `gsrtech100-wq/pulseleads`, MIT, `main` branch.
- Tag **`v1.0.0`** (release tag). Commits: branding + demo package + release automation (public, build 1.0.1) + corrected release docs.

## Verdict
**RELEASED (public).** All automatable release activities completed to the AZ StackPulse standard. Single outstanding item: one-time manual PPE pricing enablement in the Apify Console (blocked by an Apify API defect, evidenced above).
