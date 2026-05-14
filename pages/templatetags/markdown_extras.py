import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdown', is_safe=True)
def markdown_filter(value):
    """Convert Markdown text to HTML."""
    if not value:
        return ''
    extensions = ['extra', 'nl2br', 'sane_lists']
    result = md.markdown(str(value), extensions=extensions)
    return mark_safe(result)
