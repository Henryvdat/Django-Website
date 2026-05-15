"""
Data migration — fix the .text-block a colour rule so it no longer applies
to .btn elements inside a block.

The rule was making the Read More button text invisible (blue text on a blue
background) because it matched every <a> tag inside .text-block, including
the new link button.
"""
from django.db import migrations

OLD_LINK  = '.text-block a {'
NEW_LINK  = '.text-block a:not(.btn) {'

OLD_HOVER = '.text-block a:hover {'
NEW_HOVER = '.text-block a:not(.btn):hover {'


def fix_css(apps, schema_editor):
    SiteStylesheet = apps.get_model('pages', 'SiteStylesheet')
    obj = SiteStylesheet.objects.first()
    if not obj:
        return
    css = obj.css
    changed = False
    if OLD_LINK in css:
        css = css.replace(OLD_LINK, NEW_LINK)
        changed = True
    if OLD_HOVER in css:
        css = css.replace(OLD_HOVER, NEW_HOVER)
        changed = True
    if changed:
        obj.css = css
        obj.save()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0025_textblock_link_page_link_label'),
    ]

    operations = [
        migrations.RunPython(fix_css, no_op),
    ]
