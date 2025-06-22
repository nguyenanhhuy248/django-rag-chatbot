"""
RAG pipeline for chat using DeepSeek API and document retriever.
Default LLM: Together Llama-3.3-70B-Instruct-Turbo-Free
"""
from __future__ import annotations

from typing import Callable

import requests
from chat.chat_client import ChatClient
from config.config import dynaconf_settings
from documents.processors import DocumentProcessor


def chat_client(prompt: str, api_key: str | None = None, model: str | None = None) -> str:
    """Send a chat prompt to the model and return the response."""
    client = ChatClient(api_key=api_key, model=model)
    return client.chat(prompt)


def rerank_with_hfei(query: str, docs: list[dict], endpoint: str) -> list[dict]:
    """
    Rerank retrieved docs using a local HuggingFace Embedding Inference (HFEI)
    reranker server.
    """
    if not docs:
        return []
    payload = {
        'query': query,
        'documents': [d['content'] for d in docs],
    }
    response = requests.post(endpoint, json=payload, timeout=10)
    response.raise_for_status()
    ranks = response.json().get('scores', [])
    # Pair each doc with its score, then sort
    reranked = sorted(zip(docs, ranks), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in reranked]


def build_rag_chain(
    retriever: Callable[[str, int], list[dict]],
    api_key: str | None = None,
    prompt_template: str | None = None,
    model: str | None = None,
) -> Callable[[str], str]:
    """Build a RAG chain callable: question -> answer."""
    if prompt_template is None:
        prompt_template = (
            'You are a helpful assistant. Use the following context to answer the question.\n'
            'When referencing information from the context, '
            'please cite the source and include relevant quotes.\n\n'
            'For example:\n'
            '   Source: [Document Name]\n'
            '   Quote: "[relevant quote]"\n'
            'You should use markdown formatting for emphasis:\n'
            '   - Use **text** for bold\n'
            '   - Use *text* for italic\n'
            '   - Use `text` for code\n'
            'Context:\n{context}\n\n'
            'Question: {question}\n\n'
            'Answer:'
        )

    use_hfei_reranker = dynaconf_settings.get('use_hfei_reranker', False)

    def rag_fn(question: str) -> str:
        """
        Retrieve documents, rerank (if enabled), and generate an answer using the chat client.
        """
        docs = retriever(question, 4)
        if use_hfei_reranker:
            docs = rerank_with_hfei(
                question, docs, endpoint=dynaconf_settings.get('hfei_endpoint'),
            )
        context = '\n'.join(
            f"Document: {d['metadata'].get('filename', 'Unknown')}\nContent: {d['content']}"
            for d in docs
        )
        prompt = prompt_template.format(context=context, question=question)
        return chat_client(prompt, api_key=api_key, model=model)
    return rag_fn


def get_default_retriever(user_profile=None, model=None):
    """Get the default retriever function for RAG."""
    processor = DocumentProcessor(user_profile=user_profile, model=model)

    def retrieve(query: str, n_results: int = 4):
        return processor.search_similar_chunks(query, n_results)
    return retrieve
