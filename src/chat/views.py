"""
Views for the chat application.

This module contains views for handling chat functionality including
displaying the chat interface and processing messages.
"""
from __future__ import annotations

import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import ChatMessage
from .rag_pipeline import build_rag_chain
from .rag_pipeline import get_default_retriever


logger = logging.getLogger(__name__)

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


@csrf_exempt
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
            data = json.loads(request.body.decode('utf-8'))
        except Exception as e:  # pylint: disable=broad-except
            logger.error('DEBUG decode error: %s', str(e))
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid JSON data',
                }, status=400,
            )
        user_message = data.get('message', '').strip()

        if user_message:
            # RAG chatbot pipeline
            retriever = get_default_retriever(
                user_profile=getattr(request.user, 'userprofile', None),
            )
            rag_chain = build_rag_chain(retriever)
            bot_response = rag_chain(user_message)

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

    return JsonResponse(
        {
            'status': 'error',
            'message': 'Invalid request method',
        }, status=405,
    )
