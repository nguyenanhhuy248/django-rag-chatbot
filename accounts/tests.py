"""
Tests for the accounts application.

This module contains test cases for user registration and authentication.
"""
from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class UserRegistrationTest(TestCase):
    """Test cases for user registration functionality."""

    def test_user_registration(self):
        """Test that a user can register successfully."""
        response = self.client.post(
            reverse('accounts:register'),
            {
                'username': 'testuser',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
