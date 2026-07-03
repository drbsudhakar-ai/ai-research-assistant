"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Service
File         : llm_service.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Unified interface for AI providers.

Responsibilities:
    - Route requests to the selected provider.
    - Hide provider implementation details.
===============================================================================
"""

from __future__ import annotations

from app.services.ollama_service import OllamaService

__all__ = [
    "LLMService",
]


class LLMService:
    """
    Provider abstraction layer.
    """

    def __init__(self) -> None:

        self._ollama = OllamaService()

    def generate_analysis(
        self,
        paper_text: str,
        analysis_type: str,
        provider: str,
        model: str,
    ) -> str:
        """
        Generate AI analysis.
        """

        provider = provider.lower()

        if provider == "ollama":

            return self._ollama.generate_analysis(
                paper_text=paper_text,
                analysis_type=analysis_type,
                model=model,
            )

        raise ValueError(
            f"Unsupported provider: {provider}"
        )