"""
API views — DRF ViewSet and the inline-image upload endpoint.
Both require staff/admin authentication.
"""
import os
import uuid

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from ..models import Page
from ..serializers import PageSerializer

# Allowed image extensions for inline uploads (SVG excluded — XSS risk)
_ALLOWED_EXTS  = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif'}
_MAX_UPLOAD_MB = 10


class PageViewSet(viewsets.ModelViewSet):
    """
    REST API for Page objects.
    Admin users see all pages; everyone else only sees published ones.
    """
    serializer_class   = PageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Page.objects.all()
        return Page.objects.filter(published=True)


@staff_member_required
@require_POST
def upload_inline_image(request):
    """
    Accept an image file, validate it, save it to media/inline/, and return
    its public URL as JSON.  Only staff members may call this endpoint.
    """
    file = request.FILES.get('image')
    if not file:
        return JsonResponse({'error': 'No file provided.'}, status=400)

    # Size check
    if file.size > _MAX_UPLOAD_MB * 1024 * 1024:
        return JsonResponse(
            {'error': f'File too large (max {_MAX_UPLOAD_MB} MB).'},
            status=400,
        )

    # Extension check
    _name, ext = os.path.splitext(file.name)
    ext = ext.lower()
    if ext not in _ALLOWED_EXTS:
        return JsonResponse(
            {'error': 'Please upload an image file (jpg, png, gif, webp, avif).'},
            status=400,
        )

    # Content check — verify file is actually an image using Pillow
    try:
        from PIL import Image
        img = Image.open(file)
        img.verify()   # raises on corrupt / non-image data
        file.seek(0)   # verify() consumes the stream; reset before saving
    except Exception:
        return JsonResponse(
            {'error': 'File does not appear to be a valid image.'},
            status=400,
        )

    unique_name = uuid.uuid4().hex + ext
    save_dir    = os.path.join(settings.MEDIA_ROOT, 'inline')
    os.makedirs(save_dir, exist_ok=True)

    with open(os.path.join(save_dir, unique_name), 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

    return JsonResponse({'url': settings.MEDIA_URL + 'inline/' + unique_name})
