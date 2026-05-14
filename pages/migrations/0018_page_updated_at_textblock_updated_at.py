from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_textblock_image_scale'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='textblock',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
