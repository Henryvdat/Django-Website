"""
pages.views package — re-exports everything so that urls.py imports are unchanged.
"""
from .public import contact, home, page_detail
from .editing import add_block, delete_block, edit_block, edit_page
from .api import PageViewSet, upload_inline_image
from .css import bootstrap_overrides_css, dynamic_css

__all__ = [
    # public
    'home', 'page_detail', 'contact',
    # editing
    'edit_page', 'edit_block', 'add_block', 'delete_block',
    # api / upload
    'PageViewSet', 'upload_inline_image',
    # css
    'dynamic_css', 'bootstrap_overrides_css',
]
