from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SourceRef:
    platform: str
    identifier: str   # e.g. "lenny.substack.com" or a handle


@dataclass
class Profile:
    platform: str
    source_id: str
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    public_email: Optional[str] = None
    socials: dict = field(default_factory=dict)
    audience_size: Optional[int] = None
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    raw: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        socials = self.socials or {}
        twitter = socials.get("twitter") or socials.get("x")
        linkedin = socials.get("linkedin")
        website = socials.get("website")
        social_links = ",".join(f"{k}:{v}" for k, v in socials.items())
        return {
            "platform": self.platform,
            "sourceId": self.source_id,
            "sourceName": self.source_name,
            "sourceUrl": self.source_url,
            "authorName": self.name,
            "authorBio": self.bio,
            "authorAvatarUrl": self.avatar,
            "publicEmail": self.public_email,
            "hasEmail": bool(self.public_email),
            "twitter": twitter,
            "linkedin": linkedin,
            "website": website,
            "socialLinks": social_links,
            "audienceSize": self.audience_size,
        }


@dataclass
class Lead:
    profile: Profile
    relevance_score: float = 0.0
    audience_score: float = 0.0
    qualified: bool = False
    contact_ready: bool = False

    def to_dict(self) -> dict:
        d = self.profile.to_dict()
        d.update({
            "relevanceScore": round(self.relevance_score, 3),
            "audienceScore": round(self.audience_score, 3),
            "qualified": self.qualified,
            "contactReady": self.contact_ready,
        })
        return d
