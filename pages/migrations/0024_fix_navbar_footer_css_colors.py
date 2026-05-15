"""
Data migration — fix three CSS bugs in the Site Stylesheet:

  1. Missing nav.navbar background-color rule (navbar was transparent).
  2. Invalid CSS typo: "color: ##000000" on footer small (double hash).
  3. Black text on dark background: footer p had color #000000 on the
     #1a1a2e dark footer, making it invisible.
"""
from django.db import migrations

# ── Patch 1: insert nav.navbar background-color before .navbar-brand ─────────
OLD_NAVBAR_BRAND = "/* Site name / logo in the top navbar */\r\n.navbar-brand {"
NEW_NAVBAR_BRAND = (
    "/* Navbar background colour */\r\n"
    "nav.navbar {\r\n"
    "    background-color: #1a1a2e;\r\n"
    "}\r\n\r\n"
    "/* Site name / logo in the top navbar */\r\n"
    ".navbar-brand {"
)

# Unix line endings fallback
OLD_NAVBAR_BRAND_LF = "/* Site name / logo in the top navbar */\n.navbar-brand {"
NEW_NAVBAR_BRAND_LF = (
    "/* Navbar background colour */\n"
    "nav.navbar {\n"
    "    background-color: #1a1a2e;\n"
    "}\n\n"
    "/* Site name / logo in the top navbar */\n"
    ".navbar-brand {"
)

# ── Patch 2: fix double-hash typo in footer small ────────────────────────────
OLD_SMALL_COLOR = "color: ##000000;"
NEW_SMALL_COLOR = "color: rgba(255, 255, 255, 0.7);"

# ── Patch 3: fix invisible black text in footer p ────────────────────────────
OLD_FOOTER_P_CRLF = "footer p {\r\n    color: #000000;"
NEW_FOOTER_P_CRLF = "footer p {\r\n    color: #ffffff;"
OLD_FOOTER_P_LF   = "footer p {\n    color: #000000;"
NEW_FOOTER_P_LF   = "footer p {\n    color: #ffffff;"


def fix_css(apps, schema_editor):
    SiteStylesheet = apps.get_model('pages', 'SiteStylesheet')
    obj = SiteStylesheet.objects.first()
    if not obj:
        return

    css = obj.css
    changed = False

    # Patch 1 — navbar background-color
    if 'nav.navbar' not in css:
        if OLD_NAVBAR_BRAND in css:
            css = css.replace(OLD_NAVBAR_BRAND, NEW_NAVBAR_BRAND)
            changed = True
        elif OLD_NAVBAR_BRAND_LF in css:
            css = css.replace(OLD_NAVBAR_BRAND_LF, NEW_NAVBAR_BRAND_LF)
            changed = True

    # Patch 2 — double-hash typo
    if OLD_SMALL_COLOR in css:
        css = css.replace(OLD_SMALL_COLOR, NEW_SMALL_COLOR)
        changed = True

    # Patch 3 — black text on dark footer
    if OLD_FOOTER_P_CRLF in css:
        css = css.replace(OLD_FOOTER_P_CRLF, NEW_FOOTER_P_CRLF)
        changed = True
    elif OLD_FOOTER_P_LF in css:
        css = css.replace(OLD_FOOTER_P_LF, NEW_FOOTER_P_LF)
        changed = True

    if changed:
        obj.css = css
        obj.save()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0023_header_footer_text_image_css_colors'),
    ]

    operations = [
        migrations.RunPython(fix_css, no_op),
    ]
