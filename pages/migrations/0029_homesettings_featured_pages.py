"""
Migration: add HomeSettings.featured_pages ManyToMany to Page.
Replaces the scattered featured_on_home approach — pages are now
selected in one place directly inside the Homepage Settings admin.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0028_homepage_settings_and_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='homesettings',
            name='featured_pages',
            field=models.ManyToManyField(
                blank=True,
                help_text='Pages to show in the grid. Leave empty to show all published pages.',
                related_name='featured_in_home',
                to='pages.page',
            ),
        ),
    ]
