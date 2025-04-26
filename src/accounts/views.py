"""
Views for the accounts application.

This module contains views for handling user registration and authentication.
"""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import APIKeyForm
from .forms import CustomPasswordChangeForm

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


@login_required
def account_settings(request):
    """
    Handle account settings, including password change and API key management.
    Args:
        request: The HTTP request object.
    Returns:
        Rendered account settings page with forms for password change and API key management.
    """
    if request.method == 'POST':
        if 'password_change' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('accounts:account_settings')
        elif 'api_keys' in request.POST:
            api_form = APIKeyForm(request.POST, instance=request.user.userprofile)
            if api_form.is_valid():
                api_form.save()
                messages.success(request, 'API keys updated successfully!')
                return redirect('accounts:account_settings')
    else:
        password_form = CustomPasswordChangeForm(request.user)
        api_form = APIKeyForm(instance=request.user.userprofile)

    return render(
        request, 'accounts/account_settings.html', {
            'password_form': password_form,
            'api_form': api_form,
        },
    )
