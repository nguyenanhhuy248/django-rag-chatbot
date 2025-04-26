"""Django form for document management."""
from __future__ import annotations

from django import forms

from .models import Document


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""
    class Meta:
        model = Document
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
            'multiple': True,
        })
