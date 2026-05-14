"""
Migration: remove the old FooterContent proxy (which proxied Footer) and
replace it with FooterTextBlock (which proxies TextBlock).
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content_blocks', '0001_add_proxy_models'),
        ('pages', '0021_add_header_settings_update_footer_textblock_location'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FooterContent',
        ),
        migrations.CreateModel(
            name='FooterTextBlock',
            fields=[],
            options={
                'verbose_name': 'Footer Text Block',
                'verbose_name_plural': 'Footer Text Blocks',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pages.textblock',),
        ),
    ]
