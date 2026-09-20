"""Google Gemini provider adapter for the live analysis runtime."""

from __future__ import annotations

import logging
import time
from time import perf_counter
from typing import Any

import httpx

from app.config.application_config import ApplicationConfig
from app.models.llm_response import LLMResponse

_LOGGER = logging.getLogger(__name__)
_MIN_RESPONSE_LENGTH = 20


class GeminiService:
    """Translate Gemini REST responses into the provider-neutral contract."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        temperature: float = 0.2,
        top_p: float = 0.95,
        max_tokens: int | None = None,
        timeout: int = 300,
        connect_timeout: int = 30,
        retries: int = 1,
        client: httpx.Client | None = None,
    ) -> None:
        self._api_key = api_key.strip()
        self._model = model.strip()
        self._base_url = base_url.rstrip("/")
        self._temperature = temperature
        self._top_p = top_p
        self._max_tokens = max_tokens
        self._retries = max(1, retries)
        self._client = client or httpx.Client(
            timeout=httpx.Timeout(timeout, connect=connect_timeout)
        )

    @classmethod
    def from_config(cls, config: ApplicationConfig) -> GeminiService:
        llm = config.llm
        return cls(
            api_key=llm.api_key,
            model=llm.model,
            base_url=llm.base_url,
            temperature=llm.temperature,
            top_p=llm.top_p,
            max_tokens=llm.max_tokens,
            timeout=llm.timeout_seconds,
            connect_timeout=llm.connect_timeout_seconds,
            retries=llm.max_retries,
        )

    @property
    def provider(self) -> str:
        return "gemini"

    @property
    def model(self) -> str:
        return self._model

    def generate(self, *, system_prompt: str, user_prompt: str) -> LLMResponse:
        if not self._api_key:
            raise RuntimeError("Gemini API key is not configured.")
        if not system_prompt.strip() or not user_prompt.strip():
            raise ValueError("System and user prompts are required.")

        generation_config: dict[str, Any] = {
            "temperature": self._temperature,
            "topP": self._top_p,
        }
        if self._max_tokens is not None:
            generation_config["maxOutputTokens"] = self._max_tokens

        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": generation_config,
        }
        last_exception: Exception | None = None
        for attempt in range(1, self._retries + 1):
            try:
                started = perf_counter()
                response = self._client.post(
                    f"{self._base_url}/models/{self._model}:generateContent",
                    headers={"x-goog-api-key": self._api_key},
                    json=payload,
                )
                self._raise_for_status(response)
                result = self._parse_response(response.json())
                _LOGGER.info(
                    "Gemini generation completed in %.2f seconds.",
                    perf_counter() - started,
                )
                return result
            except (
                httpx.HTTPError,
                KeyError,
                RuntimeError,
                TypeError,
                ValueError,
            ) as exc:
                last_exception = exc
                _LOGGER.warning(
                    "Gemini generation attempt %d/%d failed: %s",
                    attempt,
                    self._retries,
                    exc,
                )
                if attempt < self._retries:
                    time.sleep(float(attempt))
        detail = str(last_exception) if last_exception else "Unknown provider error."
        raise RuntimeError(
            f"Failed to generate response from Gemini: {detail}"
        ) from last_exception

    def is_available(self) -> bool:
        if not self._api_key or not self._model:
            return False
        try:
            response = self._client.get(
                f"{self._base_url}/models/{self._model}",
                headers={"x-goog-api-key": self._api_key},
            )
            response.raise_for_status()
            methods = response.json().get("supportedGenerationMethods", [])
            return "generateContent" in methods
        except (httpx.HTTPError, TypeError, ValueError):
            return False

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        """Raise a concise provider error while keeping credentials private."""

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            try:
                message = str(
                    response.json().get("error", {}).get("message", "")
                ).strip()
            except (TypeError, ValueError):
                message = ""
            detail = message or response.reason_phrase
            raise RuntimeError(
                f"Gemini API returned HTTP {response.status_code}: {detail}"
            ) from exc

    def list_models(self) -> list[str]:
        if not self._api_key:
            return []
        try:
            response = self._client.get(
                f"{self._base_url}/models",
                headers={"x-goog-api-key": self._api_key},
            )
            response.raise_for_status()
            models = response.json().get("models", [])
            return sorted(
                str(item["name"]).removeprefix("models/")
                for item in models
                if "generateContent" in item.get("supportedGenerationMethods", [])
            )
        except (httpx.HTTPError, KeyError, TypeError, ValueError):
            _LOGGER.exception("Unable to retrieve Gemini models.")
            return []

    def model_exists(self, model: str) -> bool:
        return bool(model.strip()) and model in self.list_models()

    def _parse_response(self, payload: dict[str, Any]) -> LLMResponse:
        candidates = payload.get("candidates") or []
        if not candidates:
            block_reason = (payload.get("promptFeedback") or {}).get("blockReason")
            detail = f" Block reason: {block_reason}." if block_reason else ""
            raise ValueError(f"Gemini returned no response candidates.{detail}")
        parts = candidates[0].get("content", {}).get("parts", [])
        content = "\n".join(
            str(part.get("text", "")) for part in parts if part.get("text")
        ).strip()
        if len(content) < _MIN_RESPONSE_LENGTH:
            raise ValueError("Gemini returned an empty or unexpectedly short response.")
        usage = payload.get("usageMetadata") or {}
        return LLMResponse(
            content=content,
            provider=self.provider,
            model=self._model,
            prompt_tokens=usage.get("promptTokenCount"),
            completion_tokens=usage.get("candidatesTokenCount"),
            total_tokens=usage.get("totalTokenCount"),
        )
