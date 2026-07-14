# AZ PulseLeads — Release & Demo Notes

## Release status (as of this package)
- **Code:** 7/7 offline tests pass; Actor pushed & built (`0.1.2`).
- **Repo:** `github.com/gsrtech100-wq/pulseleads` (MIT, branded).
- **Branding:** product renamed **AZ PulseLeads**; official AZ logo + product lockup applied
  across Apify, GitHub, README, release notes, changelog, architecture, and this demo package.
- **Production run:** `tcgSwbc5txajohDPs` SUCCEEDED (2 leads from `lenny.substack.com`).
- **Billing (open item):** enable pay-per-event in the Apify Console (Monetization) with
  `LEAD_DISCOVERED` $0.00030, then re-run to capture `chargedEventCounts`. After that, the
  product is fully ready for public release.

## Demo readiness
- `demo_script.md` — 3–5 min talking script.
- `demo_checklist.md` — pre/during/post demo + screenshot capture list.
- `faq.md` — objections & answers.
- `demo_data/` — ready-to-paste input.
- `sample_output/` — real run output + illustrative contact-ready example.
- `screenshots/` — capture guide + textual evidence (live UI PNGs added manually).
- `videos/` — recording notes (record manually per the script).
- `branding/` — official AZ logo (light/dark), official AZ PulseLeads lockups, banner.

## Known demo caveats
- The 10 UI screenshots must be captured from the live Apify Console / GitHub (no browser
  automation in the build environment). Textual evidence (run log, dataset) is included so the
  demo can run even before the PNGs are captured.
- For a live billing screenshot, complete the PPE Console enablement first.
