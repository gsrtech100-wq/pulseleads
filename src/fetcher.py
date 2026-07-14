import logging
import time
from typing import Optional
from xml.etree import ElementTree

import httpx

from .utils import rss_url, publication_api_url, post_api_url, robots_txt_url

logger = logging.getLogger(__name__)


class SubstackFetcher:
    TIMEOUT = 30.0

    def __init__(self, client: httpx.Client):
        self.client = client
        self._robots_cache: dict[str, list[str]] = {}
        self._rss_cache: dict[str, str] = {}

    def check_robots_txt(self, domain: str, path: str) -> bool:
        if domain not in self._robots_cache:
            try:
                url = robots_txt_url(domain)
                resp = self.client.get(url, timeout=10.0)
                if resp.status_code == 200:
                    disallowed = []
                    for line in resp.text.splitlines():
                        line = line.strip()
                        if line.lower().startswith('disallow'):
                            parts = line.split(':', 1)
                            if len(parts) == 2:
                                disallowed.append(parts[1].strip().rstrip('/'))
                    self._robots_cache[domain] = disallowed
                else:
                    self._robots_cache[domain] = []
            except Exception:
                self._robots_cache[domain] = []
        for d in self._robots_cache[domain]:
            if d and path.startswith(d):
                logger.warning("robots.txt disallows %s on %s", path, domain)
                return False
        return True

    def _request(self, url: str, max_retries: int = 2) -> httpx.Response:
        for attempt in range(max_retries + 1):
            resp = self.client.get(url, timeout=self.TIMEOUT)
            if resp.status_code == 429 and attempt < max_retries:
                logger.warning("Rate limited on %s, retrying after 2s", url)
                time.sleep(2.0)
                continue
            return resp
        return resp

    def fetch_publication(self, domain: str) -> dict:
        path = '/api/v1/publication'
        if not self.check_robots_txt(domain, path):
            return self._pub_from_rss(domain)
        url = publication_api_url(domain)
        try:
            resp = self._request(url)
            if resp.status_code == 403:
                logger.info("Publication API blocked for %s, falling back to RSS metadata", domain)
                return self._pub_from_rss(domain)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.warning("Failed to fetch publication info for %s: %s — falling back to RSS", domain, exc)
            return self._pub_from_rss(domain)

    def _pub_from_rss(self, domain: str) -> dict:
        rss_text = self._rss_cache.get(domain)
        if rss_text is None:
            return self.fetch_publication_from_rss(domain)
        return self._extract_pub_from_rss_text(rss_text, domain)

    def fetch_rss(self, domain: str) -> list[dict]:
        path = '/feed'
        if not self.check_robots_txt(domain, path):
            return []
        url = rss_url(domain)
        try:
            resp = self._request(url)
            resp.raise_for_status()
            self._rss_cache[domain] = resp.text
            return self._parse_rss(resp.text, domain)
        except Exception as exc:
            logger.warning("Failed to fetch RSS for %s: %s", domain, exc)
            return []

    def fetch_post(self, domain: str, post_id: str) -> dict:
        path = f'/api/v1/posts/{post_id}'
        if not self.check_robots_txt(domain, path):
            return {}
        url = post_api_url(domain, post_id)
        try:
            resp = self._request(url)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, dict) else {}
        except Exception as exc:
            logger.warning("Failed to fetch post %s for %s: %s", post_id, domain, exc)
            return {}

    def fetch_author(self, domain: str, author_id: str) -> dict:
        path = f'/api/v1/author/{author_id}'
        if not self.check_robots_txt(domain, path):
            return {}
        url = f'https://{domain}/api/v1/author/{author_id}'
        try:
            resp = self._request(url)
            resp.raise_for_status()
            data = resp.json()
            return data if isinstance(data, dict) else {}
        except Exception as exc:
            logger.debug("Failed to fetch author %s for %s: %s", author_id, domain, exc)
            return {}

    def _parse_rss(self, xml_text: str, domain: str) -> list[dict]:
        items = []
        try:
            root = ElementTree.fromstring(xml_text)
            dc_ns = 'http://purl.org/dc/elements/1.1/'
            channel = root.find('channel')
            if channel is None:
                return items
            for item_el in channel.findall('item'):
                post = {}
                title_el = item_el.find('title')
                post['title'] = title_el.text if title_el is not None and title_el.text else ''
                link_el = item_el.find('link')
                post['url'] = link_el.text.strip() if link_el is not None and link_el.text else ''
                guid_el = item_el.find('guid')
                guid = guid_el.text.strip() if guid_el is not None and guid_el.text else ''
                post['guid'] = guid
                post['post_id'] = guid.rsplit('/', 1)[-1] if '/' in guid else guid
                pub_date_el = item_el.find('pubDate')
                if pub_date_el is not None and pub_date_el.text:
                    from email.utils import parsedate_to_datetime
                    post['published_at'] = parsedate_to_datetime(pub_date_el.text).isoformat()
                else:
                    post['published_at'] = ''
                creator_el = item_el.find(f'{{{dc_ns}}}creator')
                post['author_name'] = creator_el.text if creator_el is not None and creator_el.text else ''
                desc_el = item_el.find('description')
                if desc_el is not None and desc_el.text:
                    import html
                    post['subtitle'] = html.unescape(desc_el.text)[:500]
                else:
                    post['subtitle'] = ''
                content_el = item_el.find('{http://purl.org/rss/1.0/modules/content/}encoded')
                if content_el is not None and content_el.text:
                    post['content_preview'] = content_el.text[:1000]
                items.append(post)
        except Exception as exc:
            logger.warning("Failed to parse RSS XML for %s: %s", domain, exc)
        return items

    def fetch_publication_from_rss(self, domain: str) -> dict:
        try:
            resp = self.client.get(rss_url(domain), timeout=self.TIMEOUT)
            resp.raise_for_status()
            xml_text = resp.text
            self._rss_cache[domain] = xml_text
            return self._extract_pub_from_rss_text(xml_text, domain)
        except Exception as exc:
            logger.warning("Failed to fetch publication from RSS for %s: %s", domain, exc)
            return {}

    @staticmethod
    def _extract_pub_from_rss_text(xml_text: str, domain: str) -> dict:
        try:
            root = ElementTree.fromstring(xml_text.encode())
            channel = root.find('channel')
            if channel is None:
                return {}
            name = ''
            desc = ''
            title_el = channel.find('title')
            if title_el is not None and title_el.text:
                name = title_el.text.strip()
            desc_el = channel.find('description')
            if desc_el is not None and desc_el.text:
                import html
                desc = html.unescape(desc_el.text).strip()[:500]
            return {'publication': {'name': name, 'description': desc, 'subscriber_count': None}}
        except Exception as exc:
            logger.warning("Failed to extract publication from RSS text for %s: %s", domain, exc)
            return {}
