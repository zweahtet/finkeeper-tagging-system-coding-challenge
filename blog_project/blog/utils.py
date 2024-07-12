from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Tag


def get_all_tags():
    tags = cache.get("all_tags")
    if tags is None:
        tags = list(Tag.objects.all())
        cache.set("all_tags", tags, 3600)  # Cache for 1 hour
    return tags


@receiver([post_save, post_delete], sender=Tag)
def invalidate_tag_cache(sender, instance, **kwargs):
    cache.delete("all_tags")
