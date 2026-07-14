import re

from ..pipeline.connector import SourceConnector, ConnectorRegistry
from ..fetcher import SubstackFetcher
from ..parser import parse_publication
from ..entities import Profile

_SOCIAL_KEYS = ["twitter", "facebook", "instagram", "linkedin", "website",
               "youtube", "tiktok", "mastodon", "social_links"]
_URL = re.compile(r'https?://[^\s)<>"\']+', re.I)
_EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
_HANDLE = re.compile(r'(?<!\w)@([A-Za-z0-9_]{1,20})')


@ConnectorRegistry.register
class SubstackConnector(SourceConnector):
    """Connector #1 — reuses StackPulse's proven SubstackFetcher (RSS + author API + robots + proxy + retry)."""
    platform = "substack"

    def fetch_profiles(self, ref, limit: int, client) -> list[Profile]:
        domain = ref.identifier
        fetcher = SubstackFetcher(client)

        pub = fetcher.fetch_publication(domain)
        pub_info = parse_publication(pub, domain)

        rss_items = fetcher.fetch_rss(domain)
        profiles: list[Profile] = []
        seen: set = set()

        for item in rss_items[:limit]:
            post_id = item.get("post_id")
            author_data: dict = {}
            aid = None
            if post_id:
                post_json = fetcher.fetch_post(domain, post_id)
                post_data = post_json.get("post", post_json) if isinstance(post_json, dict) else {}
                bylines = post_data.get("publishedBylines") or []
                if isinstance(bylines, list) and bylines:
                    aid = bylines[0].get("id")
                elif isinstance(post_data.get("author"), dict):
                    aid = post_data["author"].get("id")
                if aid:
                    author_data = fetcher.fetch_author(domain, aid)

            prof = author_data.get("author", author_data) if author_data else {}
            name = prof.get("name") or item.get("author_name")
            if not name:
                continue
            key = (name, aid)
            if key in seen:
                continue
            seen.add(key)

            socials, bio_email = self._socials(prof, prof.get("bio"), domain)
            public_email = prof.get("public_email") or prof.get("email") or bio_email
            profiles.append(Profile(
                platform="substack",
                source_id=domain,
                name=name,
                bio=prof.get("bio"),
                avatar=prof.get("photo_url") or prof.get("avatar_url"),
                public_email=public_email,
                socials=socials,
                audience_size=pub_info.get("subscriber_count"),
                source_name=pub_info.get("name"),
                source_url=pub_info.get("url"),
                raw=author_data,
            ))
            if len(profiles) >= limit:
                break
        return profiles

    @staticmethod
    def _socials(prof: dict, bio=None, domain: str = "") -> tuple:
        out: dict = {}
        for k in _SOCIAL_KEYS:
            v = prof.get(k)
            if not v:
                continue
            if k == "social_links" and isinstance(v, list):
                for link in v:
                    if isinstance(link, dict) and link.get("url"):
                        out[link.get("type", "link")] = link["url"]
                    elif isinstance(link, str):
                        out.setdefault("link", link)
            elif isinstance(v, str):
                out[k] = v
        text = " ".join([str(bio or ""), str(prof.get("bio") or "")])
        email = None
        if text:
            for um in _URL.finditer(text):
                u = um.group(0).rstrip('.,);')
                lu = u.lower()
                if "twitter.com" in lu or "x.com" in lu:
                    if "twitter" not in out:
                        out["twitter"] = u
                elif "linkedin.com" in lu:
                    if "linkedin" not in out:
                        out["linkedin"] = u
                elif "substack.com" in lu:
                    continue
                else:
                    if "website" not in out:
                        out["website"] = u
            em = _EMAIL.search(text)
            if em:
                e = em.group(0)
                if not e.lower().endswith("@substack.com") and domain not in e.lower():
                    email = e
            if "twitter" not in out:
                hm = _HANDLE.search(text)
                if hm and hm.group(1).lower() not in ("substack", "note", "writers", "read"):
                    out["twitter"] = "https://twitter.com/" + hm.group(1)
        return out, email
