import asyncio
import logging
import os
import sys
from collections import defaultdict

import httpx
from apify import Actor

from . import connectors  # triggers connector registration (Substack + stubs)
from .pipeline.connector import ConnectorRegistry
from .pipeline.search import DuckDuckGoProvider
from .pipeline.qualification import QualificationService
from .pipeline.export import ExportService
from .entities import SourceRef
from .utils import normalize_url, extract_domain, is_substack_url

logger = logging.getLogger(__name__)

_RULES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "qualification_rules.json")


async def main():
    actor_input = await Actor.get_input() or {}
    keywords = actor_input.get("keywords", []) or []
    seed_urls = actor_input.get("newsletterUrls", []) or []
    max_authors = int(actor_input.get("maxAuthors", 10))
    min_relevance = float(actor_input.get("minRelevance", 0.3))
    include_contact = bool(actor_input.get("includeContact", True))
    proxy_config = actor_input.get("proxy", {}) or {}

    if not keywords and not seed_urls:
        Actor.log.warning(
            "Nothing to do: provide 'keywords' (e.g. [\"AI\", \"finance\"]) "
            "or 'newsletterUrls' (e.g. [\"https://lenny.substack.com\"])."
        )
        return

    proxy_url = None
    if proxy_config.get("useApifyProxy"):
        proxy_url = os.environ.get("APIFY_PROXY_URL")

    client_kwargs = {"follow_redirects": True, "timeout": 30.0}
    if proxy_url:
        client_kwargs["proxies"] = proxy_url

    # ── SEARCH stage → SourceRefs ──
    refs: list[SourceRef] = []
    if seed_urls:
        for u in seed_urls:
            if is_substack_url(u):
                refs.append(SourceRef("substack", extract_domain(normalize_url(u))))
            else:
                Actor.log.warning("Skipping non-Substack URL: %s", u)
    else:
        search = DuckDuckGoProvider()
        for kw in keywords:
            refs.extend(search.search(kw, limit=max_authors))
            Actor.log.info("Search '%s' -> %d candidate sources", kw, len(refs))

    if not refs:
        Actor.log.warning(
            "No Substack sources were discovered for your keywords.\n"
            "  Why this can happen:\n"
            "    - The search index returned no *.substack.com results for that term.\n"
            "    - The term may be too narrow or misspelled.\n"
            "  What to try next:\n"
            "    - Use broader or alternative keywords (e.g. 'AI' instead of 'AI governance').\n"
            "    - Or skip discovery and paste known Substack URLs in 'newsletterUrls',\n"
            "      e.g. [\"https://lenny.substack.com\", \"https://www.stratechery.com\"].\n"
            "Run finished with 0 leads."
        )
        return

    by_platform = defaultdict(list)
    for r in refs:
        by_platform[r.platform].append(r)

    # ── CONNECTOR + ENRICHMENT stages ──
    all_profiles = []
    with httpx.Client(**client_kwargs) as client:
        for platform, platform_refs in by_platform.items():
            try:
                connector = ConnectorRegistry.get(platform)
            except KeyError as e:
                Actor.log.warning(str(e))
                continue
            for ref in platform_refs:
                try:
                    profiles = connector.fetch_profiles(ref, max_authors, client)
                    profiles = [connector.enrich_profile(p, client) for p in profiles]
                    all_profiles.extend(profiles)
                    Actor.log.info("Fetched %d profiles from %s", len(profiles), ref.identifier)
                except NotImplementedError:
                    Actor.log.warning("Connector '%s' not implemented (extension point).", platform)
                except Exception as e:
                    Actor.log.warning("Error fetching %s: %s", ref.identifier, e)

    if not all_profiles:
        Actor.log.warning(
            "Found %d source(s) but collected 0 author profiles.\n"
            "  Why this can happen:\n"
            "    - The publication has no recent posts with visible authors, or access was blocked.\n"
            "  What to try next:\n"
            "    - Use a different or larger publication, e.g. [\"https://lenny.substack.com\"].\n"
            "    - Or broaden your keywords to discover more sources.\n"
            "Run finished with 0 leads.", len(refs)
        )
        return

    # ── QUALIFICATION stage ──
    qs = QualificationService(rules_path=_RULES_PATH)
    qs.rules.setdefault("relevance", {})["min_score"] = min_relevance
    leads = qs.score(all_profiles, keywords)

    # ── EXPORT stage ──
    export = ExportService(charge_event="LEAD_DISCOVERED", require_contact=include_contact)
    billed = await export.export(leads)

    if leads and billed == 0:
        Actor.log.warning(
            "Exported %d writer(s), but 0 are billable (no public contact found).\n"
            "  Why: these authors don't publish a public email or social on Substack.\n"
            "  What to try next:\n"
            "    - Use broader keywords to discover more authors.\n"
            "    - Set 'includeContact' = false to receive the full list\n"
            "      (all qualified leads are then billed, contacts or not).", len(leads)
        )
    Actor.log.info(
        "=== RUN SUMMARY ===  sources: %d | writers: %d | billable (contact-ready): %d",
        len(refs), len(leads), billed
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    async def _run() -> None:
        async with Actor:
            await main()

    asyncio.run(_run())
