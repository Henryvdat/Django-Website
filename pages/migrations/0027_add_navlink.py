"""
Migration: create the NavLink table and seed it with the four links that
were previously hard-coded in base.html (Home, About, Products, Contact).
"""
from django.db import migrations, models
import django.db.models.deletion


def seed_nav_links(apps, schema_editor):
    NavLink = apps.get_model('pages', 'NavLink')
    Page    = apps.get_model('pages', 'Page')

    # Helper: try to find a Page by slug; fall back to a custom URL.
    def page_or_url(slug, fallback_url):
        try:
            return Page.objects.get(slug=slug), ''
        except Page.DoesNotExist:
            return None, fallback_url

    links = [
        {'label': 'Home',     'slug': None,       'url': '/'},
        {'label': 'About',    'slug': 'about',    'url': '/page/about/'},
        {'label': 'Products', 'slug': 'products', 'url': '/page/products/'},
        {'label': 'Contact',  'slug': None,       'url': '/contact/'},
    ]

    for i, cfg in enumerate(links):
        if cfg['slug']:
            pg, cu = page_or_url(cfg['slug'], cfg['url'])
        else:
            pg, cu = None, cfg['url']

        NavLink.objects.create(
            label=cfg['label'],
            page=pg,
            custom_url=cu,
            order=i,
        )


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0026_fix_textblock_link_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavLink',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label',      models.CharField(max_length=100, help_text='Text shown in the menu')),
                ('custom_url', models.CharField(blank=True, max_length=200, help_text='Use for non-page links, e.g. /contact/ or https://example.com')),
                ('order',      models.IntegerField(default=0, help_text='Lower numbers appear first')),
                ('page',       models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='nav_links',
                    to='pages.page',
                    help_text='Link to an internal page — leave blank if using a custom URL',
                )),
            ],
            options={
                'verbose_name':        'Nav Link',
                'verbose_name_plural': 'Nav Links',
                'ordering':            ['order', 'id'],
            },
        ),
        migrations.RunPython(seed_nav_links, no_op),
    ]
