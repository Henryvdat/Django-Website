from django.db import migrations

UPDATED_CSS = """\
/* ============================================================
   GLOBAL / BODY
   ============================================================ */

body {
    background: #f5f5f5;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333333;
}


/* ============================================================
   NAVBAR
   ============================================================ */

/* Site name / logo in the top navbar */
.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}


/* ============================================================
   SIDEBAR NAVIGATION CARD
   ============================================================ */

/* "Navigation" label at the top of the sidebar card */
.card-header {
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Sidebar nav links (Home, About, Products, Contact) */
.list-group-item {
    font-size: 0.95rem;
    color: #444444;
}

.list-group-item:hover {
    color: #000000;
}


/* ============================================================
   PAGE CARDS (home page grid)
   ============================================================ */

.card {
    border: none;
    border-radius: 12px;
}

/* Page title inside each card on the home page */
.card-body h5 {
    font-size: 1.1rem;
    font-weight: 600;
    color: #222222;
}

/* "Read More" button label */
.btn-primary {
    font-size: 0.9rem;
    font-weight: 500;
}


/* ============================================================
   MAIN CONTENT HEADINGS
   ============================================================ */

/* Primary page heading (used on home and page detail) */
h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a2e;
}

/* Section heading (e.g. "Text Blocks" on the home page) */
h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c2c54;
}

/* Text block titles */
h3 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #333333;
}

/* Page card titles inside the card grid */
h5 {
    font-size: 1.05rem;
    font-weight: 600;
    color: #222222;
}


/* ============================================================
   BODY TEXT
   ============================================================ */

/* General paragraph text */
p {
    font-size: 1rem;
    line-height: 1.7;
    color: #444444;
}


/* ============================================================
   TEXT BLOCKS (home page editable blocks)
   ============================================================ */

.block-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 20px;
}

.text-block {
    padding: 20px;
    border-radius: 10px;
}

/* Text block body copy */
.text-block p {
    font-size: 0.95rem;
    color: #555555;
}

/* Edit / Delete links inside each text block */
.text-block a {
    font-size: 0.85rem;
    color: #0d6efd;
    margin-right: 12px;
    text-decoration: none;
}

.text-block a:hover {
    text-decoration: underline;
}

/* ------ Text block style templates ------ */

/* Template: Default — bordered card with light background */
.text-block--default {
    border: 1px solid #cccccc;
    background: #ffffff;
}

/* Template: No Background — clean text only, no border or fill */
.text-block--no_background {
    border: none;
    background: transparent;
    padding: 10px 0;
}

.text-block--no_background h3 {
    color: #1a1a2e;
}

.text-block--no_background p {
    color: #444444;
}

/* Template: Custom Font — large serif display style */
.text-block--custom_font {
    border: none;
    background: #fdfaf5;
    border-left: 4px solid #c8a96e;
}

.text-block--custom_font h3 {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #2c1a00;
    letter-spacing: 0.5px;
}

.text-block--custom_font p {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.05rem;
    line-height: 1.9;
    color: #4a3728;
    font-style: italic;
}


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
}
"""


def update_stylesheet(apps, schema_editor):
    SiteStylesheet = apps.get_model('pages', 'SiteStylesheet')
    obj = SiteStylesheet.objects.first()
    if obj:
        obj.css = UPDATED_CSS
        obj.save()


def no_op(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_textblock_style'),
    ]

    operations = [
        migrations.RunPython(update_stylesheet, no_op),
    ]
