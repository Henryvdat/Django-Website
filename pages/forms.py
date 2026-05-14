from django import forms
from .models import Page, TextBlock


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'content_format', 'published']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control markdown-editor',
                'rows': 16,
                'id': 'id_page_content',
            }),
            'content_format': forms.HiddenInput(attrs={'id': 'id_page_content_format'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TextBlockForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ['title', 'content', 'content_format', 'style']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'content':     forms.Textarea(attrs={
                'class': 'form-control markdown-editor',
                'rows': 10,
                'id': 'id_block_content',
            }),
            'content_format': forms.HiddenInput(attrs={'id': 'id_block_content_format'}),
            'style':       forms.Select(attrs={'class': 'form-select'}),
        }
