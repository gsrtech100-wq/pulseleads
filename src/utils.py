import re
from urllib.parse import urlparse


SUBSTACK_DOMAIN_PATTERN = re.compile(r'^[\w-]+\.substack\.com$')
_REJECTED_DOMAINS = {'substack.com', 'www.substack.com', 'localhost', '127.0.0.1'}
_IP_PATTERN = re.compile(r'^\d+\.\d+\.\d+\.\d+$')


def is_substack_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    parsed = urlparse(url)
    host = parsed.hostname or ''
    if not host:
        return False
    if parsed.scheme not in ('http', 'https'):
        return False
    if host in _REJECTED_DOMAINS:
        return False
    if _IP_PATTERN.match(host):
        return False
    if SUBSTACK_DOMAIN_PATTERN.match(host):
        return True
    return True


def is_known_substack(domain: str) -> bool:
    return bool(SUBSTACK_DOMAIN_PATTERN.match(domain))


def normalize_url(url: str) -> str:
    url = url.strip().rstrip('/')
    if not url.startswith('http'):
        url = 'https://' + url
    return url


def extract_domain(url: str) -> str:
    parsed = urlparse(normalize_url(url))
    return parsed.hostname or ''


def rss_url(domain: str) -> str:
    return f'https://{domain}/feed'


def publication_api_url(domain: str) -> str:
    return f'https://{domain}/api/v1/publication'


def post_api_url(domain: str, post_id: str) -> str:
    return f'https://{domain}/api/v1/posts/{post_id}'


def robots_txt_url(domain: str) -> str:
    return f'https://{domain}/robots.txt'
