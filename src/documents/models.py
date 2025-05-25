"""Models for document management app."""
from __future__ import annotations

import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Document(models.Model):
    """Document model for storing uploaded files."""
    PROCESSING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.BigIntegerField(help_text='File size in bytes')
    file_type = models.CharField(max_length=100)
    processing_status = models.CharField(
        max_length=20,
        choices=PROCESSING_STATUS_CHOICES,
        default='pending',
    )
    processing_error = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.get_filename()

    def get_filename(self):
        """Return the name of the file."""
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        """Override save method to set file size and type."""
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)


class DocumentChunk(models.Model):
    """Model for storing document chunks with embeddings."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()
    embedding = models.JSONField(help_text='Vector embedding of the chunk')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['chunk_index']
        unique_together = ['document', 'chunk_index']

    def __str__(self):
        return f'Chunk {self.chunk_index} of {self.document.get_filename()}'
