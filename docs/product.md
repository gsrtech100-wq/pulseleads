# PulseLeads — Product Record (Traceability)

This document preserves the evolution of AI-GIT's second commercial product for audit and
governance. It is immutable history — do not rewrite; append corrections as new entries.

## Lineage

```
PPE Product #2  "Substack Author Profile Extractor"   (original concept: data export tool)
        │
        ▼  Customer Discovery
   PR agencies / marketers / recruiters want REACHABLE writers to PITCH,
   not raw profile dumps. "Leads I can email" > "profiles I can read".
        │
        ▼  Business Redesign (HY3)
   Re-positioned as PulseLeads — a qualified-outreach-lead solution.
   Discovery = search-index + seed-URL hybrid (NOT Substack-native API, which is closed).
   Revenue = LEAD_DISCOVERED (pay for qualified, contact-ready leads).
        │
        ▼  Evidence Validation
   Proved Substack has no keyword API (403/404 on /api/v1/publication, /search, /discover).
   RSS + author API work from an Apify proxy; search-engine discovery (DDG) returns
   relevant substack domains. Option B (workflow change) chosen: buildable.
        │
        ▼  Final Commercial Product
   PulseLeads — Substack Outreach Lead Generator (Substack-only MVP on the frozen
   Connector Architecture). Apify Actor: pure_matai~substack-outreach-leads.
```

## Guardrail compliance

- Portfolio: Product #2 in the recommended 3-product sequence (Apify tactical → AutomationMart
  GST n8n → AutomationWorkflows.io n8n), keeping marketplace dependency within limits.
- Every 3rd product introduces a new marketplace/segment/revenue model (per PSR rules).

## Evidence artifacts

- `design/PRODUCT_FACTORY_CONNECTOR_ARCHITECTURE.md` — frozen architecture (v1.0).
- `operations/EVIDENCE_BASED_BACKLOG.md` — evidence-based backlog (items E1–E4, S1–S5, C1–C3).
- Production run `tcgSwbc5txajohDPs` — 2 leads extracted from `lenny.substack.com`
  (see `sample_output/`).
- `RELEASE_NOTES.md` — public release notes.
- `CHANGELOG.md` — release history.
