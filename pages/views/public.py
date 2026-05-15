"""Public-facing views — no authentication required."""
from django.shortcuts import get_object_or_404, render

from ..models import HomeSettings, Page, TextBlock


def home(request):
    home_settings = HomeSettings.objects.first()

    blocks = (
        TextBlock.objects
        .filter(page__isnull=True, location=TextBlock.LOCATION_PAGE)
        .select_related('link_page')
        .order_by('order')
    )

    pages = None
    if not home_settings or home_settings.show_page_grid:
        if home_settings and home_settings.featured_pages.exists():
            pages = home_settings.featured_pages.filter(published=True).order_by('title')
        else:
            pages = Page.objects.filter(published=True).order_by('title')

    return render(request, 'home.html', {
        'home_settings': home_settings,
        'blocks':        blocks,
        'pages':         pages,
    })


def page_detail(request, slug):
    page   = get_object_or_404(Page, slug=slug, published=True)
    blocks = page.blocks.select_related('page').order_by('order')
    return render(request, 'page_detail.html', {'page': page, 'blocks': blocks})
