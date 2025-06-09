"""
URL configuration for the chat application.

This module defines the URL patterns for the chat interface and message handling.
"""
from __future__ import annotations

from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('send_message/', views.send_message, name='send_message'),
    path(
        'conversation/<int:conversation_id>/',
        views.get_conversation_messages, name='get_conversation_messages',
    ),
    path(
        'conversation/<int:conversation_id>/delete/',
        views.delete_conversation, name='delete_conversation',
    ),
]
