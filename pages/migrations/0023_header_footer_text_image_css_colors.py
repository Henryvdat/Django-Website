"""
Migration:
  - Remove background_color from Footer and HeaderSettings.
  - Add text + image to both Footer and HeaderSettings.
  - Update the live Site Stylesheet to include background-color rules for
    the navbar and footer (previously driven by inline DB values).
"""
from django.db import migrations, models

# ─────────────────────────────────────────────────────────────────────────────
# Stylesheet patches
# ─────────────────────────────────────────────────────────────────────────────

# Add background-color to the navbar block.
OLD_NAVBAR_RULE = """\
/* Site name text in the top navbar */
.navbar-brand {"""

NEW_NAVBAR_RULE = """\
/* Navbar / header background colour */
nav.navbar {
    background-color: #343a40;
}

/* Site name text in the top navbar */
.navbar-brand {"""

# Add background-color back to the footer block (was removed when the DB field
# was introduced; now the DB field is gone so CSS owns it again).
OLD_FOOTER_RULE = """\
footer {
    text-align: center;
}"""

NEW_FOOTER_RULE = """\
footer {
    background-color: #343a40;
    text-align: center;
}"""

# Add header-banner and footer image helper rules at the end of the sheet.
EXTRA_CSS = """

/* ============================================================
   HEADER BANNER
   Shown below the navbar when header text or image is set in
   Page Settings → Header Settings.
   ============================================================ */

.header-banner {
    padding: 24px 0;
}

.header-banner__image {
    max-width: 100%;
    height: auto;
    display: block;
    margin-bottom: 12px;
}

.header-banner__text {
    font-size: 1rem;
}


/* ============================================================
   FOOTER IMAGE
   ============================================================ */

.footer__image {
    max-width: 160px;
    height: auto;
}
"""


def update_stylesheet(apps, schema_editor):
    SiteStylesheet = apps.get_model('pages', 'SiteStylesheet')
    obj = SiteStylesheet.objects.first()
    if not obj:
        return
    css = obj.css
    if OLD_NAVBAR_RULE in css:
        css = css.replace(OLD_NAVBAR_RULE, NEW_NAVBAR_RULE)
    if OLD_FOOTER_RULE in css:
        css = css.replace(OLD_FOOTER_RULE, NEW_FOOTER_RULE)
    # Append helper rules only once
    if '.header-banner' not in css:
        css += EXTRA_CSS
    obj.css = css
    obj.save()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_update_stylesheet_header_footer_text'),
    ]

    operations = [
        # ── Footer ────────────────────────────────────────────────────────────
        migrations.RemoveField(model_name='footer', name='background_color'),
        migrations.AddField(
            model_name='footer',
            name='text',
            field=models.TextField(
                blank=True,
                help_text='Text displayed in the footer (supports Markdown)',
            ),
        ),
        migrations.AddField(
            model_name='footer',
            name='image',
            field=models.ImageField(
                blank=True, null=True,
                upload_to='footer/',
                help_text='Optional image displayed in the footer',
            ),
        ),

        # ── HeaderSettings ────────────────────────────────────────────────────
        migrations.RemoveField(model_name='headersettings', name='background_color'),
        migrations.AddField(
            model_name='headersettings',
            name='text',
            field=models.TextField(
                blank=True,
                help_text='Text displayed in a banner below the navbar (supports Markdown)',
            ),
        ),
        migrations.AddField(
            model_name='headersettings',
            name='image',
            field=models.ImageField(
                blank=True, null=True,
                upload_to='header/',
                help_text='Optional banner image displayed below the navbar',
            ),
        ),

        # ── Stylesheet data patch ─────────────────────────────────────────────
        migrations.RunPython(update_stylesheet, no_op),
    ]
