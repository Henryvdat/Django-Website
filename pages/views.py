from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import viewsets

from .models import Page, TextBlock, Footer, SiteStylesheet, BootstrapOverrides, ContactInfo
from .serializers import PageSerializer
from .forms import TextBlockForm


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


def home(request):
    pages = Page.objects.filter(published=True)
    blocks = TextBlock.objects.all().order_by('order')

    return render(request, 'home.html', {
        'pages': pages,
        'blocks': blocks,
    })


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, published=True)

    return render(request, 'page_detail.html', {
        'page': page
    })


def edit_block(request, block_id):
    block = get_object_or_404(TextBlock, id=block_id)

    if request.method == 'POST':
        form = TextBlockForm(request.POST, instance=block)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TextBlockForm(instance=block)

    return render(request, 'edit_block.html', {
        'form': form
    })


def delete_block(request, block_id):
    block = get_object_or_404(TextBlock, id=block_id)
    block.delete()

    return redirect('home')


def contact(request):
    contact_info = ContactInfo.objects.first()
    return render(request, 'contact.html', {
        'contact_info': contact_info,
    })


def dynamic_css(request):
    stylesheet = SiteStylesheet.objects.first()
    css = stylesheet.css if stylesheet else ''
    return HttpResponse(css, content_type='text/css')


def bootstrap_overrides_css(request):
    overrides = BootstrapOverrides.objects.first()
    css = overrides.css if overrides else ''
    return HttpResponse(css, content_type='text/css')