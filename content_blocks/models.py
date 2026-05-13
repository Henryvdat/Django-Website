from pages.models import TextBlock, Footer


class TextBlockContent(TextBlock):
    class Meta:
        proxy = True
        app_label = 'content_blocks'
        verbose_name = 'Text Block'
        verbose_name_plural = 'Text Blocks'


class FooterContent(Footer):
    class Meta:
        proxy = True
        app_label = 'content_blocks'
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'
