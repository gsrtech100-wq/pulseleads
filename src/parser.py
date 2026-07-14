import logging
from typing import Optional

from .models import PostRecord

logger = logging.getLogger(__name__)


def parse_publication(publication: dict, domain: str) -> dict:
    info = publication.get('publication', publication)
    return {
        'name': info.get('name', '') or '',
        'url': f'https://{domain}',
        'description': info.get('description') or info.get('tagline'),
        'subscriber_count': info.get('subscriber_count'),
    }


def _get_bylines(post_data: dict) -> list[dict]:
    bylines = post_data.get('publishedBylines', [])
    if isinstance(bylines, list) and len(bylines) > 0:
        return bylines
    author = post_data.get('author')
    if isinstance(author, dict):
        return [author]
    return []


def parse_post(
    rss_item: dict,
    post_json: dict,
    publication_info: dict,
    domain: str,
    include_content: bool,
) -> Optional[PostRecord]:
    post_data = post_json.get('post', post_json) if isinstance(post_json, dict) else {}
    post_id = rss_item.get('post_id') or str(post_data.get('id', ''))
    if not post_id:
        return None

    title = rss_item.get('title') or post_data.get('title', '')
    url = rss_item.get('url') or post_data.get('canonical_url', '') or f'https://{domain}/p/{post_id}'

    content_html = None
    content_text = None
    if include_content:
        content_html = post_data.get('body_html') or post_data.get('html')
        content_text = post_data.get('truncated_body_text') or _strip_html(content_html)

    bylines = _get_bylines(post_data)
    primary_author = bylines[0] if bylines else {}
    author_id = primary_author.get('id')

    category = None
    post_tags = post_data.get('postTags')
    if isinstance(post_tags, list) and len(post_tags) > 0:
        tag = post_tags[0]
        if isinstance(tag, dict):
            category = tag.get('name') or tag.get('tag')
        elif isinstance(tag, str):
            category = tag

    return PostRecord(
        newsletterName=publication_info.get('name', domain),
        newsletterUrl=publication_info.get('url', f'https://{domain}'),
        newsletterDescription=publication_info.get('description'),
        subscriberCount=publication_info.get('subscriber_count'),
        postId=str(post_id),
        title=title or '',
        url=url or '',
        publishedAt=rss_item.get('published_at', '') or post_data.get('post_date', ''),
        subtitle=rss_item.get('subtitle') or post_data.get('subtitle'),
        wordCount=post_data.get('wordcount'),
        likeCount=post_data.get('reaction_count'),
        commentCount=post_data.get('comment_count'),
        restackCount=post_data.get('restacks') if isinstance(post_data.get('restacks'), int) else None,
        contentHtml=content_html,
        contentText=content_text,
        authorName=primary_author.get('name') or post_data.get('author_name'),
        authorBio=primary_author.get('bio') or post_data.get('author_bio'),
        authorAvatarUrl=primary_author.get('photo_url') or primary_author.get('avatar_url'),
        authorEmail=primary_author.get('email'),
        category=category,
        audioUrl=post_data.get('podcast_url'),
    )


def enrich_author(post: PostRecord, author_data: dict) -> PostRecord:
    if not author_data:
        return post
    profile = author_data.get('author', author_data)
    if not post.authorName and profile.get('name'):
        post.authorName = profile['name']
    if not post.authorBio and profile.get('bio'):
        post.authorBio = profile['bio']
    if not post.authorAvatarUrl and profile.get('photo_url'):
        post.authorAvatarUrl = profile['photo_url']
    if not post.authorAvatarUrl and profile.get('avatar_url'):
        post.authorAvatarUrl = profile['avatar_url']
    if not post.authorEmail and profile.get('email'):
        post.authorEmail = profile['email']
    if not post.authorEmail and profile.get('public_email'):
        post.authorEmail = profile['public_email']
    return post


def _strip_html(html: Optional[str]) -> Optional[str]:
    if html is None:
        return None
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(html, 'lxml').get_text(separator=' ', strip=True)
    except Exception:
        import re
        return re.sub(r'<[^>]+>', '', html)
