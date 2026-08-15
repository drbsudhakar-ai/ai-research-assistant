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

from dataclasses import dataclass

__all__ = ["LLMResponse"]


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """
    Response returned by a language model provider.
    """

    content: str

    provider: str

    model: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    total_tokens: int | None = None