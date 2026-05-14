"""
Authenticated editing views — all require staff login.
delete_block is also restricted to POST to prevent accidental deletion via GET.
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..forms import PageForm, TextBlockForm
from ..models import Page, TextBlock


@staff_member_required
def edit_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('page_detail', slug=page.slug)
    else:
        form = PageForm(instance=page)
    return render(request, 'edit_page.html', {'form': form, 'page': page})


@staff_member_required
def edit_block(request, block_id):
    block = get_object_or_404(TextBlock, id=block_id)
    if request.method == 'POST':
        form = TextBlockForm(request.POST, request.FILES, instance=block)
        if form.is_valid():
            form.save()
            return redirect('page_detail', slug=block.page.slug) if block.page else redirect('home')
    else:
        form = TextBlockForm(instance=block)
    return render(request, 'edit_block.html', {'form': form, 'block': block})


@staff_member_required
def add_block(request, slug=None):
    """Add a new TextBlock to a page (slug) or the home page (no slug)."""
    page = get_object_or_404(Page, slug=slug) if slug else None
    if request.method == 'POST':
        form = TextBlockForm(request.POST, request.FILES)
        if form.is_valid():
            block = form.save(commit=False)
            block.page = page
            # Single query to determine the next order value
            last = TextBlock.objects.filter(page=page).order_by('-order').first()
            block.order = (last.order + 1) if last else 0
            block.save()
            return redirect('page_detail', slug=page.slug) if page else redirect('home')
    else:
        form = TextBlockForm()
    return render(request, 'edit_block.html', {
        'form': form, 'block': None, 'page': page, 'adding': True,
    })


@staff_member_required
@require_POST
def delete_block(request, block_id):
    block = get_object_or_404(TextBlock, id=block_id)
    page  = block.page
    block.delete()
    return redirect('page_detail', slug=page.slug) if page else redirect('home')
