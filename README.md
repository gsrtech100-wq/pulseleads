# PulseLeads — Substack Outreach Lead Generator

**Stop scrolling Substack for people to pitch. Type a topic, get a ranked list of relevant writers with their public email and socials — ready to reach out for PR, partnerships, influencer, or recruiting.**

PulseLeads turns a keyword or a list of Substack publications into an **outreach lead list**: the right authors and publications in your niche, with their **public contact info** (when published) and a **topic-fit score** — ready to drop into your outreach.

> **Ethical use:** only public Substack data is used. Use the output only for lawful outreach, honor opt-outs, and comply with applicable privacy law (e.g. GDPR). We never invent contact data.

---

## Customer problem

PR agencies, marketers, recruiters, and partnership teams need to reach relevant writers — but discovering and qualifying them on Substack is manual, slow, and the contacts are scattered across profiles.

## Customer solution

1. **You provide** a topic (e.g. `AI`, `finance`, `health`) **or** paste known Substack URLs.
2. **PulseLeads discovers** relevant Substack publications (search index + seed URLs).
3. **It extracts** the authors, their public email / socials, and a topic-fit score.
4. **You export** a clean, contact-ready lead list (CSV / JSON) and pay only for leads that include a public contact.

---

## Installation

```bash
# from this repository
apify login            # uses the token stored by the Apify CLI
apify push            # builds and uploads the Actor to your Apify account
```

The Actor is also available on the Apify Store as **`pure_matai~substack-outreach-leads`**.

## Configuration

All configuration is via the Actor input (no code changes). Key fields:

| Field | Default | What it does |
|---|---|---|
| `keywords` | _(empty)_ | Topics to discover Substack publications for. Leave empty to use `newsletterUrls`. |
| `newsletterUrls` | _(empty)_ | Known Substack URLs to skip discovery. |
| `maxAuthors` | `10` | Max authors collected per publication. |
| `minRelevance` | `0.3` | Topic-fit threshold (0 = loose, 1 = exact). Leads below are flagged `qualified:false`. |
| `includeContact` | `true` | Only bill for leads that have a public contact. |
| `proxy` | Apify proxy on | **Required** — Substack blocks datacenter IPs. |

## Example workflow

```json
{
  "keywords": ["AI", "finance"],
  "maxAuthors": 10,
  "minRelevance": 0.3,
  "includeContact": true,
  "proxy": { "useApifyProxy": true }
}
```

See [`examples/input_example.json`](examples/input_example.json) for a ready-to-run input.

## Output

Each lead in the dataset contains:

`authorName`, `authorBio`, `publicEmail`, `hasEmail`, `twitter`, `linkedin`, `website`,
`sourceName`, `sourceUrl`, `audienceSize`, `relevanceScore`, `qualified`, `contactReady`.

A **"Contact-Ready Leads"** dataset view shows only rows with an email or social.
See [`sample_output/`](sample_output/) for a real production run.

## Pricing

- **Pay per reachable lead:** billed via the `LEAD_DISCOVERED` event **only** for leads that are
  qualified **and** have a public contact. You pay for leads you can actually reach, not raw rows.
- Apify also adds a small per-run start fee and per-dataset-item fee.
- **Example:** 100 writers with contact ≈ **$0.08**.

> Pay-per-event pricing is enabled in the Apify Console (Monetization) for the published Actor.
> Intended events: `apify-actor-start` $0.00005, `apify-default-dataset-item` $0.00050,
> `LEAD_DISCOVERED` $0.00030.

## Architecture

See [`docs/architecture.md`](docs/architecture.md). The product uses a frozen connector
architecture: `SEARCH → CONNECTOR → ENRICHMENT → QUALIFICATION → EXPORT`. Substack is
**Connector #1** (fully implemented); Medium, GitHub, YouTube, and blogs are documented
extension points that require no core changes.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `No Substack sources were discovered` | Keyword returned no `*.substack.com` results | Use broader keywords or paste `newsletterUrls`. |
| `Found N source(s) but collected 0 author profiles` | Publication has no visible authors / was blocked | Try a larger publication (e.g. `https://lenny.substack.com`). |
| `0 are billable (no public contact found)` | Authors don't publish public contact | Broaden keywords, or set `includeContact=false` to get the full list. |
| Run fails immediately | Proxy not enabled | Ensure `proxy.useApifyProxy = true`. |
| Empty dataset | No input provided | Provide `keywords` or `newsletterUrls`. |

## Honesty / limitations

- Discovery via keyword uses a search index (DuckDuckGo in MVP). For production volume, wire a
  paid search provider (SerpAPI / Bing) — a documented extension point.
- Authors who don't publish a public email are still returned, flagged `contactReady:false`.
  We never invent contact data.
- `audienceSize` is often unavailable from public Substack APIs and may be `null`.
