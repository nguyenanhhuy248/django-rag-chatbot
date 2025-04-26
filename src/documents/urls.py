"""Django URL configuration for the documents app."""
from __future__ import annotations

from django.urls import path

from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='document_list'),
]
