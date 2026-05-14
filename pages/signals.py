"""
Cache-invalidation signals.

Clears the relevant cache keys whenever singleton site-config models are saved,
so that views and the context processor always serve fresh data without waiting
for the TTL to expire.
"""
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BootstrapOverrides, Footer, HeaderSettings, SiteSettings, SiteStylesheet


@receiver(post_save, sender=SiteStylesheet)
def clear_stylesheet_cache(sender, **kwargs):
    cache.delete('site_stylesheet_css')


@receiver(post_save, sender=BootstrapOverrides)
def clear_bootstrap_overrides_cache(sender, **kwargs):
    cache.delete('bootstrap_overrides_css')


@receiver(post_save, sender=Footer)
def clear_footer_cache(sender, **kwargs):
    cache.delete('site_footer')


@receiver(post_save, sender=SiteSettings)
def clear_site_settings_cache(sender, **kwargs):
    cache.delete('site_settings')


@receiver(post_save, sender=HeaderSettings)
def clear_header_settings_cache(sender, **kwargs):
    cache.delete('header_settings')
