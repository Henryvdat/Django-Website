from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

from .constants import CSS_TEXTAREA_ATTRS, DEFAULT_BOOTSTRAP_OVERRIDES
from .models import (
    BootstrapOverrides, ContactInfo, Footer, HeaderSettings, Page,
    SiteSettings, SiteStylesheet, TextBlock,
)


# ── Shared utilities ──────────────────────────────────────────────────────────

class SingletonAdminMixin:
    """Prevents creating a second row for models that should only have one."""
    def has_add_permission(self, request):
        return not self.model.objects.exists()


# ── TextBlock inline ──────────────────────────────────────────────────────────

class TextBlockInline(admin.StackedInline):
    model  = TextBlock
    extra  = 1
    fields = ('title', 'content', 'style', 'order')


# ── Page ──────────────────────────────────────────────────────────────────────

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display  = ('title', 'slug', 'published', 'updated_at')
    list_filter   = ('published',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TextBlockInline]


# ── Header Settings ───────────────────────────────────────────────────────────

@admin.register(HeaderSettings)
class HeaderSettingsAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('text', 'image'),
            'description': (
                'Optional banner content shown below the navbar. '
                'Background colour is controlled via Page Settings → Site Stylesheet.'
            ),
        }),
    )


# ── Site Settings ─────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdminMixin, admin.ModelAdmin):
    pass


# ── Footer Settings ───────────────────────────────────────────────────────────

@admin.register(Footer)
class FooterAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ('Content', {
            'fields': ('text', 'image'),
            'description': (
                'Main footer content. For additional text blocks use '
                'Content Blocks → Footer Text Block.'
            ),
        }),
        ('Copyright', {
            'fields': ('copyright_text',),
        }),
    )


# ── Contact Page ──────────────────────────────────────────────────────────────

@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ('Page Heading & Intro', {
            'fields': ('heading', 'intro_text'),
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'address', 'opening_hours'),
        }),
        ('Extra Information', {
            'fields': ('extra_info',),
        }),
    )


# ── Site Stylesheet ───────────────────────────────────────────────────────────

class SiteStylesheetForm(forms.ModelForm):
    class Meta:
        model   = SiteStylesheet
        fields  = '__all__'
        widgets = {'css': forms.Textarea(attrs=CSS_TEXTAREA_ATTRS)}


@admin.register(SiteStylesheet)
class SiteStylesheetAdmin(SingletonAdminMixin, admin.ModelAdmin):
    form = SiteStylesheetForm


# ── Bootstrap Overrides ───────────────────────────────────────────────────────

class BootstrapOverridesForm(forms.ModelForm):
    class Meta:
        model   = BootstrapOverrides
        fields  = '__all__'
        widgets = {'css': forms.Textarea(attrs=CSS_TEXTAREA_ATTRS)}


@admin.register(BootstrapOverrides)
class BootstrapOverridesAdmin(SingletonAdminMixin, admin.ModelAdmin):
    form = BootstrapOverridesForm
    change_form_template = 'admin/pages/bootstrapoverrides/change_form.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:object_id>/reset/',
                self.admin_site.admin_view(self.reset_to_default),
                name='bootstrapoverrides_reset',
            ),
        ]
        return custom_urls + urls

    def reset_to_default(self, request, object_id):
        obj = BootstrapOverrides.objects.get(pk=object_id)
        obj.css = DEFAULT_BOOTSTRAP_OVERRIDES
        obj.save()
        messages.success(request, 'Bootstrap overrides have been reset to default.')
        return redirect('..')
