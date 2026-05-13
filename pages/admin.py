from django.contrib import admin
from .models import Page, TextBlock, Footer


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')


@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('copyright_text',)