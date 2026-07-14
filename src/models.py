from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PostRecord:
    newsletterName: str
    newsletterUrl: str
    newsletterDescription: Optional[str]
    subscriberCount: Optional[int]
    postId: str
    title: str
    url: str
    publishedAt: str
    subtitle: Optional[str]
    wordCount: Optional[int]
    likeCount: Optional[int]
    commentCount: Optional[int]
    restackCount: Optional[int]
    contentHtml: Optional[str]
    contentText: Optional[str]
    authorName: Optional[str]
    authorBio: Optional[str]
    authorAvatarUrl: Optional[str]
    authorEmail: Optional[str]
    category: Optional[str]
    audioUrl: Optional[str]

    def to_dict(self) -> dict:
        return {
            field_name: getattr(self, field_name)
            for field_name in self.__dataclass_fields__
        }
