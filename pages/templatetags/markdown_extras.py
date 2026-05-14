import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdown', is_safe=True)
def markdown_filter(value):
    """Convert Markdown text to HTML."""
    if not value:
        return ''
    extensions = ['extra', 'sane_lists']
    result = md.markdown(str(value), extensions=extensions)
    return mark_safe(result)


@register.simple_tag
def render_content(content, content_format):
    """
    Render page/block content respecting its stored format.
    - 'markdown'  → runs through the markdown pipeline
    - 'html'      → returned as-is (trusted staff-only input)
    """
    if not content:
        return mark_safe('')
    if content_format == 'html':
        return mark_safe(content)
    # default: markdown
    extensions = ['extra', 'sane_lists']
    result = md.markdown(str(content), extensions=extensions)
    return mark_safe(result)
