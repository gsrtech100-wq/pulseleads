# Changelog

All notable changes to AZ PulseLeads are documented here. This product evolved from
**PPE Product #2 — "Substack Author Profile Extractor"** through customer discovery, business
redesign, and evidence validation into the commercial product described in this repository.
Branding follows the AZULGANZES TECHNOLOGIES Product Factory standard (AZ StackPulse, AZ PulseLeads).

## v0.1 — Concept
- Originated as PPE Product #2: a Substack author-profile extractor (data export tool).

## v0.5 — Architecture
- Frozen **Product Factory Connector Architecture** (`SEARCH → CONNECTOR → ENRICHMENT →
  QUALIFICATION → EXPORT`).
- Substack selected as **Connector #1** (reuses the proven AZ StackPulse `SubstackFetcher`).
- Other platforms (Medium, GitHub, YouTube, blogs) defined as extension points.

## v0.9 — MVP
- Implemented Substack-only MVP on the frozen architecture.
- DuckDuckGo keyword discovery + seed-URL mode.
- Qualification service (relevance scoring, configurable rules).
- `LEAD_DISCOVERED` pay-per-event billing hook.
- 7 offline tests passing; modules import cleanly.

## v1.0 — First Public Release
- **Branding:** renamed to **AZ PulseLeads**; official AZ logo / product lockup applied across
  Apify, GitHub, README, release notes, changelog, and architecture docs.
- **Customer Experience Review** applied: rewrote store title/description (outcome-first,
  proxy-handled, ethical-use line); dropped the misleading "contact-ready" over-promise.
- **Clean dataset/output handling:** split `socials` into `twitter` / `linkedin` / `website`
  columns + `hasEmail`; added a "Contact-Ready Leads" dataset view.
- **First-run experience:** input prefill examples + plain-language help.
- **Empty-result guidance:** customer-friendly messages for no sources / no profiles /
  no billable leads, each with "why" + "what to try next".
- **Production verification:** Actor pushed, built, and run on Apify
  (Run `tcgSwbc5txajohDPs`, 2 leads extracted from `lenny.substack.com`).
- Repository organized as a production commercial project (LICENSE, CHANGELOG, RELEASE_NOTES,
  architecture doc, examples, sample output, demo package).
