"""
===============================================================================
Project      : AI Research Assistant
Module       : Models
File         : llm_response.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
    Represents the response returned by a language model provider.

Responsibilities:
    - Store generated content.
    - Store provider metadata.
    - Store token usage statistics.
    - Provide a provider-independent response contract.
===============================================================================
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.models.exceptions import DomainValidationError

__all__ = ["LLMResponse"]


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """Provider-neutral language-model output.

    Provider adapters must translate SDK objects into this contract.
    """

    content: str
    provider: str
    model: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.content, str):
            raise DomainValidationError("content must be a string.", field="content")
        if not str(self.provider).strip():
            raise DomainValidationError("provider is required.", field="provider")
        if not str(self.model).strip():
            raise DomainValidationError("model is required.", field="model")
        for name in ("prompt_tokens", "completion_tokens", "total_tokens"):
            value = getattr(self, name)
            if value is not None and int(value) < 0:
                raise DomainValidationError(
                    f"{name} cannot be negative.",
                    field=name,
                )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> LLMResponse:
        return cls(**data)
