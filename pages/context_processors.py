from .models import Footer, SiteSettings

def footer_content(request):
    footer = Footer.objects.first()
    site_settings = SiteSettings.objects.first()
    return {
        'footer': footer,
        'site_settings': site_settings,
    }