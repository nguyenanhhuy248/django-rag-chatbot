"""
Views for the documents application.

This module contains the views for the documents application.
"""
from __future__ import annotations

import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import DocumentUploadForm
from .models import Document
from .processors import DocumentProcessor

# Create your views here.

os.environ['TOKENIZERS_PARALLELISM'] = 'false'


@login_required
def document_list(request):
    """
    View for displaying a list of documents uploaded by the current user.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered HTML template with the list of documents.
    """

    # Filter documents to show only those uploaded by the current user
    documents = Document.objects.filter(uploaded_by=request.user)
    paginator = Paginator(documents, 10)  # Show 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            embedding_model = form.cleaned_data['embedding_model']

            for file in files:
                document = Document(
                    file=file,
                    uploaded_by=request.user,
                )
                document.save()
                # Start document processing with user profile and selected model
                processor = DocumentProcessor(
                    user_profile=request.user.userprofile,
                    model=embedding_model,
                )
                processor.process_document(document)
            messages.success(request, f'{len(files)} document(s) uploaded successfully!')
            return redirect('documents:document_list')
    else:
        form = DocumentUploadForm()

    # Get available models based on user's API keys
    available_models = [('All-MiniLM-L6-v2', 'All-MiniLM-L6-v2 (Default)')]
    if request.user.userprofile.openai_api_key:
        available_models.append(('openai', 'OpenAI - text-embedding-3-small'))

    # Update form choices with available models
    form.fields['embedding_model'].choices = available_models

    return render(
        request, 'documents/document_list.html', {
            'page_obj': page_obj,
            'form': form,
            'available_models': available_models,
        },
    )


@login_required
@require_POST
def search_documents(request):
    """Search for similar document chunks."""
    query = request.POST.get('query', '')
    model = request.POST.get('model', '')
    if not query:
        return JsonResponse({'error': 'Query is required'}, status=400)

    processor = DocumentProcessor(
        user_profile=request.user.userprofile,
        model=model if model else None,
    )
    results = processor.search_similar_chunks(query)

    return JsonResponse({
        'results': results,
    })


@login_required
@require_POST
def delete_document(request, document_id):
    """Delete a document and its associated chunks."""
    try:
        document = Document.objects.get(id=document_id, uploaded_by=request.user)
        document.delete()  # This will also delete associated chunks due to CASCADE
        messages.success(request, 'Document deleted successfully.')
    except Document.DoesNotExist:
        messages.error(request, 'Document not found.')
    return redirect('documents:document_list')
