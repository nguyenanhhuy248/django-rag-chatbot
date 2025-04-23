"""
Views for the chat application.

This module contains views for handling chat functionality including
displaying the chat interface and processing messages.
"""
from __future__ import annotations

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import ChatMessage

# Create your views here.


@login_required
def chat_home(request):
    """
    Display the chat interface.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered template with chat messages.
    """
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chat/chat_home.html', {'messages': messages})


@login_required
def send_message(request):
    """
    Process and respond to chat messages.

    Args:
        request: The HTTP request object containing the message.

    Returns:
        JsonResponse with the bot's response or error message.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if user_message:
                # Placeholder for chatbot/LLM service
                bot_response = 'Bot response'

                # Save the message and response
                chat_message = ChatMessage.objects.create(
                    user=request.user,
                    message=user_message,
                    response=bot_response,
                )

                return JsonResponse({
                    'status': 'success',
                    'response': bot_response,
                    'timestamp': chat_message.timestamp.strftime(
                        '%Y-%m-%d %H:%M:%S',
                    ),
                })

            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Message cannot be empty',
                }, status=400,
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid JSON data',
                }, status=400,
            )

    return JsonResponse(
        {
            'status': 'error',
            'message': 'Invalid request method',
        }, status=405,
    )
