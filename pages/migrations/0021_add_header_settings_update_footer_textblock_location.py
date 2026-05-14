"""
Migration: add HeaderSettings model, update Footer (drop text / add background_color),
add location field to TextBlock.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_remove_block_image_fields'),
    ]

    operations = [
        # ── HeaderSettings ────────────────────────────────────────────────────
        migrations.CreateModel(
            name='HeaderSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_color', models.CharField(
                    blank=True, default='#343a40', max_length=7,
                    help_text='Hex color code for the header/navbar background, e.g. #343a40',
                )),
            ],
            options={
                'verbose_name': 'Header Settings',
                'verbose_name_plural': 'Header Settings',
            },
        ),

        # ── Footer: remove text, add background_color ─────────────────────────
        migrations.RemoveField(
            model_name='footer',
            name='text',
        ),
        migrations.AddField(
            model_name='footer',
            name='background_color',
            field=models.CharField(
                blank=True, default='#343a40', max_length=7,
                help_text='Hex color code for the footer background, e.g. #343a40',
            ),
        ),

        # ── TextBlock: add location field ─────────────────────────────────────
        migrations.AddField(
            model_name='textblock',
            name='location',
            field=models.CharField(
                choices=[('page', 'Page'), ('footer', 'Footer')],
                default='page',
                max_length=10,
                help_text='Whether this block appears on a page or in the site footer',
            ),
        ),
    ]
