from .models import Footer

def footer_content(request):
    footer = Footer.objects.first()
    return {
        'footer': footer
    }