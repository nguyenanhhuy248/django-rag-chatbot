"""
Configuration for the documents application.

This module contains the configuration for the documents application.
"""
from __future__ import annotations

from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    """Configuration class for the documents application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'documents'
