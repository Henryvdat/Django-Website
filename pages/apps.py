from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name         = 'pages'
    verbose_name = 'Page Settings'

    def ready(self):
        import pages.signals  # noqa: F401 — registers cache-invalidation signal receivers
