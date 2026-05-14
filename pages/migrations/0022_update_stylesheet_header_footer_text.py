"""
Data migration: add explicit colour and font rules for the header (navbar) and
footer text so they are visible and editable in the Site Stylesheet admin.
"""
from django.db import migrations

# ── Replacement NAVBAR section ────────────────────────────────────────────────
OLD_NAVBAR = """\
/* ============================================================
   NAVBAR
   ============================================================ */

/* Site name / logo in the top navbar */
.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}"""

NEW_NAVBAR = """\
/* ============================================================
   NAVBAR / HEADER
   Edit these rules to change the header text font and colour.
   The background colour is set separately in Page Settings →
   Header Settings.
   ============================================================ */

/* Site name text in the top navbar */
.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #ffffff;
}

/* Navbar links (if any are added in the future) */
.navbar-nav .nav-link {
    color: rgba(255, 255, 255, 0.85);
    font-size: 0.95rem;
}

.navbar-nav .nav-link:hover {
    color: #ffffff;
}"""

# ── Replacement FOOTER section ────────────────────────────────────────────────
OLD_FOOTER = """\
/* ============================================================
   FOOTER
   ============================================================ */

footer {
    background-color: #1a1a2e;
    text-align: center;
}

/* Main footer message text */
footer p {
    color: #ffffff;
    font-size: 0.95rem;
}

/* Copyright line */
footer small {
    color: #ffffff;
    font-size: 0.8rem;
}"""

NEW_FOOTER = """\
/* ============================================================
   FOOTER
   Edit these rules to change the footer text font and colour.
   The background colour is set separately in Page Settings →
   Footer Settings.
   ============================================================ */

footer {
    text-align: center;
}

/* Footer text block content */
footer p,
footer li {
    color: #ffffff;
    font-size: 0.95rem;
    font-family: inherit;
}

/* Footer headings (if used inside text blocks) */
footer h1, footer h2, footer h3,
footer h4, footer h5, footer h6 {
    color: #ffffff;
}

/* Copyright line */
footer small {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.8rem;
}"""


def update_stylesheet(apps, schema_editor):
    SiteStylesheet = apps.get_model('pages', 'SiteStylesheet')
    obj = SiteStylesheet.objects.first()
    if obj:
        css = obj.css
        if OLD_NAVBAR in css:
            css = css.replace(OLD_NAVBAR, NEW_NAVBAR)
        if OLD_FOOTER in css:
            css = css.replace(OLD_FOOTER, NEW_FOOTER)
        obj.css = css
        obj.save()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_add_header_settings_update_footer_textblock_location'),
    ]

    operations = [
        migrations.RunPython(update_stylesheet, no_op),
    ]
