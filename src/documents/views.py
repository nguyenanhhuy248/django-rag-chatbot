"""
Views for the documents application.

This module contains the views for the documents application.
"""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import DocumentUploadForm
from .models import Document

# Create your views here.


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
            for file in files:
                document = Document(
                    file=file,
                    uploaded_by=request.user,
                )
                document.save()
            messages.success(request, f'{len(files)} document(s) uploaded successfully!')
            return redirect('documents:document_list')
    else:
        form = DocumentUploadForm()

    return render(
        request, 'documents/document_list.html', {
            'page_obj': page_obj,
            'form': form,
        },
    )
