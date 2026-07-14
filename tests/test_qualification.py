import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from src.entities import Profile, Lead
from src.pipeline.qualification import QualificationService


def test_scores_by_keyword():
    p = Profile(platform="substack", source_id="x", name="Jane",
                bio="writes about AI", source_name="AI Weekly")
    leads = QualificationService().score([p], ["AI"])
    assert len(leads) == 1
    assert leads[0].qualified is True
    assert leads[0].relevance_score > 0


def test_low_relevance_unqualified():
    p = Profile(platform="substack", source_id="x", name="Bob",
                bio="cooking recipes", source_name="Food Blog")
    leads = QualificationService().score([p], ["cybersecurity"])
    assert leads[0].qualified is False


def test_no_keyword_all_relevant():
    p = Profile(platform="substack", source_id="x", name="Sam")
    leads = QualificationService().score([p], [])
    assert leads[0].qualified is True
