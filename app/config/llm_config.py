"""
===============================================================================
Project      : AI Research Assistant
Module       : LLM Configuration
File         : llm_config.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Central configuration for Large Language Model (LLM) providers and models.
    This module enables provider abstraction, allowing the application to
    switch between local and cloud models with minimal code changes.

Supported Providers:
    • Ollama
    • OpenAI (Future)
    • Gemini (Future)
    • DeepSeek (Future)

Last Updated:
    2026-06-28
===============================================================================
"""

# -----------------------------------------------------------------------------
# Default Provider Configuration
# -----------------------------------------------------------------------------

DEFAULT_PROVIDER = "ollama"

DEFAULT_MODEL = "qwen3:4b"

# -----------------------------------------------------------------------------
# Model Recommendations
# -----------------------------------------------------------------------------

RECOMMENDED_MODELS = {
    "paper_analysis": {
        "minimum": "qwen3:4b",
        "recommended": "qwen3:8b",
        "advanced": "gemini-2.5-pro"
    }
}

# -----------------------------------------------------------------------------
# LLM Parameters
# -----------------------------------------------------------------------------

TEMPERATURE = 0.2

MAX_INPUT_CHARACTERS = 10000