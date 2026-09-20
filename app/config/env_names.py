"""Environment variable names actually read by the configuration loader.

These names reuse the existing ``AI_RA_`` prefix from
``app.settings.api.constants`` where that module already defined them.
"""

from __future__ import annotations

from typing import Final

from app.settings.api.constants import ENV_API_PROVIDER, ENV_OLLAMA_BASE_URL, ENV_PREFIX

ENV_ENVIRONMENT: Final[str] = f"{ENV_PREFIX}ENV"
ENV_DEVELOPER_MODE: Final[str] = f"{ENV_PREFIX}DEVELOPER_MODE"
ENV_DEBUG: Final[str] = f"{ENV_PREFIX}DEBUG"
ENV_LOG_LEVEL: Final[str] = f"{ENV_PREFIX}LOG_LEVEL"
ENV_LOG_FILE: Final[str] = f"{ENV_PREFIX}LOG_FILE"

ENV_LLM_PROVIDER: Final[str] = ENV_API_PROVIDER
ENV_LLM_MODEL: Final[str] = f"{ENV_PREFIX}MODEL"
ENV_LLM_BASE_URL: Final[str] = ENV_OLLAMA_BASE_URL
ENV_LLM_API_KEY: Final[str] = f"{ENV_PREFIX}API_KEY"
ENV_LLM_TEMPERATURE: Final[str] = f"{ENV_PREFIX}TEMPERATURE"
ENV_LLM_TOP_P: Final[str] = f"{ENV_PREFIX}TOP_P"
ENV_LLM_MAX_TOKENS: Final[str] = f"{ENV_PREFIX}MAX_TOKENS"
ENV_LLM_TIMEOUT: Final[str] = f"{ENV_PREFIX}TIMEOUT"
ENV_LLM_CONNECT_TIMEOUT: Final[str] = f"{ENV_PREFIX}CONNECT_TIMEOUT"
ENV_LLM_MAX_RETRIES: Final[str] = f"{ENV_PREFIX}MAX_RETRIES"
ENV_LLM_MAX_INPUT_CHARACTERS: Final[str] = f"{ENV_PREFIX}MAX_INPUT_CHARACTERS"

ENV_DATA_DIR: Final[str] = f"{ENV_PREFIX}DATA_DIR"
ENV_UPLOADS_DIR: Final[str] = f"{ENV_PREFIX}UPLOADS_DIR"
ENV_TEMP_DIR: Final[str] = f"{ENV_PREFIX}TEMP_DIR"
ENV_REPORTS_DIR: Final[str] = f"{ENV_PREFIX}REPORTS_DIR"
ENV_LOGS_DIR: Final[str] = f"{ENV_PREFIX}LOGS_DIR"
ENV_CONFIG_DIR: Final[str] = f"{ENV_PREFIX}CONFIG_DIR"
ENV_DATABASE_PATH: Final[str] = f"{ENV_PREFIX}DATABASE_PATH"

ENV_EXPORT_DEFAULT_FORMAT: Final[str] = f"{ENV_PREFIX}EXPORT_DEFAULT_FORMAT"

SECRET_ENV_NAMES: Final[frozenset[str]] = frozenset(
    {
        ENV_LLM_API_KEY,
        f"{ENV_PREFIX}OPENAI_API_KEY",
        f"{ENV_PREFIX}GEMINI_API_KEY",
        f"{ENV_PREFIX}ANTHROPIC_API_KEY",
        f"{ENV_PREFIX}DEEPSEEK_API_KEY",
    }
)

__all__ = [
    "ENV_CONFIG_DIR",
    "ENV_DATABASE_PATH",
    "ENV_DATA_DIR",
    "ENV_DEBUG",
    "ENV_DEVELOPER_MODE",
    "ENV_ENVIRONMENT",
    "ENV_EXPORT_DEFAULT_FORMAT",
    "ENV_LLM_API_KEY",
    "ENV_LLM_BASE_URL",
    "ENV_LLM_CONNECT_TIMEOUT",
    "ENV_LLM_MAX_INPUT_CHARACTERS",
    "ENV_LLM_MAX_RETRIES",
    "ENV_LLM_MAX_TOKENS",
    "ENV_LLM_MODEL",
    "ENV_LLM_PROVIDER",
    "ENV_LLM_TEMPERATURE",
    "ENV_LLM_TIMEOUT",
    "ENV_LLM_TOP_P",
    "ENV_LOGS_DIR",
    "ENV_LOG_FILE",
    "ENV_LOG_LEVEL",
    "ENV_PREFIX",
    "ENV_REPORTS_DIR",
    "ENV_TEMP_DIR",
    "ENV_UPLOADS_DIR",
    "SECRET_ENV_NAMES",
]
