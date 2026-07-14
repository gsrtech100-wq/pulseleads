# AZ PulseLeads — Demo Script (3–5 minutes)

*Self-contained demo package. Reuse for customer meetings, website showcases, conferences, training.*

**Goal:** show a buyer (PR agency / marketer / recruiter) how AZ PulseLeads turns a topic into a
ranked, contact-ready Substack lead list they can pitch today.

---

## 0. Setup (before you start, 1 min)
- Open the Apify Store page for `pure_matai~substack-outreach-leads` (or your Actor console).
- Have `demo_data/demo_input.json` ready to paste.
- Have this script + `demo_checklist.md` open.

## 1. Customer problem (30s)
- "Finding and qualifying niche writers on Substack is manual and slow. Contacts are scattered."
- "You end up scrolling for hours and still don't know who to email."

## 2. AZ PulseLeads (30s)
- Show the logo/banner (`demo/branding/az_pulseleads_banner.png`).
- "AZ PulseLeads turns a topic into a ranked list of relevant writers with their public email
  and socials — ready to pitch. You pay only for leads that include a public contact."

## 3. Product workflow (45s)
- Point at the architecture diagram (`docs/architecture.md` / `demo/screenshots/architecture.png`):
  `SEARCH → CONNECTOR → ENRICHMENT → QUALIFICATION → EXPORT`.
- Substack is Connector #1 (reuses the proven AZ StackPulse engine); other platforms are
  documented extension points.

## 4. Live execution (90s)
- Paste `demo_data/demo_input.json` (keywords `["AI","finance"]`, proxy on).
- Run. Show the run log (`demo/screenshots/running_actor.png`) — proxy/runtime, RSS fetch,
  "RUN SUMMARY".
- Reference the verified production run `tcgSwbc5txajohDPs` (2 leads from `lenny.substack.com`).

## 5. Output (45s)
- Open the dataset (`demo/screenshots/output_dataset.png`): columns `authorName`, `hasEmail`,
  `twitter`, `linkedin`, `website`, `relevanceScore`, `contactReady`.
- Switch to the **"Contact-Ready Leads"** view (`demo/screenshots/qualified_leads.png`).

## 6. Customer value (30s)
- "Minutes instead of hours. Pay for reachable leads, not raw rows. Drops into your outreach tool."

## 7. Pricing (30s)
- "Per reachable lead via `LEAD_DISCOVERED` (~$0.08 per 100 writers with contact). Start and
  dataset-item fees are tiny."

## 8. Closing summary (20s)
- "AZ PulseLeads — find, qualify, and reach the right Substack writers. Let's set up a trial."

---

## Talking points / objections (see `faq.md`)
- "Where are the emails?" → we return public emails when authors publish them; others flagged
  `contactReady:false`; we never invent data.
- "Only Substack?" → MVP; Medium/GitHub/YouTube/blog connectors are extension points.
- "Is this allowed?" → public data only, lawful outreach, opt-out honored (ethical-use line).
