from django.contrib import admin

from pages.models import TextBlock

from .models import FooterTextBlock, TextBlockContent


# ── Text Blocks (page content) ────────────────────────────────────────────────

@admin.register(TextBlockContent)
class TextBlockContentAdmin(admin.ModelAdmin):
    list_display  = ('title', 'style', 'order', 'created_at')
    list_editable = ('style', 'order')
    ordering      = ('order',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(location=TextBlock.LOCATION_PAGE)

    def save_model(self, request, obj, form, change):
        obj.location = TextBlock.LOCATION_PAGE
        super().save_model(request, obj, form, change)


# ── Footer Text Blocks ────────────────────────────────────────────────────────

@admin.register(FooterTextBlock)
class FooterTextBlockAdmin(admin.ModelAdmin):
    list_display  = ('title', 'order', 'updated_at')
    list_editable = ('order',)
    ordering      = ('order',)
    fields        = ('title', 'content', 'content_format', 'order')

    def get_queryset(self, request):
        return super().get_queryset(request).filter(location=TextBlock.LOCATION_FOOTER)

    def save_model(self, request, obj, form, change):
        obj.location = TextBlock.LOCATION_FOOTER
        super().save_model(request, obj, form, change)
