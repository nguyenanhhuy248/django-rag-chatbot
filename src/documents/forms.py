"""Django form for document management."""
from __future__ import annotations

from django import forms

from .models import Document


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""
    EMBEDDING_MODEL_CHOICES = [
        ('All-MiniLM-L6-v2', 'All-MiniLM-L6-v2 (Default)'),
        ('openai', 'OpenAI - text-embedding-3-small'),
    ]

    embedding_model = forms.ChoiceField(
        choices=EMBEDDING_MODEL_CHOICES,
        required=True,
        initial='All-MiniLM-L6-v2',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Document
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
            'multiple': True,
        })
