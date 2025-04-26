"""Models for document management app."""
from __future__ import annotations

import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Document(models.Model):
    """Document model for storing uploaded files."""
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_size = models.BigIntegerField(help_text='File size in bytes')
    file_type = models.CharField(max_length=100)

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
