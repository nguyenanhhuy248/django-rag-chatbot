"""
Django application configuration for the accounts app.

This module contains the configuration for the accounts application,
which handles user registration and authentication.
"""
from __future__ import annotations

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the accounts application.

    This class defines the configuration for the accounts app,
    including its name and any app-specific settings.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
