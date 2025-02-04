from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from about.models import About


@receiver(post_save, sender=About)
def clear_about_cache(sender, instance, **kwargs):
    cache.clear()
