from django.core.cache import cache
from django.db.models import Count
from .models import Tag


def get_all_tags():
    """
    Retrieve all tags, using cache if available.

    This function attempts to get the tags from the cache. If the tags are not
    found in the cache, it queries the database and stores the result in the cache.

    Returns:
        list: A list of all Tag objects.
    """
    tags = cache.get("all_tags")
    if tags is None:
        tags = list(Tag.objects.all())
        cache.set("all_tags", tags, timeout=3600)  # Cache for 1 hour
    return tags


def get_popular_tags(limit=10):
    """
    Retrieve the most popular tags, using cache if available.

    This function attempts to get the popular tags from the cache. If the tags are not
    found in the cache, it queries the database, annotates with post count, orders by
    popularity, and stores the result in the cache.

    Args:
        limit (int): The number of popular tags to retrieve. Default is 10.

    Returns:
        QuerySet: A QuerySet of the most popular Tag objects.
    """
    popular_tags = cache.get("popular_tags")
    if popular_tags is None:
        popular_tags = Tag.objects.annotate(post_count=Count("posts")).order_by(
            "-post_count"
        )[:limit]
        cache.set("popular_tags", popular_tags, timeout=3600)  # Cache for 1 hour
    return popular_tags
