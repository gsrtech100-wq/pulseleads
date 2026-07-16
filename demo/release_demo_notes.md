# AZ PulseLeads — Release & Demo Notes

## Release status (verified 2026-07-16)
- **Code:** 7/7 offline tests pass in a clean isolated venv; Actor pushed & built (`0.1.3`).
- **Repo:** `github.com/gsrtech100-wq/pulseleads` (MIT, branded).
- **Branding:** product renamed **AZ PulseLeads**; official AZ logo + product lockup applied
  across Apify, GitHub, README, release notes, changelog, architecture, and this demo package.
- **Live verification run:** `jyOzEyQ7ZCpyMacxj` SUCCEEDED (build `0.1.2`→`0.1.3`), 4 leads from
  `lenny.substack.com` (Lenny Rachitsky, Claire Vo, Kiyani, Noam Segal). Reproduces the original
  release evidence exactly — the engine + live deployment both work end-to-end.
- **Billing:** pay-per-event LIVE. `apify actors info` confirms `LEAD_DISCOVERED` $0.00030 armed;
  `apify-actor-start` $0.00005 and result $0.0005 charged on every run.
- **Schema fix (build 0.1.3):** `.actor/actor.json` dataset fields aligned to the real exported
  schema (`sourceId`, `authorAvatarUrl`, `socialLinks`, `audienceScore` now declared).

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
