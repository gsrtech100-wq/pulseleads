import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.pipeline.search import DuckDuckGoProvider


class _FakeResp:
    def __init__(self, text):
        self.text = text

    def raise_for_status(self):
        return None


class _FakeClient:
    def __init__(self, text):
        self._text = text

    def get(self, url, params=None):
        return _FakeResp(self._text)


def test_parses_substack_domains():
    html = (
        '<a href="https://lenny.substack.com/p/ai">x</a>'
        '<a href="https://foo.substack.com">y</a>'
    )
    refs = DuckDuckGoProvider().search("AI", limit=5, client=_FakeClient(html))
    domains = {r.identifier for r in refs}
    assert "lenny.substack.com" in domains
    assert "foo.substack.com" in domains
    assert all(r.platform == "substack" for r in refs)
