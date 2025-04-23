"""
Views for the accounts application.

This module contains views for handling user registration and authentication.
"""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render

# Create your views here.


def register(request):
    """
    Handle user registration.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered registration form or redirects to chat home on success.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('chat:chat_home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
