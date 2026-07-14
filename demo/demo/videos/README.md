# AZ PulseLeads — Demo Video

**Target length:** 3–5 minutes. **Record manually** using the script in `demo_script.md`
(no browser/screen automation in the build environment).

## Shot list (maps to `demo_script.md`)
1. (0:00–0:30) Customer problem — manual Substack discovery pain.
2. (0:30–1:00) AZ PulseLeads intro — show `branding/az_pulseleads_banner.png`.
3. (1:00–1:45) Workflow — architecture diagram (`docs/architecture.md` / `screenshots/architecture.png`).
4. (1:45–3:15) Live execution — paste `demo_data/demo_input.json`, run, show log + RUN SUMMARY.
5. (3:15–4:00) Output — dataset table + "Contact-Ready Leads" view.
6. (4:00–4:30) Customer value — minutes vs hours; pay for reachable leads.
7. (4:30–5:00) Pricing — per-lead cost; closing summary.

## Recording tips
- Keep the Apify Console and a text editor with `demo_input.json` side by side.
- If showing billing live, enable PPE in the Console first and capture `chargedEventCounts`.
- Export the final clip to `demo/videos/az_pulseleads_demo.mp4`.

## Assets to show on screen
- `branding/az_pulseleads_banner.png`
- `docs/architecture.md`
- `demo_data/demo_input.json`
- Live Apify run + dataset
