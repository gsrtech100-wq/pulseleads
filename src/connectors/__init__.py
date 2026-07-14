from ..pipeline.connector import SourceConnector, ConnectorRegistry
from ..entities import SourceRef, Profile

from . import substack  # registers SubstackConnector (Connector #1)


@ConnectorRegistry.register
class MediumConnector(SourceConnector):
    """EXTENSION POINT — not implemented in MVP.

    Implement fetch_profiles(ref, limit, client) using Medium's public API / RSS
    (https://<user>.medium.com/feed). Map authors to Profile. Then this connector
    is automatically routed by the orchestrator — no core change required.
    """
    platform = "medium"

    def fetch_profiles(self, ref: SourceRef, limit: int, client) -> list[Profile]:
        raise NotImplementedError("Medium connector is an extension point (MVP ships Substack only).")


@ConnectorRegistry.register
class GitHubConnector(SourceConnector):
    """EXTENSION POINT — not implemented in MVP.

    Map GitHub repos -> maintainers/contributors to Profile. Use GitHub REST/GraphQL.
    """
    platform = "github"

    def fetch_profiles(self, ref: SourceRef, limit: int, client) -> list[Profile]:
        raise NotImplementedError("GitHub connector is an extension point (MVP ships Substack only).")


@ConnectorRegistry.register
class YouTubeConnector(SourceConnector):
    """EXTENSION POINT — not implemented in MVP.

    Map YouTube channels -> creators to Profile via YouTube Data API.
    """
    platform = "youtube"

    def fetch_profiles(self, ref: SourceRef, limit: int, client) -> list[Profile]:
        raise NotImplementedError("YouTube connector is an extension point (MVP ships Substack only).")


@ConnectorRegistry.register
class BlogRssConnector(SourceConnector):
    """EXTENSION POINT — not implemented in MVP.

    Generic RSS connector. Reuse StackPulse's RSS parser for any blog with a feed.
    """
    platform = "blog"

    def fetch_profiles(self, ref: SourceRef, limit: int, client) -> list[Profile]:
        raise NotImplementedError("Blog/RSS connector is an extension point (MVP ships Substack only).")
