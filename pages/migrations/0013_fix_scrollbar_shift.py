from django.db import migrations

FIX = """\
/* Always reserve scrollbar space so layout doesn't shift between pages */
html {
    overflow-y: scroll;
}

"""


def apply_fix(apps, schema_editor):
    SiteStylesheet = apps.get_model('pages', 'SiteStylesheet')
    obj = SiteStylesheet.objects.first()
    if obj and 'overflow-y: scroll' not in obj.css:
        obj.css = FIX + obj.css
        obj.save()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_add_contactinfo'),
    ]

    operations = [
        migrations.RunPython(apply_fix, no_op),
    ]
