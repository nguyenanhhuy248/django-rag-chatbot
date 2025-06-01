"""
RAG pipeline for chat using DeepSeek API and document retriever.
Default LLM: Together Llama-3.3-70B-Instruct-Turbo-Free
"""
from __future__ import annotations

from typing import Callable

from chat.chat_client import ChatClient
from documents.processors import DocumentProcessor


def chat_client(prompt: str, api_key: str | None = None, model: str | None = None) -> str:
    """Send a chat prompt to the model and return the response."""
    client = ChatClient(api_key=api_key, model=model)
    return client.chat(prompt)


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
            'Context:\n{context}\n\nQuestion: {question}\nAnswer:'
        )

    def rag_fn(question: str) -> str:
        """Retrieve documents and generate an answer using the chat client."""
        docs = retriever(question, 4)
        context = '\n'.join(d['content'] for d in docs)
        prompt = prompt_template.format(context=context, question=question)
        return chat_client(prompt, api_key=api_key, model=model)
    return rag_fn


def get_default_retriever(user_profile=None, model=None):
    """Get the default retriever function for RAG."""
    processor = DocumentProcessor(user_profile=user_profile, model=model)

    def retrieve(query: str, n_results: int = 4):
        return processor.search_similar_chunks(query, n_results)
    return retrieve
