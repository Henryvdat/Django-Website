from pages.models import TextBlock


class TextBlockContent(TextBlock):
    class Meta:
        proxy = True
        app_label = 'content_blocks'
        verbose_name = 'Text Block'
        verbose_name_plural = 'Text Blocks'


class FooterTextBlock(TextBlock):
    """Proxy of TextBlock scoped to blocks with location='footer'."""
    class Meta:
        proxy = True
        app_label = 'content_blocks'
        verbose_name = 'Footer Text Block'
        verbose_name_plural = 'Footer Text Blocks'
