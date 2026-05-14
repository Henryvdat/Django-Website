"""
Site-wide constants shared between admin, views, and other modules.
"""

DEFAULT_BOOTSTRAP_OVERRIDES = """\
/* ============================================================
   BOOTSTRAP OVERRIDES
   These load after Bootstrap so they always take priority.
   Uncomment any rule to activate it, or add your own below.
   ============================================================ */


/* --- Buttons -------------------------------------------- */

/* .btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
    border-radius: 6px;
} */

/* .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
} */


/* --- Navbar --------------------------------------------- */

/* .navbar.bg-dark {
    background-color: #212529 !important;
} */

/* .navbar-brand {
    font-size: 1.4rem;
    font-weight: 700;
} */


/* --- Cards ---------------------------------------------- */

/* .card {
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
} */

/* .card-header {
    font-weight: 600;
} */


/* --- Links ---------------------------------------------- */

/* a {
    color: #0d6efd;
    text-decoration: none;
} */

/* a:hover {
    text-decoration: underline;
} */


/* --- Typography ----------------------------------------- */

/* body {
    font-size: 1rem;
    line-height: 1.6;
} */

/* h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
} */


/* --- List Group (sidebar nav) --------------------------- */

/* .list-group-item-action:hover {
    background-color: #f0f0f0;
} */


/* --- Badges --------------------------------------------- */

/* .badge.bg-primary {
    background-color: #0d6efd !important;
} */


/* --- Forms ---------------------------------------------- */

/* .form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
} */
"""

# Shared attrs for the monospace CSS textarea used in admin editors.
CSS_TEXTAREA_ATTRS = {
    'style': (
        'font-family: monospace;'
        'font-size: 13px;'
        'width: 100%;'
        'height: 600px;'
        'background: #1e1e1e;'
        'color: #d4d4d4;'
        'border: 1px solid #444;'
        'padding: 12px;'
        'line-height: 1.5;'
    ),
    'spellcheck': 'false',
}
