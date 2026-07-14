import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.pipeline.connector import ConnectorRegistry, SourceConnector
from src.connectors import substack  # triggers registration
from src.connectors.substack import SubstackConnector


def test_substack_registered():
    assert "substack" in ConnectorRegistry.platforms()
    c = ConnectorRegistry.get("substack")
    assert isinstance(c, SubstackConnector)


def test_extension_stubs_registered():
    for plat in ("medium", "github", "youtube", "blog"):
        assert plat in ConnectorRegistry.platforms()
        c = ConnectorRegistry.get(plat)
        try:
            c.fetch_profiles(None, 1, None)
            assert False, "stub should raise NotImplementedError"
        except NotImplementedError:
            pass
