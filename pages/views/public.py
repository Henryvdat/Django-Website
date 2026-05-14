"""Public-facing views — no authentication required."""
from django.shortcuts import get_object_or_404, render

from ..models import ContactInfo, Page, TextBlock


def home(request):
    pages  = Page.objects.filter(published=True)
    blocks = TextBlock.objects.filter(page__isnull=True).order_by('order')
    return render(request, 'home.html', {'pages': pages, 'blocks': blocks})


def page_detail(request, slug):
    page   = get_object_or_404(Page, slug=slug, published=True)
    blocks = page.blocks.select_related('page').order_by('order')
    return render(request, 'page_detail.html', {'page': page, 'blocks': blocks})


def contact(request):
    contact_info = ContactInfo.objects.first()
    return render(request, 'contact.html', {'contact_info': contact_info})
