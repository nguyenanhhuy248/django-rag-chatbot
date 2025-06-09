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
from .models import Conversation
from .rag_pipeline import build_rag_chain
from .rag_pipeline import get_default_retriever


logger = logging.getLogger(__name__)

# Create your views here.


@login_required
def chat_home(request):
    """
    Display the chat interface with conversation list and selected conversation messages.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered template with chat messages.
    """
    conversations = Conversation.objects.filter(user=request.user).order_by('-created_at')
    selected_conversation_id = request.GET.get('conversation')
    if selected_conversation_id:
        try:
            selected_conversation = conversations.get(pk=selected_conversation_id)
        except Conversation.DoesNotExist:
            selected_conversation = conversations.first()
    else:
        selected_conversation = conversations.first()
    messages = (
        selected_conversation.messages.order_by('timestamp') if selected_conversation else []
    )
    # Prepare a list of (conversation, first_msg) for the sidebar
    conversation_previews = [
        (conv, conv.messages.order_by('timestamp').first())
        for conv in conversations
    ]
    return render(
        request, 'chat/chat_home.html', {
            'conversations': conversations,
            'selected_conversation': selected_conversation,
            'messages': messages,
            'conversation_previews': conversation_previews,
        },
    )


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
        conversation_id = data.get('conversation_id')
        conversation = None
        if conversation_id:
            try:
                conversation = Conversation.objects.get(pk=conversation_id, user=request.user)
            except Conversation.DoesNotExist:
                pass
        if not conversation:
            conversation = Conversation.objects.create(user=request.user)
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
                conversation=conversation,
            )

            return JsonResponse({
                'status': 'success',
                'response': bot_response,
                'timestamp': chat_message.timestamp.strftime(
                    '%Y-%m-%d %H:%M:%S',
                ),
                'conversation_id': conversation.id,
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


@login_required
def get_conversation_messages(request, conversation_id):
    """
    Return messages for a given conversation (AJAX endpoint).

    Args:
        request: The HTTP request object.
        conversation_id: The ID of the conversation to retrieve messages for.

    Returns:
        JsonResponse with the conversation messages or error message.
    """
    try:
        conversation = Conversation.objects.get(pk=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Conversation not found'}, status=404)
    messages = [
        {
            'id': m.id,
            'message': m.message,
            'response': m.response,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for m in conversation.messages.order_by('timestamp')
    ]
    return JsonResponse({'status': 'success', 'messages': messages})


@login_required
def delete_conversation(request, conversation_id):
    """
    Delete a conversation and all its messages.
    """
    if request.method == 'POST':
        try:
            conversation = Conversation.objects.get(pk=conversation_id, user=request.user)
            conversation.delete()
            return JsonResponse({'status': 'success'})
        except Conversation.DoesNotExist:
            return JsonResponse(
                {'status': 'error', 'message': 'Conversation not found'},
                status=404,
            )
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
