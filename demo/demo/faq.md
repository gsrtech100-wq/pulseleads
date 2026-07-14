# AZ PulseLeads — FAQ

**Q: What is AZ PulseLeads?**
A: An AZULGANZES TECHNOLOGIES product that turns a topic (or known Substack URLs) into a ranked
list of relevant Substack writers with their public contact — ready to pitch.

**Q: Where do the emails come from?**
A: Only from public Substack profile data. If an author doesn't publish a public email, the lead
is returned flagged `contactReady:false`. We never invent or guess contact data.

**Q: Why is a lead "qualified" but have no email?**
A: "Qualified" means it passed the topic-fit threshold (keyword match in name/bio/source).
"Contact-ready" means it also has a public email or social. You can set `includeContact=false`
to receive the full list.

**Q: Is this only for Substack?**
A: The MVP is Substack-only (Connector #1). Medium, GitHub, YouTube, and generic blogs are
documented extension points that require no core changes.

**Q: How does discovery work if Substack has no keyword API?**
A: AZ PulseLeads uses a search index (DuckDuckGo in MVP) to find relevant `*.substack.com`
domains, then reads each publication's RSS + author API (via Apify proxy). For production volume,
wire a paid search provider (SerpAPI / Bing) — an extension point.

**Q: Is this legal / allowed?**
A: It uses only public Substack data, for lawful outreach with opt-out honoring, per the
ethical-use commitment. Always comply with applicable privacy law (e.g. GDPR).

**Q: How much does it cost?**
A: Pay per reachable lead via `LEAD_DISCOVERED` (~$0.08 per 100 writers with contact). Small
per-run start and per-dataset-item fees also apply.

**Q: What if I get no results?**
A: The Actor prints a clear message with reasons and next steps (broader keywords, paste known
URLs, try a larger publication). See Troubleshooting in the README.

**Q: Who built it?**
A: AI-GIT's Product Factory. It evolved from PPE Product #2 via customer discovery, business
redesign, and evidence validation. The Substack connector reuses the proven AZ StackPulse engine.
