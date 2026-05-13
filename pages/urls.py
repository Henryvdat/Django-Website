from django.urls import path
from .views import home, page_detail, edit_block, delete_block

urlpatterns = [
    path('', home, name='home'),
    path('page/<slug:slug>/', page_detail, name='page_detail'),

    # TextBlock routes
    path('block/edit/<int:block_id>/', edit_block, name='edit_block'),
    path('block/delete/<int:block_id>/', delete_block, name='delete_block'),
]