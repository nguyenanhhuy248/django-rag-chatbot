"""
Models for the chat application.

This module contains the database models for storing chat messages.
"""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Conversation(models.Model):
    """
    Model representing a chat conversation.

    Attributes:
        user: The user who owns the conversation
        created_at: When the conversation was created
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        first_message = self.chatmessage_set.order_by('timestamp').first()
        if first_message:
            preview = first_message.message.split()
            preview = ' '.join(preview[:5]) + ('...' if len(preview) > 4 else '')
            return f'{self.user.username}: {preview}'
        return f'{self.user.username}: Conversation {self.pk}'


class ChatMessage(models.Model):
    """
    Model representing a chat message and its response.

    Attributes:
        user: The user who sent the message
        message: The content of the user's message
        response: The bot's response to the message
        timestamp: When the message was created
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True,
    )
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadata for the ChatMessage model."""
        ordering = ['-timestamp']

    def __str__(self):
        """Return a string representation of the message."""
        return f'{self.user.username} - {self.timestamp}'
