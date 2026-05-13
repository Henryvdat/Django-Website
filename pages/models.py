from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TextBlock(models.Model):

    STYLE_DEFAULT = 'default'
    STYLE_NO_BACKGROUND = 'no_background'
    STYLE_CUSTOM_FONT = 'custom_font'

    STYLE_CHOICES = [
        (STYLE_DEFAULT,       'Default — bordered card with light background'),
        (STYLE_NO_BACKGROUND, 'No Background — clean, text only'),
        (STYLE_CUSTOM_FONT,   'Custom Font — large serif display style'),
    ]

    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    order = models.IntegerField(default=0)
    style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default=STYLE_DEFAULT,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Block {self.id}"


class Footer(models.Model):
    text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "Site Footer"


class SiteStylesheet(models.Model):
    css = models.TextField(blank=True)

    class Meta:
        verbose_name = "Site Stylesheet"
        verbose_name_plural = "Site Stylesheet"

    def __str__(self):
        return "Site Stylesheet"


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Shoppalist')
    logo      = models.ImageField(upload_to='logo/', blank=True, null=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'


class ContactInfo(models.Model):
    heading       = models.CharField(max_length=200, default='Contact Us')
    intro_text    = models.TextField(blank=True, help_text='Introductory paragraph shown at the top of the page')
    email         = models.EmailField(blank=True)
    phone         = models.CharField(max_length=50, blank=True)
    address       = models.TextField(blank=True, help_text='Physical address — each line will be shown separately')
    opening_hours = models.TextField(blank=True, help_text='E.g. Mon–Fri 9am–5pm')
    extra_info    = models.TextField(blank=True, help_text='Any additional information to display at the bottom')

    class Meta:
        verbose_name = 'Contact Page'
        verbose_name_plural = 'Contact Page'

    def __str__(self):
        return 'Contact Page'


class BootstrapOverrides(models.Model):
    css = models.TextField(blank=True)

    class Meta:
        verbose_name = "Bootstrap Overrides"
        verbose_name_plural = "Bootstrap Overrides"

    def __str__(self):
        return "Bootstrap Overrides"
