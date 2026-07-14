from abc import ABC, abstractmethod
from typing import Type

from ..entities import SourceRef, Profile


class SourceConnector(ABC):
    """Frozen connector contract. Implement fetch_profiles for a platform.

    A connector turns one SourceRef into platform-native Profile entities.
    Only connectors know about a specific external platform.
    """
    platform: str

    @abstractmethod
    def fetch_profiles(self, ref: SourceRef, limit: int, client) -> list[Profile]:
        ...

    def enrich_profile(self, p: Profile, client) -> Profile:
        # Override per platform to fill public_email / socials / bio.
        return p


class ConnectorRegistry:
    _reg: dict[str, Type[SourceConnector]] = {}

    @classmethod
    def register(cls, connector_cls: Type[SourceConnector]) -> Type[SourceConnector]:
        cls._reg[connector_cls.platform] = connector_cls
        return connector_cls

    @classmethod
    def get(cls, platform: str) -> SourceConnector:
        if platform not in cls._reg:
            raise KeyError(f"No connector registered for platform '{platform}'. "
                           f"Registered: {list(cls._reg)}")
        return cls._reg[platform]()

    @classmethod
    def platforms(cls) -> list[str]:
        return list(cls._reg)
