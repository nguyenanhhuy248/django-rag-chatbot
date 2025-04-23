"""
Admin configuration for the chat application.

This module registers the ChatMessage model with the Django admin interface.
"""
from __future__ import annotations

from django.contrib import admin

from .models import ChatMessage

# Register your models here.

admin.site.register(ChatMessage)
