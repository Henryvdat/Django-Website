from django import forms
from .models import TextBlock

class TextBlockForm(forms.ModelForm):
    class Meta:
        model = TextBlock
        fields = ['title', 'content']