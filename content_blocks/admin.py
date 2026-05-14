from django.contrib import admin

from pages.admin import SingletonAdminMixin
from pages.models import Footer

from .models import FooterContent, TextBlockContent


@admin.register(TextBlockContent)
class TextBlockContentAdmin(admin.ModelAdmin):
    list_display   = ('title', 'style', 'order', 'created_at')
    list_editable  = ('style', 'order')
    ordering       = ('order',)


@admin.register(FooterContent)
class FooterContentAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'copyright_text')
    # has_add_permission is inherited from SingletonAdminMixin,
    # which checks Footer (the parent model) via self.model.objects.exists()
