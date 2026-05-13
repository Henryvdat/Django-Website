from django import forms
from django.contrib import admin
from .models import TextBlockContent, FooterContent
from pages.models import Footer


@admin.register(TextBlockContent)
class TextBlockContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'style', 'order', 'created_at')
    list_editable = ('style', 'order')
    ordering = ('order',)


@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'copyright_text')

    def has_add_permission(self, request):
        return not Footer.objects.exists()
