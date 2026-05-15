from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    home, page_detail,
    edit_page,
    edit_block, add_block, delete_block,
    upload_inline_image,
    dynamic_css, bootstrap_overrides_css,
    PageViewSet,
)

# ── DRF API router ────────────────────────────────────────────────────────────
router = DefaultRouter()
router.register(r'api/pages', PageViewSet, basename='page')

# ── URL patterns ──────────────────────────────────────────────────────────────
urlpatterns = [
    path('', home, name='home'),
    path('page/<slug:slug>/', page_detail, name='page_detail'),
    # Page editing (staff only)
    path('page/<slug:slug>/edit/', edit_page, name='edit_page'),

    # TextBlock routes (staff only)
    path('block/edit/<int:block_id>/', edit_block, name='edit_block'),
    path('block/delete/<int:block_id>/', delete_block, name='delete_block'),
    path('block/add/', add_block, name='add_block_home'),
    path('block/add/<slug:slug>/', add_block, name='add_block_page'),

    # Inline image upload used by the Markdown editor toolbar (staff only)
    path('upload/image/', upload_inline_image, name='upload_inline_image'),

    # Dynamic stylesheets served from the database (cached)
    path('site-styles.css', dynamic_css, name='dynamic_css'),
    path('bootstrap-overrides.css', bootstrap_overrides_css, name='bootstrap_overrides_css'),

    # REST API
    *router.urls,
]
