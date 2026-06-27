"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Service
File         : ollama_service.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    This module provides a reusable service for communicating with
    Ollama-based local language models.

Purpose:
    • Encapsulate all Ollama API interactions.
    • Hide provider-specific implementation details.
    • Enable easy migration to cloud providers.
    • Support provider abstraction.

Future Compatibility:
    • OpenAI
    • Gemini
    • DeepSeek
    • Claude
===============================================================================
"""

import ollama

from app.config.llm_config import (
    DEFAULT_MODEL,
    TEMPERATURE
)


class OllamaService:
    """
    Service class for interacting with Ollama LLMs.
    """

    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.provider = "Ollama"

    def generate(self, system_prompt, user_prompt):
        """
        Generate a response from the configured Ollama model.

        Args:
            system_prompt (str): Defines AI behavior.
            user_prompt (str): Contains the analysis task.

        Returns:
            str: Model response.
        """

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": TEMPERATURE
            }
        )

        return response["message"]["content"]