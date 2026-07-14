from abc import ABC, abstractmethod

from ..entities import SourceRef


class SearchProvider(ABC):
    """Frozen search contract. Maps a keyword to candidate SourceRefs."""

    @abstractmethod
    def search(self, query: str, limit: int = 20, client=None) -> list[SourceRef]:
        ...


class DuckDuckGoProvider(SearchProvider):
    """MVP search provider (free, proven concept, low volume).

    Queries DuckDuckGo HTML and extracts *.substack.com domains.
    Production should prefer SerpApiProvider / BingProvider (extension points).
    """
    _ENDPOINT = "https://html.duckduckgo.com/html/"

    def search(self, query: str, limit: int = 20, client=None) -> list[SourceRef]:
        import re
        import httpx

        q = f"{query} substack"
        own = client or httpx.Client(follow_redirects=True, timeout=20.0)
        close = client is None
        refs: list[SourceRef] = []
        seen = set()
        try:
            resp = own.get(self._ENDPOINT, params={"q": q})
            resp.raise_for_status()
            for dom in re.findall(r"([a-z0-9\-]+\.substack\.com)", resp.text):
                if dom in seen:
                    continue
                seen.add(dom)
                refs.append(SourceRef(platform="substack", identifier=dom))
                if len(refs) >= limit:
                    break
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning("DuckDuckGo search failed: %s", exc)
        finally:
            if close:
                own.close()
        return refs


# ── Documented extension points (NOT implemented in MVP) ──────────────────────

class SerpApiProvider(SearchProvider):
    def search(self, query: str, limit: int = 20, client=None) -> list[SourceRef]:
        raise NotImplementedError(
            "Extension point: wire SERPAPI_KEY and map results to SourceRefs."
        )


class BingProvider(SearchProvider):
    def search(self, query: str, limit: int = 20, client=None) -> list[SourceRef]:
        raise NotImplementedError(
            "Extension point: wire Bing Web Search API and map results to SourceRefs."
        )
