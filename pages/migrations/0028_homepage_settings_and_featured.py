"""
Migration:
  - Add Page.featured_on_home BooleanField.
  - Create HomeSettings singleton table and seed one record.
  - Create HomepageBlock proxy model.
"""
from django.db import migrations, models


def seed_home_settings(apps, schema_editor):
    HomeSettings = apps.get_model('pages', 'HomeSettings')
    if not HomeSettings.objects.exists():
        HomeSettings.objects.create()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0027_add_navlink'),
    ]

    operations = [
        # ── Page.featured_on_home ──────────────────────────────────────────────
        migrations.AddField(
            model_name='page',
            name='featured_on_home',
            field=models.BooleanField(
                default=False,
                help_text='Show this page as a card in the homepage page grid',
            ),
        ),

        # ── HomeSettings ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='HomeSettings',
            fields=[
                ('id',             models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading',        models.CharField(default='Home', max_length=100, help_text='Heading shown at the top of the homepage')),
                ('intro',          models.TextField(blank=True, help_text='Optional intro paragraph shown below the heading (supports Markdown)')),
                ('show_page_grid', models.BooleanField(default=True, help_text='Show the page cards grid. Tick "Featured on home" on individual Pages to choose which appear; if none are ticked all published pages are shown.')),
            ],
            options={
                'verbose_name':        'Homepage Settings',
                'verbose_name_plural': 'Homepage Settings',
            },
        ),
        migrations.RunPython(seed_home_settings, no_op),

        # ── HomepageBlock proxy ────────────────────────────────────────────────
        migrations.CreateModel(
            name='HomepageBlock',
            fields=[],
            options={
                'proxy':               True,
                'verbose_name':        'Homepage Block',
                'verbose_name_plural': 'Homepage Blocks',
                'indexes':             [],
                'constraints':         [],
            },
            bases=('pages.textblock',),
        ),
    ]
