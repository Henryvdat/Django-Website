from django.urls import path
from .views import home, page_detail, contact, edit_block, delete_block, dynamic_css, bootstrap_overrides_css

urlpatterns = [
    path('', home, name='home'),
    path('page/<slug:slug>/', page_detail, name='page_detail'),
    path('contact/', contact, name='contact'),

    # TextBlock routes
    path('block/edit/<int:block_id>/', edit_block, name='edit_block'),
    path('block/delete/<int:block_id>/', delete_block, name='delete_block'),

    # Dynamic stylesheets served from the database
    path('site-styles.css', dynamic_css, name='dynamic_css'),
    path('bootstrap-overrides.css', bootstrap_overrides_css, name='bootstrap_overrides_css'),
]