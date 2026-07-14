![AZ PulseLeads](demo/branding/az_pulseleads_light.png)

# Release Notes — AZ PulseLeads v1.0 (First Public Release)

*An AZULGANZES TECHNOLOGIES product.*

## What's new
AZ PulseLeads is AI-GIT's second commercial product: a Substack outreach lead generator that turns a
topic into a ranked list of relevant writers with their public contact, ready to pitch.

- **Discovery:** keyword (DuckDuckGo) or seed Substack URLs.
- **Connector #1 (Substack):** RSS + author API, robots-respecting, proxy-safe (reuses the
  proven AZ StackPulse engine).
- **Qualification:** configurable topic-fit scoring.
- **Export:** clean lead rows with `hasEmail`, `twitter`, `linkedin`, `website`, plus a
  "Contact-Ready Leads" view.
- **Billing:** pay only for leads that include a public contact (`LEAD_DISCOVERED`).

## Customer benefits
- Find and qualify niche writers in minutes instead of hours of manual scrolling.
- Pay for reachable leads, not raw data.
- Output drops straight into outreach tools (CSV / JSON).

## Limitations
- **Substack only** in this release. Medium / GitHub / YouTube / blogs are documented
  extension points (no core changes required to add them).
- Keyword discovery relies on a public search index (DuckDuckGo MVP); volume users should
  wire a paid search provider (SerpAPI / Bing).
- `audienceSize` is frequently unavailable from public Substack APIs and may be `null`.
- Authors without a published public contact are returned flagged `contactReady:false`.

## Known issues
- **Pay-per-event pricing is set manually in the Apify Console (Monetization).** The Apify Update
  Actor API returns `internal-server-error` on every `pricingInfos` write (attempted: FREE,
  PAY_PER_EVENT, minimal, with timestamps, while private, and via the version endpoint) — a
  platform defect in the pricing-change notification path, not a schema rejection. This is a
  one-time manual enablement: add events `apify-actor-start` $0.00005,
  `apify-default-dataset-item` $0.00050, `LEAD_DISCOVERED` $0.00030. The `LEAD_DISCOVERED` charge
  code is in place and fires on every contact-ready lead once PPE is enabled.
- **Keyword discovery depends on DuckDuckGo** (MVP). It intermittently returns `202 Accepted`
  (bot challenge) instead of `200`, yielding 0 sources. Seed `newsletterUrls` always work and are
  the reliable path; volume users should wire SerpAPI/Bing for guaranteed discovery volume.

## Future roadmap
- Production search providers (SerpAPI / Bing) for higher discovery volume.
- Additional connectors (Medium, GitHub, YouTube, blogs).
- Recruiter / PR preset views and CSV enrichment.
- Subscription mode for recurring weekly discovery.
