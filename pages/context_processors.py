"""
Context processor that injects the site footer and settings into every template.

Both objects are singleton rows that almost never change, so they are cached for
five minutes.  post_save signals in pages/signals.py clear the cache keys
immediately whenever the objects are saved via the admin or shell.
"""
from django.core.cache import cache

from .models import Footer, SiteSettings


def footer_content(request):
    footer = cache.get('site_footer')
    if footer is None:
        footer = Footer.objects.first()
        cache.set('site_footer', footer, 300)

    site_settings = cache.get('site_settings')
    if site_settings is None:
        site_settings = SiteSettings.objects.first()
        cache.set('site_settings', site_settings, 300)

    return {
        'footer':        footer,
        'site_settings': site_settings,
    }
