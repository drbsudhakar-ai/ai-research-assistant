"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Service
File         : app/services/llm_service.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
    Unified provider abstraction layer for Large Language Models (LLMs).

Responsibilities:
    - Expose a provider-independent interface.
    - Route requests to the configured provider.
    - Hide provider implementation details.
    - Validate provider availability.
    - Support future providers without changing callers.

Current Provider:
    - Ollama

Future Providers:
    - OpenAI
    - Azure OpenAI
    - Gemini
    - Anthropic
    - DeepSeek
    - OpenRouter
    - LM Studio
===============================================================================
"""

from __future__ import annotations

import logging

from app.config.application_config import ApplicationConfig
from app.config.loader import get_application_config
from app.models.llm_response import LLMResponse
from app.services.gemini_service import GeminiService
from app.services.llm_provider import LLMProvider
from app.services.ollama_service import OllamaService

__all__ = [
    "LLMService",
]

_LOGGER = logging.getLogger(__name__)


class LLMService:
    """
    Provider-independent interface for language model services.

    Higher-level application components (PaperAnalyzer, AnalysisService,
    etc.) should communicate only with this class and never directly with
    provider-specific implementations.
    """

    def __init__(
        self,
        provider: LLMProvider | None = None,
    ) -> None:
        """
        Initialize the LLM service.

        Parameters
        ----------
        provider:
            Optional provider implementation. If omitted, the configured
            Ollama provider is used.
        """

        self._provider = provider or self._provider_from_config(
            get_application_config()
        )

    @classmethod
    def from_config(cls, config: ApplicationConfig) -> LLMService:
        """Construct the LLM facade from ApplicationConfig."""

        return cls(provider=cls._provider_from_config(config))

    @staticmethod
    def _provider_from_config(config: ApplicationConfig) -> LLMProvider:
        if config.llm.provider == "gemini":
            return GeminiService.from_config(config)
        return OllamaService.from_config(config)

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def provider(self) -> str:
        """
        Return active provider name.
        """

        return self._provider.provider

    @property
    def model(self) -> str:
        """
        Return active model name.
        """

        return self._provider.model

    # =========================================================================
    # Public API
    # =========================================================================

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        """
        Generate a response using the configured provider.

        Parameters
        ----------
        system_prompt:
            System prompt.

        user_prompt:
            User prompt.

        Returns
        -------
        LLMResponse

        Raises
        ------
        RuntimeError
            If the configured provider is unavailable or generation fails.
        """

        if not self.is_available():
            raise RuntimeError(f"{self.provider} is not available.")

        _LOGGER.info(
            "Generating response using provider='%s', model='%s'.",
            self.provider,
            self.model,
        )

        return self._provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

    def is_available(self) -> bool:
        """
        Check whether the configured provider is available.

        Returns
        -------
        bool
        """

        return self._provider.is_available()

    def list_models(self) -> list[str]:
        """
        Return installed/available models.

        Returns
        -------
        list[str]
        """

        if hasattr(self._provider, "list_models"):
            return self._provider.list_models()

        return []

    def model_exists(
        self,
        model: str,
    ) -> bool:
        """
        Determine whether a model exists.

        Parameters
        ----------
        model:
            Model name.

        Returns
        -------
        bool
        """

        if hasattr(self._provider, "model_exists"):
            return self._provider.model_exists(model)

        return False

    def health_check(self) -> bool:
        """
        Perform a lightweight provider health check.

        Returns
        -------
        bool
        """

        try:
            return self.is_available()

        except Exception:

            _LOGGER.exception("LLM provider health check failed.")

            return False

    def __repr__(self) -> str:
        """
        Return developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"provider={self.provider!r}, "
            f"model={self.model!r})"
        )
