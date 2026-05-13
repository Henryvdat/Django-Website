from django import forms
from .models import TextBlock

class TextBlockForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ['title', 'content', 'style']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'style':   forms.Select(attrs={'class': 'form-select'}),
        }