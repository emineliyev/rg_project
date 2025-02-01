from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from partners.models import Partner


@receiver(post_save, sender=Partner)
def clear_partner_cache(sender, instance, **kwargs):
    cache.clear()
