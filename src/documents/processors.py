"""Document processing utilities."""
from __future__ import annotations

import os
from typing import Any

import chromadb
import torch
from accounts.models import UserProfile
from chromadb.config import Settings
from config import dynaconf_settings
from django.conf import settings as django_settings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from semantic_text_splitter.semantic_text_splitter import TextSplitter  # pylint: disable=E0611
from unstructured.partition.auto import partition

from .models import Document
from .models import DocumentChunk

chromadb.api.client.SharedSystemClient.clear_system_cache()


class DocumentProcessor:
    """Handles document processing, chunking, and embedding."""

    def __init__(self, user_profile: UserProfile | None = None, model: str | None = None):
        """Initialize the document processor.

        Args:
            user_profile: Optional UserProfile instance containing API keys.
            model: Optional model identifier to use for embeddings.
        """
        self.user_profile = user_profile
        self.model = model
        self.embeddings = self._setup_embeddings()
        self.chroma_client = chromadb.Client(
            Settings(
                is_persistent=True,
                persist_directory=os.path.join(django_settings.BASE_DIR, 'chroma_db'),
            ),
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name='documents',
            metadata={'hnsw:space': 'cosine'},
        )

    def _setup_embeddings(self) -> Any:
        """Set up embeddings with available API keys."""
        model_configs = dynaconf_settings.get('model_configs', {})
        if not self.model or self.model not in model_configs:
            # Default to all-MiniLM-L6-v2 if no model specified or invalid
            self.model = 'all-MiniLM-L6-v2'

        model_config = dynaconf_settings.get('model_configs', {}).get(self.model, {})

        if self.model == 'all-MiniLM-L6-v2':
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

            return HuggingFaceEmbeddings(
                model_name=model_config.get('name', 'all-MiniLM-L6-v2'),
                model_kwargs={
                    'device': device,
                },
                encode_kwargs={
                    'normalize_embeddings': model_config.get('normalize_embeddings', True),
                    'convert_to_tensor': True,
                },
            )

        # For API-based models
        api_key = None
        if self.user_profile:
            api_key = getattr(self.user_profile, model_config.get('key_field', ''))

        return OpenAIEmbeddings(
            openai_api_key=api_key,
            model=model_config.get('name', 'text-embedding-3-small'),
        )

    def process_document(self, document: Document) -> None:
        """Process a document: extract text, chunk, embed, and store."""
        try:
            document.processing_status = 'processing'
            document.save()

            # Extract text from document
            elements = partition(filename=document.file.path)
            text = '\n'.join([str(el) for el in elements])

            # Split text into chunks
            splitter = TextSplitter(capacity=1000)
            chunks = splitter.chunks(text)

            # Create document chunks and store embeddings
            for i, chunk in enumerate(chunks):
                # Generate embedding using LangChain
                embedding = self.embeddings.embed_query(chunk)

                # Store in ChromaDB
                self.collection.add(
                    ids=[f'{document.id}_{i}'],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        'document_id': document.id,
                        'chunk_index': i,
                        'filename': document.get_filename(),
                        'model': self.model,
                    }],
                )

                # Store in Django database
                DocumentChunk.objects.create(
                    document=document,
                    content=chunk,
                    chunk_index=i,
                    metadata={
                        'filename': document.get_filename(),
                        'chunk_size': len(chunk),
                        'model': self.model,
                    },
                )

            document.processing_status = 'completed'
            document.metadata = {
                'num_chunks': len(chunks),
                'total_chars': sum(len(chunk) for chunk in chunks),
                'model': self.model,
            }
            document.save()

        except Exception as e:
            document.processing_status = 'failed'
            document.processing_error = str(e)
            document.save()
            raise

    def search_similar_chunks(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Search for similar chunks using the query."""
        query_embedding = self.embeddings.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )

        return [
            {
                'content': doc,
                'metadata': meta,
                'distance': dist,
            }
            for doc, meta, dist in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0],
            )
        ]
