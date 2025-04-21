"""
Tests for the chat application.

This module contains test cases for chat functionality.
"""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ChatMessage


User = get_user_model()


class ChatTest(TestCase):
    """Test cases for chat functionality."""

    def setUp(self):
        """Set up test user and login."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )
        self.client.login(username='testuser', password='testpassword123')

    def test_chat_home(self):
        """Test that the chat home page loads successfully."""
        response = self.client.get(reverse('chat:chat_home'))
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        """Test that a message can be sent successfully."""
        response = self.client.post(
            reverse('chat:send_message'),
            {'message': 'Hello, bot!'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ChatMessage.objects.filter(
                user=self.user,
                message='Hello, bot!',
            ).exists(),
        )
