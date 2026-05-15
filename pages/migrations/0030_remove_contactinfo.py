"""
Migration: remove the ContactInfo model.
Contact is now a regular Page created and edited through the Pages admin.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_homesettings_featured_pages'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContactInfo',
        ),
    ]
