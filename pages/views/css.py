"""
CSS utility views — serve stylesheet content stored in the database.
Results are cached (300 s) and invalidated by post_save signals in pages/signals.py.
"""
from django.core.cache import cache
from django.http import HttpResponse

from ..models import BootstrapOverrides, SiteStylesheet


def dynamic_css(request):
    css = cache.get('site_stylesheet_css')
    if css is None:
        obj = SiteStylesheet.objects.first()
        css = obj.css if obj else ''
        cache.set('site_stylesheet_css', css, 300)
    return HttpResponse(css, content_type='text/css')


def bootstrap_overrides_css(request):
    css = cache.get('bootstrap_overrides_css')
    if css is None:
        obj = BootstrapOverrides.objects.first()
        css = obj.css if obj else ''
        cache.set('bootstrap_overrides_css', css, 300)
    return HttpResponse(css, content_type='text/css')
