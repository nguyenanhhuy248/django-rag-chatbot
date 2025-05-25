"""
Models for the accounts application.

This module contains the database models for user accounts.
"""
from __future__ import annotations

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    User profile model to store additional information about users.
    This model extends the default User model to include API keys for various services.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    openai_api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile when a new user is created.
    Args:
        sender: The model class.
        instance: The instance being saved.
        created: Boolean indicating if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the user profile when the user instance is saved.
    Args:
        sender: The model class.
        instance: The instance being saved.
        **kwargs: Additional keyword arguments.
    """
    instance.userprofile.save()
