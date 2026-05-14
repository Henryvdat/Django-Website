from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_textblock_page_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='textblock',
            name='image_width',
            field=models.IntegerField(
                choices=[(25, '25%'), (33, '33%'), (50, '50%'), (66, '66%'), (75, '75%'), (100, '100% (full width)')],
                default=100,
                help_text='Display width of the block image as a percentage of its container',
            ),
        ),
        migrations.AddField(
            model_name='textblock',
            name='image_align',
            field=models.CharField(
                choices=[('left', 'Left'), ('center', 'Centre'), ('right', 'Right')],
                default='left',
                help_text='Horizontal alignment of the block image',
                max_length=10,
            ),
        ),
    ]
