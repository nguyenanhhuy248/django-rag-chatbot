"""
Django application configuration for the chat app.

This module contains the configuration for the chat application,
which handles the chat interface and message processing.
"""
from __future__ import annotations

from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    Configuration class for the chat application.

    This class defines the configuration for the chat app,
    including its name and any app-specific settings.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
