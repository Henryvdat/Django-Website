from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets

from .models import Page, TextBlock
from .serializers import PageSerializer
from .forms import TextBlockForm


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


from .models import Footer

def home(request):
    pages = Page.objects.filter(published=True)
    blocks = TextBlock.objects.all().order_by('order')
    footer = Footer.objects.first()

    return render(request, 'home.html', {
        'pages': pages,
        'blocks': blocks,
        'footer': footer,
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