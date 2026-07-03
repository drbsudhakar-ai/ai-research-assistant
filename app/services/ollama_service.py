"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Service
File         : ollama_service.py
Version      : 1.2.0
Author       : Dr. B. Sudhakar

Description:
    Service responsible for communication with Ollama.

Responsibilities:
    - Generate responses from local language models.
    - Check Ollama server availability.
    - Discover installed models.
    - Validate configured models.
    - Hide provider-specific implementation.

Notes:
    - This module is the only place that imports the Ollama SDK.
    - Business logic must not be implemented here.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import ollama

from app.config.llm_config import (
    MODEL_NAME,
    PROVIDER_NAME,
    TEMPERATURE,
)

__all__ = [
    "LLMResponse",
    "OllamaService",
]


# =============================================================================
# Data Models
# =============================================================================


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """
    Standard response returned by a language model.
    """

    content: str
    model: str
    provider: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


# =============================================================================
# Ollama Service
# =============================================================================


class OllamaService:
    """
    Service responsible for communication with Ollama.
    """

    def __init__(
        self,
        model: str = MODEL_NAME,
    ) -> None:
        """
        Initialize the Ollama service.

        Parameters
        ----------
        model : str, optional
            Model name to use.
        """

        self._model = model
        self._provider = PROVIDER_NAME

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def model(self) -> str:
        """
        Return configured model.
        """
        return self._model

    @property
    def provider(self) -> str:
        """
        Return provider name.
        """
        return self._provider

    # =========================================================================
    # Public API
    # =========================================================================

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        """
        Generate a response from the configured model.

        Parameters
        ----------
        system_prompt : str
            System prompt.

        user_prompt : str
            User prompt.

        Returns
        -------
        LLMResponse
            Generated response.

        Raises
        ------
        RuntimeError
            If generation fails.
        """

        if not self.model_exists(self._model):
            raise RuntimeError(
                f"Ollama model '{self._model}' is not installed."
            )

        try:

            response: dict[str, Any] = ollama.chat(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                options={
                    "temperature": TEMPERATURE,
                },
            )

            message = response.get("message")

            if message is None:
                raise RuntimeError(
                    "Invalid response received from Ollama."
                )

            content = message.get("content", "").strip()

            if not content:
                raise RuntimeError(
                    "Ollama returned an empty response."
                )

            prompt_tokens = response.get("prompt_eval_count")
            completion_tokens = response.get("eval_count")

            total_tokens = None

            if (
                prompt_tokens is not None
                and completion_tokens is not None
            ):
                total_tokens = (
                    prompt_tokens + completion_tokens
                )

            return LLMResponse(
                content=content,
                model=self._model,
                provider=self._provider,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
            )

        except Exception as exc:
            raise RuntimeError(
                f"Ollama generation failed: {exc}"
            ) from exc

    def list_models(self) -> list[str]:
        """
        Return installed Ollama models.

        Returns
        -------
        list[str]
            Installed model names.
        """

        try:

            response: dict[str, Any] = ollama.list()

            models = response.get("models", [])

            model_names: list[str] = []

            for model in models:

                name = (
                    model.get("model")
                    or model.get("name")
                )

                if name:
                    model_names.append(name)

            return sorted(model_names)

        except Exception:
            return []

    def model_exists(
        self,
        model: str,
    ) -> bool:
        """
        Check whether a model is installed.

        Parameters
        ----------
        model : str

        Returns
        -------
        bool
        """

        return model in self.list_models()

    def is_available(self) -> bool:
        """
        Check whether the Ollama server is reachable.

        Returns
        -------
        bool
        """

        try:

            ollama.list()

            return True

        except Exception:

            return False

    def get_model(self) -> str:
        """
        Return configured model name.
        """

        return self._model

    def get_provider(self) -> str:
        """
        Return configured provider name.
        """

        return self._provider