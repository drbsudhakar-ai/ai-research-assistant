"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Service
File         : app/services/ollama_service.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
    Production-ready service responsible for communication with Ollama.

Responsibilities:
    - Generate responses from local language models.
    - Check Ollama server availability.
    - Discover installed models.
    - Validate configured models.
    - Retry transient failures.
    - Validate responses.
    - Hide provider-specific implementation.

Notes:
    - This is the only module that imports the Ollama SDK.
    - No business logic belongs here.
    - Provider-independent orchestration belongs in LLMService.
===============================================================================
"""

from __future__ import annotations

from time import perf_counter
from typing import Any
import logging
import time

import ollama

from app.config.application_config import ApplicationConfig
from app.config.llm_config import (
    MODEL_NAME,
    PROVIDER_NAME,
    TEMPERATURE,
)
from app.models.llm_response import LLMResponse

__all__ = [
    "OllamaService",
]


# =============================================================================
# Configuration
# =============================================================================

_LOGGER = logging.getLogger(__name__)

_DEFAULT_RETRIES = 3

_RETRY_DELAY_SECONDS = 1.0

_MIN_RESPONSE_LENGTH = 20


# =============================================================================
# Ollama Service
# =============================================================================


class OllamaService:
    """
    Service responsible for all communication with Ollama.

    Responsibilities
    ----------------
    * Send prompts to Ollama.
    * Validate responses.
    * Handle transient failures.
    * Provide model discovery.
    * Check server availability.

    This class intentionally contains no application business logic.
    """

    def __init__(
        self,
        model: str = MODEL_NAME,
        *,
        temperature: float = TEMPERATURE,
        retries: int = _DEFAULT_RETRIES,
        base_url: str = "http://localhost:11434",
        timeout: int = 120,
        developer_mode: bool = False,
        top_p: float = 0.95,
        max_tokens: int | None = None,
        provider: str = PROVIDER_NAME,
    ) -> None:
        """
        Initialize the service from explicit constructor arguments.

        Do not read environment variables here. Pass values from
        ApplicationConfig via ``from_config``.
        """

        self._provider = provider
        self._model = model
        self._temperature = temperature
        self._retries = max(1, retries)
        self._base_url = base_url
        self._timeout = timeout
        self._developer_mode = developer_mode
        self._top_p = top_p
        self._max_tokens = max_tokens
        try:
            self._client = ollama.Client(host=base_url, timeout=timeout)
        except TypeError:
            self._client = ollama.Client(host=base_url)

    @classmethod
    def from_config(cls, config: ApplicationConfig) -> OllamaService:
        """Build OllamaService from the canonical application configuration."""

        llm = config.llm
        return cls(
            model=llm.model,
            temperature=llm.temperature,
            retries=llm.max_retries,
            base_url=llm.base_url,
            timeout=llm.timeout_seconds,
            developer_mode=config.application.developer_mode,
            top_p=llm.top_p,
            max_tokens=llm.max_tokens,
            provider=llm.provider,
        )

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def provider(self) -> str:
        """
        Return configured provider.
        """

        return self._provider

    @property
    def model(self) -> str:
        """
        Return configured model.
        """

        return self._model

    @property
    def temperature(self) -> float:
        """
        Return configured temperature.
        """

        return self._temperature

    @property
    def base_url(self) -> str:
        """Return configured Ollama host URL."""

        return self._base_url

    @property
    def developer_mode(self) -> bool:
        """Return whether simulated responses are enabled."""

        return self._developer_mode

    @property
    def retries(self) -> int:
        """
        Return retry count.
        """

        return self._retries

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
        Generate a response from the configured Ollama model.

        This method performs:

        * Developer mode handling
        * Server availability check
        * Automatic retry
        * Response validation

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
            If generation ultimately fails.
        """

        if self._developer_mode:
            _LOGGER.info("Developer mode enabled.")
            return self._developer_response()

        self._validate_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        self._validate_model()

        self._log_request(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        if not self.is_available():
            raise RuntimeError(
                "Ollama server is not available."
            )

        last_exception: Exception | None = None

        for attempt in range(1, self._retries + 1):

            try:

                _LOGGER.info(
                    "Generating response "
                    "(attempt %d/%d)...",
                    attempt,
                    self._retries,
                )

                start = perf_counter()

                response = self._chat(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )

                llm_response = self._validate_response(
                    response,
                )

                elapsed = perf_counter() - start

                _LOGGER.info(
                    "Generation completed in %.2f seconds.",
                    elapsed,
                )

                self._log_response(
                    llm_response,
                )

                return llm_response

            except Exception as exc:

                last_exception = exc

                _LOGGER.exception(
                    "Generation attempt %d failed.",
                    attempt,
                )

                if attempt < self._retries:
                    self._sleep_before_retry(attempt)

        raise RuntimeError(
            "Failed to generate response from Ollama."
        ) from last_exception


    def list_models(self) -> list[str]:
        """
        Return installed Ollama models.

        Returns
        -------
        list[str]
        """
        # Implemented in Part 3.
        raise NotImplementedError

    def model_exists(
        self,
        model: str,
    ) -> bool:
        """
        Determine whether the specified model exists.

        Parameters
        ----------
        model:
            Model name.

        Returns
        -------
        bool
        """
        # Implemented in Part 3.
        raise NotImplementedError

    def is_available(self) -> bool:
        """
        Check whether the Ollama server is reachable.

        Returns
        -------
        bool
        """
        # Implemented in Part 3.
        raise NotImplementedError

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _developer_response(self) -> LLMResponse:
        """
        Return a deterministic simulated response for developer mode.
        """
        # Implemented in Part 2.
        raise NotImplementedError

    def _validate_response(
        self,
        response: dict[str, Any],
    ) -> LLMResponse:
        """
        Validate the Ollama response and convert it into LLMResponse.

        Returns
        -------
        LLMResponse
        """
        # Implemented in Part 2.
        raise NotImplementedError

    def _calculate_total_tokens(
        self,
        prompt_tokens: int | None,
        completion_tokens: int | None,
    ) -> int | None:
        """
        Calculate total token count.

        Returns
        -------
        int | None
        """
        # Implemented in Part 3.
        raise NotImplementedError

    def _sleep_before_retry(
        self,
        attempt: int,
    ) -> None:
        """
        Sleep before retrying a failed request.

        Parameters
        ----------
        attempt:
            Retry attempt number.
        """

        delay = (
            _RETRY_DELAY_SECONDS
            * attempt
        )

        _LOGGER.warning(
            "Retry %d scheduled after %.1f second(s).",
            attempt,
            delay,
        )

        time.sleep(delay)
    # =========================================================================

    def _developer_response(
        self,
    ) -> LLMResponse:
        """
        Return a deterministic response when developer mode
        is enabled.
        """

        return LLMResponse(
            content="""
# AI Research Analysis (Developer Mode)

## Executive Summary

This is a simulated response returned because
Developer Mode is enabled.

## Research Problem

Simulated research problem.

## Methodology

Transformer-based architecture.

## Key Contributions

- Contribution 1
- Contribution 2
- Contribution 3

## Strengths

- Clear methodology
- Good experimental design

## Limitations

- Simulated output

## Future Work

- Replace with real model output.
""".strip(),
            provider="developer-mode",
            model="developer-mode",
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
        )

    # =========================================================================

    def _chat(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:
        """
        Execute a single Ollama request.

        Returns
        -------
        dict[str, Any]
        """

        try:

            return self._client.chat(
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
                    "temperature": self._temperature,
                },
            )

        except ollama.ResponseError as exc:

            raise RuntimeError(
                f"Ollama generation failed: {exc}"
            ) from exc

        except Exception as exc:

            raise RuntimeError(
                f"Unexpected Ollama error: {exc}"
            ) from exc
    # =========================================================================

    def _validate_response(
        self,
        response: dict[str, Any],
    ) -> LLMResponse:
        """
        Validate Ollama response.

        Parameters
        ----------
        response:
            Raw Ollama response.

        Returns
        -------
        LLMResponse

        Raises
        ------
        RuntimeError
            If the response is invalid.
        """

        message = response.get("message")

        if message is None:
            raise RuntimeError(
                "Ollama returned an invalid response."
            )

        content = (
            message.get("content", "")
            .strip()
        )

        if not content:
            raise RuntimeError(
                "Ollama returned an empty response."
            )

        if len(content) < _MIN_RESPONSE_LENGTH:

            _LOGGER.warning(
                "Very short response received "
                "(%d characters).",
                len(content),
            )

        prompt_tokens = response.get(
            "prompt_eval_count"
        )

        completion_tokens = response.get(
            "eval_count"
        )

        total_tokens = self._calculate_total_tokens(
            prompt_tokens,
            completion_tokens,
        )

        return LLMResponse(
            content=content,
            provider=self._provider,
            model=self._model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )

    def list_models(self) -> list[str]:
        """
        Return installed Ollama models.

        Returns
        -------
        list[str]
            Sorted list of installed model names.
        """

        try:

            response: dict[str, Any] = self._client.list()

            models = response.get("models", [])

            names: list[str] = []

            for model in models:

                name = (
                    model.get("model")
                    or model.get("name")
                )

                if name:
                    names.append(name)

            names = sorted(set(names))

            _LOGGER.info(
                "Discovered %d installed model(s).",
                len(names),
            )

            return names

        except Exception as exc:

            _LOGGER.exception(
                "Unable to retrieve installed models."
            )

            raise RuntimeError(
                "Failed to retrieve Ollama models."
            ) from exc

    # =========================================================================

    def model_exists(
        self,
        model: str,
    ) -> bool:
        """
        Determine whether a model exists locally.

        Parameters
        ----------
        model:
            Model name.

        Returns
        -------
        bool
        """

        if not model.strip():
            return False

        return model in self.list_models()

    # =========================================================================

    def is_available(self) -> bool:
        """
        Determine whether the Ollama server is reachable.

        Returns
        -------
        bool
        """

        try:

            self._client.list()

            return True

        except Exception:
            _LOGGER.exception("Ollama server is not reachable.")
            return False

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _calculate_total_tokens(
        self,
        prompt_tokens: int | None,
        completion_tokens: int | None,
    ) -> int | None:
        """
        Calculate the total token count.

        Parameters
        ----------
        prompt_tokens:
            Prompt token count.

        completion_tokens:
            Completion token count.

        Returns
        -------
        int | None
        """

        if (
            prompt_tokens is None
            or completion_tokens is None
        ):
            return None

        return (
            prompt_tokens
            + completion_tokens
        )

    # =========================================================================

    def _validate_prompt(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> None:
        """
        Validate prompts before sending them to Ollama.

        Parameters
        ----------
        system_prompt:
            System prompt.

        user_prompt:
            User prompt.

        Raises
        ------
        ValueError
            If either prompt is invalid.
        """

        if not system_prompt.strip():
            raise ValueError(
                "System prompt cannot be empty."
            )

        if not user_prompt.strip():
            raise ValueError(
                "User prompt cannot be empty."
            )

    # =========================================================================

    def _validate_model(self) -> None:
        """
        Validate the configured model.

        Raises
        ------
        RuntimeError
            If the configured model is unavailable.
        """

        if not self.model_exists(self._model):

            raise RuntimeError(
                f"Ollama model '{self._model}' "
                "is not installed."
            )

    # =========================================================================

    def _log_request(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> None:
        """
        Log request metadata.

        Parameters
        ----------
        system_prompt:
            System prompt.

        user_prompt:
            User prompt.
        """

        _LOGGER.debug(
            "Provider=%s | Model=%s",
            self._provider,
            self._model,
        )

        _LOGGER.debug(
            "System Prompt: %d characters",
            len(system_prompt),
        )

        _LOGGER.debug(
            "User Prompt: %d characters",
            len(user_prompt),
        )

        _LOGGER.debug(
            "Total Prompt: %d characters",
            len(system_prompt)
            + len(user_prompt),
        )

    # =========================================================================

    def _log_response(
        self,
        response: LLMResponse,
    ) -> None:
        """
        Log response metadata.

        Parameters
        ----------
        response:
            Validated response.
        """

        _LOGGER.debug(
            "Response Length: %d characters",
            len(response.content),
        )

        _LOGGER.debug(
            "Prompt Tokens: %s",
            response.prompt_tokens,
        )

        _LOGGER.debug(
            "Completion Tokens: %s",
            response.completion_tokens,
        )

        _LOGGER.debug(
            "Total Tokens: %s",
            response.total_tokens,
        )
    def __repr__(self) -> str:
        """
        Return a developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"provider={self._provider!r}, "
            f"model={self._model!r})"
        )