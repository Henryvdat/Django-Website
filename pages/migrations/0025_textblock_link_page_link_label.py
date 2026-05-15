"""
Migration: add link_page (FK → Page) and link_label to TextBlock,
enabling a "Read More" button that links to another page.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0024_fix_navbar_footer_css_colors'),
    ]

    operations = [
        migrations.AddField(
            model_name='textblock',
            name='link_page',
            field=models.ForeignKey(
                blank=True,
                help_text='Optional page to link to — renders a button at the bottom of the block',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='linked_from_blocks',
                to='pages.page',
            ),
        ),
        migrations.AddField(
            model_name='textblock',
            name='link_label',
            field=models.CharField(
                blank=True,
                default='Read More',
                help_text='Button label (defaults to "Read More")',
                max_length=80,
            ),
        ),
    ]
