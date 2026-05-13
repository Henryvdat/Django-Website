from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Page, SiteStylesheet, BootstrapOverrides, ContactInfo, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Page Heading & Intro', {
            'fields': ('heading', 'intro_text')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'address', 'opening_hours')
        }),
        ('Extra Information', {
            'fields': ('extra_info',)
        }),
    )

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()


class SiteStylesheetForm(forms.ModelForm):
    class Meta:
        model = SiteStylesheet
        fields = '__all__'
        widgets = {
            'css': forms.Textarea(attrs={
                'style': (
                    'font-family: monospace;'
                    'font-size: 13px;'
                    'width: 100%;'
                    'height: 600px;'
                    'background: #1e1e1e;'
                    'color: #d4d4d4;'
                    'border: 1px solid #444;'
                    'padding: 12px;'
                    'line-height: 1.5;'
                ),
                'spellcheck': 'false',
            }),
        }


@admin.register(SiteStylesheet)
class SiteStylesheetAdmin(admin.ModelAdmin):
    form = SiteStylesheetForm

    def has_add_permission(self, request):
        return not SiteStylesheet.objects.exists()


DEFAULT_BOOTSTRAP_OVERRIDES = """\
/* ============================================================
   BOOTSTRAP OVERRIDES
   These load after Bootstrap so they always take priority.
   Uncomment any rule to activate it, or add your own below.
   ============================================================ */


/* --- Buttons -------------------------------------------- */

/* .btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
    border-radius: 6px;
} */

/* .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
} */


/* --- Navbar --------------------------------------------- */

/* .navbar.bg-dark {
    background-color: #212529 !important;
} */

/* .navbar-brand {
    font-size: 1.4rem;
    font-weight: 700;
} */


/* --- Cards ---------------------------------------------- */

/* .card {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
} */

/* .card-header {
    font-weight: 600;
} */


/* --- Links ---------------------------------------------- */

/* a {
    color: #0d6efd;
    text-decoration: none;
} */

/* a:hover {
    text-decoration: underline;
} */


/* --- Typography ----------------------------------------- */

/* body {
    font-size: 1rem;
    line-height: 1.6;
} */

/* h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
} */


/* --- List Group (sidebar nav) --------------------------- */

/* .list-group-item-action:hover {
    background-color: #f0f0f0;
} */


/* --- Badges --------------------------------------------- */

/* .badge.bg-primary {
    background-color: #0d6efd !important;
} */


/* --- Forms ---------------------------------------------- */

/* .form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
} */
"""


class BootstrapOverridesForm(forms.ModelForm):
    class Meta:
        model = BootstrapOverrides
        fields = '__all__'
        widgets = {
            'css': forms.Textarea(attrs={
                'style': (
                    'font-family: monospace;'
                    'font-size: 13px;'
                    'width: 100%;'
                    'height: 600px;'
                    'background: #1e1e1e;'
                    'color: #d4d4d4;'
                    'border: 1px solid #444;'
                    'padding: 12px;'
                    'line-height: 1.5;'
                ),
                'spellcheck': 'false',
            }),
        }


@admin.register(BootstrapOverrides)
class BootstrapOverridesAdmin(admin.ModelAdmin):
    form = BootstrapOverridesForm
    change_form_template = 'admin/pages/bootstrapoverrides/change_form.html'

    def has_add_permission(self, request):
        return not BootstrapOverrides.objects.exists()

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
