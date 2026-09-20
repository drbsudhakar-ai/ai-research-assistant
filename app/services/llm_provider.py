"""Structural contract implemented by language-model provider adapters."""

from __future__ import annotations

from typing import Protocol

from app.models.llm_response import LLMResponse


class LLMProvider(Protocol):
    """Minimum provider interface consumed by :class:`LLMService`."""

    @property
    def provider(self) -> str: ...

    @property
    def model(self) -> str: ...

    def generate(self, *, system_prompt: str, user_prompt: str) -> LLMResponse: ...

    def is_available(self) -> bool: ...

    def list_models(self) -> list[str]: ...

    def model_exists(self, model: str) -> bool: ...
