import types

from django import forms
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

from .constants import CSS_TEXTAREA_ATTRS, DEFAULT_BOOTSTRAP_OVERRIDES
from .models import (
    BootstrapOverrides, Footer, HeaderSettings,
    HomeSettings, HomepageBlock, NavLink, Page,
    SiteSettings, SiteStylesheet, TextBlock,
)


# ── Shared utilities ──────────────────────────────────────────────────────────

class SingletonAdminMixin:
    """Prevents creating a second row for models that should only have one."""
    def has_add_permission(self, request):
        return not self.model.objects.exists()


# ── Homepage Settings ─────────────────────────────────────────────────────────

@admin.register(HomeSettings)
class HomeSettingsAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ('Heading', {
            'fields': ('heading', 'intro'),
        }),
        ('Page Grid', {
            'fields': ('show_page_grid', 'featured_pages'),
            'description': (
                'When "Show page grid" is on, a row of page cards appears below the blocks. '
                'Use the picker to choose specific pages — move them to the right column. '
                'Leave the right column empty to show all published pages automatically.'
            ),
        }),
    )
    filter_horizontal = ('featured_pages',)


# ── Homepage Blocks ───────────────────────────────────────────────────────────

@admin.register(HomepageBlock)
class HomepageBlockAdmin(admin.ModelAdmin):
    """Admin view scoped to blocks that live on the homepage (no page assigned)."""
    list_display       = ('__str__', 'style', 'order')
    list_editable      = ('style', 'order')
    list_display_links = ('__str__',)
    fields             = ('title', 'content', 'content_format', 'style', 'order', 'link_page', 'link_label')
    ordering           = ('order',)

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .filter(page__isnull=True, location=TextBlock.LOCATION_PAGE)
        )

    def save_model(self, request, obj, form, change):
        obj.page     = None
        obj.location = TextBlock.LOCATION_PAGE
        super().save_model(request, obj, form, change)


# ── Nav Links ────────────────────────────────────────────────────────────────

@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display  = ('order', 'label', 'page', 'custom_url')
    list_editable = ('order', 'label', 'page', 'custom_url')
    list_display_links = None   # make the whole row editable in-place
    ordering      = ('order', 'id')


# ── TextBlock inline ──────────────────────────────────────────────────────────

class TextBlockInline(admin.StackedInline):
    model   = TextBlock
    fk_name = 'page'
    extra   = 1
    fields  = ('title', 'content', 'style', 'order')


# ── Page ──────────────────────────────────────────────────────────────────────

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display        = ('title', 'slug', 'published', 'featured_on_home', 'updated_at')
    list_filter         = ('published', 'featured_on_home')
    list_editable       = ('published', 'featured_on_home')
    list_display_links  = ('title',)
    search_fields       = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines             = [TextBlockInline]


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


# ── Admin branding ────────────────────────────────────────────────────────────

admin.site.site_header = 'My CMS'
admin.site.site_title  = 'My CMS Admin'
admin.site.index_title = 'Site Administration'


# ── Admin index grouping ──────────────────────────────────────────────────────
#
# Django groups the admin index by app label.  All our models live in the
# 'pages' app so they appear in one big unsorted list.  We fix this by
# patching get_app_list to return custom logical groups in a fixed order.
#
# The model order within each group is the order the models should appear.

_ADMIN_GROUPS = [
    {
        'name':   'Site Configuration',
        'models': [
            'SiteSettings',
            'HeaderSettings',
            'Footer',
            'SiteStylesheet',
            'BootstrapOverrides',
        ],
    },
    {
        'name':   'Homepage',
        'models': [
            'HomeSettings',
            'HomepageBlock',
            'NavLink',
        ],
    },
    {
        'name':   'Content',
        'models': [
            'Page',
        ],
    },
    {
        'name':   'Users & Permissions',
        'models': [
            'User',
            'Group',
        ],
    },
]


def _custom_get_app_list(self, request, app_label=None):
    """Return admin index groups in the order defined by _ADMIN_GROUPS."""
    app_dict = self._build_app_dict(request, app_label)

    # Flatten every registered model into a single lookup by object_name.
    all_models = {}
    for app_data in app_dict.values():
        for model in app_data['models']:
            all_models[model['object_name']] = model

    result = []
    seen   = set()

    for group in _ADMIN_GROUPS:
        group_models = []
        for name in group['models']:
            if name in all_models and name not in seen:
                group_models.append(all_models[name])
                seen.add(name)

        if group_models:
            result.append({
                'name':              group['name'],
                'app_label':         group['name'].lower().replace(' ', '_'),
                'app_url':           '/admin/',
                'has_module_perms':  True,
                'models':            group_models,
            })

    # Anything not explicitly listed above goes into a catch-all group
    # so nothing is ever accidentally hidden.
    remaining = [m for k, m in all_models.items() if k not in seen]
    if remaining:
        result.append({
            'name':             'Other',
            'app_label':        'other',
            'app_url':          '/admin/',
            'has_module_perms': True,
            'models':           remaining,
        })

    return result


admin.site.get_app_list = types.MethodType(_custom_get_app_list, admin.site)
