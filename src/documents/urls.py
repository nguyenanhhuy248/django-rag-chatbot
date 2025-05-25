"""Django URL configuration for the documents app."""
from __future__ import annotations

from django.urls import path

from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('search/', views.search_documents, name='search_documents'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
]
