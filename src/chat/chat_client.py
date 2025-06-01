"""Chat Client Module"""
from __future__ import annotations

from config.config import dynaconf_settings
from openai import OpenAI


class ChatClient:
    """Client for interacting with chat models via OpenRouter API."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.model = model or dynaconf_settings.model_configs.chat_model
        self.api_key = api_key or dynaconf_settings.chat_model_api_key.api_key
        if not self.api_key:
            raise ValueError(f'API key is required for {self.model}.')
        self.model_version = dynaconf_settings.model_configs[self.model].version
        self.api_url = dynaconf_settings.model_configs[self.model].api_url
        self.client = OpenAI(
            base_url=self.api_url,
            api_key=self.api_key,
        )

    def chat(self, prompt: str) -> str:
        """Send a chat prompt to the model and return the response."""
        completion = self.client.chat.completions.create(
            extra_body={},
            model=f'{self.model}/{self.model_version}',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        return completion.choices[0].message.content
