"""Django forms for user authentication and profile management."""
from __future__ import annotations

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import UserProfile


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom form for changing user password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class APIKeyForm(forms.ModelForm):
    """Form for managing API keys in user profile."""
    class Meta:
        model = UserProfile
        fields = ['openai_api_key', 'anthropic_api_key', 'google_api_key']
        widgets = {
            'openai_api_key': forms.PasswordInput(attrs={'class': 'form-control'}),
            'anthropic_api_key': forms.PasswordInput(attrs={'class': 'form-control'}),
            'google_api_key': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
