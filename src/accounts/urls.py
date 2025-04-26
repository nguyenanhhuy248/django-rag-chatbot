"""
URL configuration for the accounts application.

This module defines the URL patterns for user registration and authentication.
"""
from __future__ import annotations

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('settings/', views.account_settings, name='account_settings'),
]
