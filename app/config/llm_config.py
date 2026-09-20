"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Configuration
File         : llm_config.py
Version      : 0.5.0
Author       : Dr. B. Sudhakar

Description:
    Compatibility defaults for LLM provider and generation parameters.

    Canonical runtime values come from ApplicationConfig via
    ``get_application_config()``. This module re-exports the same defaults
    so existing imports keep working.
===============================================================================
"""

from app.config.application_config import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_PROVIDER,
    DEFAULT_MAX_INPUT_CHARACTERS,
    DEFAULT_TEMPERATURE,
)

PROVIDER_NAME = DEFAULT_LLM_PROVIDER

MODEL_NAME = DEFAULT_LLM_MODEL

RECOMMENDED_MODELS = {
    "paper_analysis": {
        "minimum": "qwen3:4b",
        "recommended": "qwen3:8b",
        "advanced": "gemini-2.5-pro",
    }
}

TEMPERATURE = DEFAULT_TEMPERATURE

MAX_INPUT_CHARACTERS = DEFAULT_MAX_INPUT_CHARACTERS
