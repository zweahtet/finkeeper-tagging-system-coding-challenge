from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Tag


@receiver([post_save, post_delete], sender=Tag)
def invalidate_tag_cache(sender, instance, **kwargs):
    """
    Invalidate the cache when a Tag object is saved or deleted.

    This function invalidates the cache for all tags and popular tags when a Tag object
    is saved or deleted.

    Args:
    - sender: The model class that sent the signal.
    - instance: The instance of the model that was saved or deleted.
    """
    print("Invalidating tag cache ...")
    cache.delete("all_tags")
    cache.delete("popular_tags")
