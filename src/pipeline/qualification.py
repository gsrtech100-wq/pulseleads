import json
import logging
import os
from typing import Optional

from ..entities import Profile, Lead

logger = logging.getLogger(__name__)

_DEFAULT_RULES = {
    "relevance": {
        "keyword_weight": 1.0,
        "min_score": 0.3,
        "fields": ["name", "bio", "source_name"],
    },
    "audience": {"unknown_as_zero": True},
    "contact_required_for_charge": True,
}


class QualificationService:
    """Rules-based scoring. Rules live in config/qualification_rules.json (no code change to retune)."""

    def __init__(self, rules_path: Optional[str] = None):
        self.rules = _DEFAULT_RULES
        if rules_path and os.path.exists(rules_path):
            try:
                with open(rules_path, "r", encoding="utf-8") as f:
                    self.rules = json.load(f)
            except Exception as exc:
                logger.warning("Failed to load qualification rules (%s); using defaults", exc)

    def score(self, profiles: list[Profile], keywords: list[str]) -> list[Lead]:
        rel_cfg = self.rules.get("relevance", {})
        min_score = float(rel_cfg.get("min_score", 0.3))
        fields = rel_cfg.get("fields", ["authorName", "authorBio"])
        kws = [k.lower() for k in (keywords or []) if k]

        leads: list[Lead] = []
        for p in profiles:
            text = " ".join(str(getattr(p, f, "") or "") for f in fields).lower()
            if kws:
                hits = sum(1 for k in kws if k in text)
                relevance = min(1.0, (hits / len(kws)) * float(rel_cfg.get("keyword_weight", 1.0)))
            else:
                relevance = 1.0  # no keyword filter → all relevant
            audience = float(p.audience_size or 0)
            contact_ready = bool(p.public_email or p.socials)
            lead = Lead(
                profile=p,
                relevance_score=relevance,
                audience_score=audience,
                qualified=relevance >= min_score,
                contact_ready=contact_ready,
            )
            leads.append(lead)
        return leads
