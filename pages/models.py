from django.db import models
from django.urls import reverse
from django.utils.text import slugify


FORMAT_MARKDOWN = 'markdown'
FORMAT_HTML     = 'html'
FORMAT_CHOICES  = [
    (FORMAT_MARKDOWN, 'Markdown'),
    (FORMAT_HTML,     'HTML'),
]


class Page(models.Model):

    title          = models.CharField(max_length=200)
    slug           = models.SlugField(unique=True)
    content        = models.TextField()
    content_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default=FORMAT_MARKDOWN,
    )
    published        = models.BooleanField(default=True)
    featured_on_home = models.BooleanField(
        default=False,
        help_text='Show this page as a card in the homepage page grid',
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TextBlock(models.Model):

    STYLE_DEFAULT      = 'default'
    STYLE_NO_BACKGROUND = 'no_background'
    STYLE_CUSTOM_FONT  = 'custom_font'

    STYLE_CHOICES = [
        (STYLE_DEFAULT,        'Default — bordered card with light background'),
        (STYLE_NO_BACKGROUND,  'No Background — clean, text only'),
        (STYLE_CUSTOM_FONT,    'Custom Font — large serif display style'),
    ]

    LOCATION_PAGE   = 'page'
    LOCATION_FOOTER = 'footer'
    LOCATION_CHOICES = [
        (LOCATION_PAGE,   'Page'),
        (LOCATION_FOOTER, 'Footer'),
    ]

    page = models.ForeignKey(
        'Page', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='blocks',
        help_text='Assign to a page, or leave blank to show on the home page',
    )
    title   = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    order          = models.IntegerField(default=0)
    content_format = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES,
        default=FORMAT_MARKDOWN,
    )
    style   = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default=STYLE_DEFAULT,
    )
    location = models.CharField(
        max_length=10,
        choices=LOCATION_CHOICES,
        default=LOCATION_PAGE,
        help_text='Whether this block appears on a page or in the site footer',
    )

    link_page = models.ForeignKey(
        'Page', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='linked_from_blocks',
        help_text='Optional page to link to — renders a button at the bottom of the block',
    )
    link_label = models.CharField(
        max_length=80, blank=True, default='Read More',
        help_text='Button label (defaults to "Read More")',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f'Block {self.id}'


class Footer(models.Model):
    text           = models.TextField(blank=True, help_text='Text displayed in the footer (supports Markdown)')
    image          = models.ImageField(upload_to='footer/', blank=True, null=True, help_text='Optional image displayed in the footer')
    copyright_text = models.CharField(max_length=200, blank=True, help_text='Small copyright line shown at the bottom of the footer')

    class Meta:
        verbose_name        = 'Footer Settings'
        verbose_name_plural = 'Footer Settings'

    def __str__(self):
        return 'Footer Settings'


class HeaderSettings(models.Model):
    text  = models.TextField(blank=True, help_text='Text displayed in a banner below the navbar (supports Markdown)')
    image = models.ImageField(upload_to='header/', blank=True, null=True, help_text='Optional banner image displayed below the navbar')

    class Meta:
        verbose_name        = 'Header Settings'
        verbose_name_plural = 'Header Settings'

    def __str__(self):
        return 'Header Settings'


class SiteStylesheet(models.Model):
    css = models.TextField(blank=True)

    class Meta:
        verbose_name        = 'Site Stylesheet'
        verbose_name_plural = 'Site Stylesheet'

    def __str__(self):
        return 'Site Stylesheet'


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Shoppalist')
    logo      = models.ImageField(upload_to='logo/', blank=True, null=True)

    class Meta:
        verbose_name        = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'



class BootstrapOverrides(models.Model):
    css = models.TextField(blank=True)

    class Meta:
        verbose_name        = 'Bootstrap Overrides'
        verbose_name_plural = 'Bootstrap Overrides'

    def __str__(self):
        return 'Bootstrap Overrides'


class HomeSettings(models.Model):
    """Singleton — controls the layout of the homepage."""
    heading        = models.CharField(
        max_length=100, default='Home',
        help_text='Heading shown at the top of the homepage',
    )
    intro          = models.TextField(
        blank=True,
        help_text='Optional intro paragraph shown below the heading (supports Markdown)',
    )
    show_page_grid = models.BooleanField(
        default=True,
        help_text='Show the page cards grid below the blocks',
    )
    featured_pages = models.ManyToManyField(
        'Page',
        blank=True,
        related_name='featured_in_home',
        help_text='Pages to show in the grid. Leave empty to show all published pages.',
    )

    class Meta:
        verbose_name        = 'Homepage Settings'
        verbose_name_plural = 'Homepage Settings'

    def __str__(self):
        return 'Homepage Settings'


class HomepageBlock(TextBlock):
    """Proxy model so homepage blocks get their own admin section."""
    class Meta:
        proxy                = True
        verbose_name         = 'Homepage Block'
        verbose_name_plural  = 'Homepage Blocks'


class NavLink(models.Model):
    """A single entry in the site navigation menu."""

    label      = models.CharField(max_length=100, help_text='Text shown in the menu')
    page       = models.ForeignKey(
        'Page', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='nav_links',
        help_text='Link to an internal page — leave blank if using a custom URL',
    )
    custom_url = models.CharField(
        max_length=200, blank=True,
        help_text='Use for non-page links, e.g. /contact/ or https://example.com',
    )
    order      = models.IntegerField(default=0, help_text='Lower numbers appear first')

    class Meta:
        verbose_name        = 'Nav Link'
        verbose_name_plural = 'Nav Links'
        ordering            = ['order', 'id']

    def __str__(self):
        return self.label

    def get_url(self):
        if self.page_id:
            return self.page.get_absolute_url()
        return self.custom_url
