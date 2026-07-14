import asyncio
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.pipeline.connector import ConnectorRegistry, SourceConnector
from src.entities import SourceRef, Profile
from src.pipeline.qualification import QualificationService
from src.pipeline.export import ExportService
import src.pipeline.export as export_mod


class _FakeConnector(SourceConnector):
    platform = "fake"

    def fetch_profiles(self, ref, limit, client):
        return [
            Profile(platform="fake", source_id=ref.identifier, name="A", public_email="a@x.com"),
            Profile(platform="fake", source_id=ref.identifier, name="B"),
        ]


class _FakeActor:
    @staticmethod
    async def push_data(d):
        _FakeActor.pushed.append(d)

    @staticmethod
    async def charge(event_name=None, count=0):
        _FakeActor.charged = count

    pushed = []
    charged = 0


def test_e2e_pipeline_charges_only_contact_ready(monkeypatch):
    _FakeActor.pushed = []
    _FakeActor.charged = 0
    monkeypatch.setattr(export_mod, "Actor", _FakeActor)

    ConnectorRegistry.register(_FakeConnector)
    c = ConnectorRegistry.get("fake")
    profiles = []
    for r in [SourceRef("fake", "demo")]:
        profiles += c.fetch_profiles(r, 10, None)
    leads = QualificationService().score(profiles, [])
    n = asyncio.run(ExportService().export(leads))

    assert len(_FakeActor.pushed) == 2     # both leads exported
    assert n == 1                          # only the one with public_email is billable
