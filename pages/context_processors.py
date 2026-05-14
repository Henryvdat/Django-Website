"""
Context processor that injects site-wide settings into every template.

Singleton objects (footer, header settings, site settings) are cached for five
minutes.  post_save signals in pages/signals.py clear the relevant cache keys
immediately whenever any of these objects are saved via the admin or shell.

Footer text blocks are NOT cached here because they can be added/removed
frequently; they are fetched fresh on every request (still a very cheap query).
"""
from django.core.cache import cache

from .models import Footer, HeaderSettings, SiteSettings, TextBlock


def footer_content(request):
    footer = cache.get('site_footer')
    if footer is None:
        footer = Footer.objects.first()
        cache.set('site_footer', footer, 300)

    header_settings = cache.get('header_settings')
    if header_settings is None:
        header_settings = HeaderSettings.objects.first()
        cache.set('header_settings', header_settings, 300)

    site_settings = cache.get('site_settings')
    if site_settings is None:
        site_settings = SiteSettings.objects.first()
        cache.set('site_settings', site_settings, 300)

    footer_text_blocks = list(
        TextBlock.objects.filter(location=TextBlock.LOCATION_FOOTER).order_by('order')
    )

    return {
        'footer':             footer,
        'header_settings':    header_settings,
        'site_settings':      site_settings,
        'footer_text_blocks': footer_text_blocks,
    }
