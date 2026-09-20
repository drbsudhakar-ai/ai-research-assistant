"""
app/settings/api/defaults.py

Default configuration values for supported LLM providers.

This module is the single source of truth for provider defaults used by
the configuration layer, settings UI, validation, and initialization.

It intentionally contains no Streamlit code.

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .enums import APIProvider


# ============================================================================
# Global API Defaults
# ============================================================================

DEFAULT_TIMEOUT: int = 120

DEFAULT_CONNECT_TIMEOUT: int = 30

DEFAULT_READ_TIMEOUT: int = 120

DEFAULT_MAX_RETRIES: int = 3

DEFAULT_RETRY_DELAY: float = 2.0

DEFAULT_TEMPERATURE: float = 0.20

DEFAULT_TOP_P: float = 0.95

DEFAULT_MAX_TOKENS: int = 4096

DEFAULT_STREAMING: bool = True

DEFAULT_VERIFY_SSL: bool = True

DEFAULT_SAVE_API_KEYS: bool = False

DEFAULT_ENABLE_LOGGING: bool = True

DEFAULT_TEST_CONNECTION_ON_SAVE: bool = True

DEFAULT_AUTO_DISCOVER_MODELS: bool = True

DEFAULT_REQUESTS_PER_MINUTE: int = 60


# ============================================================================
# Provider Defaults
# ============================================================================


@dataclass(frozen=True, slots=True)
class ProviderDefaults:
    """
    Default configuration for an API provider.
    """

    provider: APIProvider

    enabled: bool

    base_url: str

    default_model: str

    timeout: int = DEFAULT_TIMEOUT

    connect_timeout: int = DEFAULT_CONNECT_TIMEOUT

    read_timeout: int = DEFAULT_READ_TIMEOUT

    max_retries: int = DEFAULT_MAX_RETRIES

    retry_delay: float = DEFAULT_RETRY_DELAY

    temperature: float = DEFAULT_TEMPERATURE

    top_p: float = DEFAULT_TOP_P

    max_tokens: int = DEFAULT_MAX_TOKENS

    streaming: bool = DEFAULT_STREAMING

    verify_ssl: bool = DEFAULT_VERIFY_SSL

    save_api_key: bool = DEFAULT_SAVE_API_KEYS

    auto_discover_models: bool = DEFAULT_AUTO_DISCOVER_MODELS

    requests_per_minute: int = DEFAULT_REQUESTS_PER_MINUTE


# ============================================================================
# Provider Registry
# ============================================================================

_PROVIDER_DEFAULTS: Dict[APIProvider, ProviderDefaults] = {
    APIProvider.OPENAI: ProviderDefaults(
        provider=APIProvider.OPENAI,
        enabled=False,
        base_url="https://api.openai.com/v1",
        default_model="gpt-5",
    ),

    APIProvider.GEMINI: ProviderDefaults(
        provider=APIProvider.GEMINI,
        enabled=False,
        base_url="https://generativelanguage.googleapis.com",
        default_model="gemini-2.5-flash",
    ),

    APIProvider.ANTHROPIC: ProviderDefaults(
        provider=APIProvider.ANTHROPIC,
        enabled=False,
        base_url="https://api.anthropic.com",
        default_model="claude-sonnet",
    ),

    APIProvider.OLLAMA: ProviderDefaults(
        provider=APIProvider.OLLAMA,
        enabled=True,
        base_url="http://localhost:11434",
        default_model="qwen3:4b",
        streaming=True,
        auto_discover_models=True,
    ),

    APIProvider.LM_STUDIO: ProviderDefaults(
        provider=APIProvider.LM_STUDIO,
        enabled=True,
        base_url="http://localhost:1234/v1",
        default_model="",
        timeout=120,
        streaming=True,
        auto_discover_models=True,
    ),

    APIProvider.AZURE_OPENAI: ProviderDefaults(
        provider=APIProvider.AZURE_OPENAI,
        enabled=False,
        base_url="https://YOUR_RESOURCE.openai.azure.com",
        default_model="gpt-4.1",
    ),

    APIProvider.OPENROUTER: ProviderDefaults(
        provider=APIProvider.OPENROUTER,
        enabled=False,
        base_url="https://openrouter.ai/api/v1",
        default_model="openai/gpt-4.1",
    ),

    APIProvider.MISTRAL: ProviderDefaults(
        provider=APIProvider.MISTRAL,
        enabled=False,
        base_url="https://api.mistral.ai/v1",
        default_model="mistral-large-latest",
    ),

    APIProvider.GROQ: ProviderDefaults(
        provider=APIProvider.GROQ,
        enabled=False,
        base_url="https://api.groq.com/openai/v1",
        default_model="llama-3.3-70b-versatile",
    ),

    APIProvider.COHERE: ProviderDefaults(
        provider=APIProvider.COHERE,
        enabled=False,
        base_url="https://api.cohere.ai/v1",
        default_model="command-r-plus",
    ),

    APIProvider.HUGGINGFACE: ProviderDefaults(
        provider=APIProvider.HUGGINGFACE,
        enabled=False,
        base_url="https://api-inference.huggingface.co",
        default_model="",
    ),

    APIProvider.CUSTOM_OPENAI: ProviderDefaults(
        provider=APIProvider.CUSTOM_OPENAI,
        enabled=False,
        base_url="http://localhost:8000/v1",
        default_model="",
    ),

    APIProvider.CUSTOM: ProviderDefaults(
        provider=APIProvider.CUSTOM,
        enabled=False,
        base_url="",
        default_model="",
    ),

    APIProvider.DEEPSEEK: ProviderDefaults(
        provider=APIProvider.DEEPSEEK,
        enabled=False,
        base_url="https://api.deepseek.com",
        default_model="deepseek-chat",
    ),
}


# ============================================================================
# Public API
# ============================================================================


def get_provider_defaults(provider: APIProvider) -> ProviderDefaults:
    """
    Return the default configuration for a provider.

    Raises
    ------
    KeyError
        If the provider has not been registered.
    """
    try:
        return _PROVIDER_DEFAULTS[provider]
    except KeyError as exc:
        raise KeyError(
            f"No default configuration registered for "
            f"provider '{provider.value}'."
        ) from exc


def get_all_provider_defaults() -> Dict[APIProvider, ProviderDefaults]:
    """
    Return a shallow copy of the provider defaults registry.
    """
    return dict(_PROVIDER_DEFAULTS)


def provider_has_defaults(provider: APIProvider) -> bool:
    """
    Return True if defaults exist for the provider.
    """
    return provider in _PROVIDER_DEFAULTS


# ============================================================================
# Convenience Helpers
# ============================================================================


def get_default_model(provider: APIProvider) -> str:
    """
    Return the provider's default model.
    """
    return get_provider_defaults(provider).default_model


def get_default_base_url(provider: APIProvider) -> str:
    """
    Return the provider's default API endpoint.
    """
    return get_provider_defaults(provider).base_url


def get_default_timeout(provider: APIProvider) -> int:
    """
    Return the provider's default request timeout.
    """
    return get_provider_defaults(provider).timeout


def get_default_temperature(provider: APIProvider) -> float:
    """
    Return the provider's default temperature.
    """
    return get_provider_defaults(provider).temperature


def get_default_max_tokens(provider: APIProvider) -> int:
    """
    Return the provider's default max token limit.
    """
    return get_provider_defaults(provider).max_tokens


def is_provider_enabled_by_default(provider: APIProvider) -> bool:
    """
    Return whether the provider is enabled by default.
    """
    return get_provider_defaults(provider).enabled


# ============================================================================
# Configuration Builders
# ============================================================================


def build_default_provider_config(
    provider: APIProvider,
) -> Dict[str, object]:
    """
    Build a serializable provider configuration dictionary.

    Suitable for JSON/YAML export and application settings.
    """
    defaults = get_provider_defaults(provider)

    return {
        "provider": provider.value,
        "enabled": defaults.enabled,
        "api_key": "",
        "base_url": defaults.base_url,
        "model": defaults.default_model,
        "timeout": defaults.timeout,
        "connect_timeout": defaults.connect_timeout,
        "read_timeout": defaults.read_timeout,
        "max_retries": defaults.max_retries,
        "retry_delay": defaults.retry_delay,
        "temperature": defaults.temperature,
        "top_p": defaults.top_p,
        "max_tokens": defaults.max_tokens,
        "streaming": defaults.streaming,
        "verify_ssl": defaults.verify_ssl,
        "save_api_key": defaults.save_api_key,
        "auto_discover_models": defaults.auto_discover_models,
        "requests_per_minute": defaults.requests_per_minute,
    }


def build_default_api_settings() -> Dict[str, object]:
    """
    Build the complete default API settings structure.

    Returns
    -------
    dict
        Complete configuration for all providers and
        global API settings.
    """
    return {
        "default_provider": APIProvider.OLLAMA.value,
        "active_provider": APIProvider.OLLAMA.value,
        "global": {
            "enable_logging": DEFAULT_ENABLE_LOGGING,
            "verify_ssl": DEFAULT_VERIFY_SSL,
            "test_connection_on_save": (
                DEFAULT_TEST_CONNECTION_ON_SAVE
            ),
            "save_api_keys": DEFAULT_SAVE_API_KEYS,
            "streaming": DEFAULT_STREAMING,
        },
        "providers": {
            provider.value: build_default_provider_config(provider)
            for provider in _PROVIDER_DEFAULTS
        },
    }


# ============================================================================
# Registry Statistics
# ============================================================================


def total_registered_providers() -> int:
    """
    Return the total number of providers with defaults.
    """
    return len(_PROVIDER_DEFAULTS)


def enabled_provider_count() -> int:
    """
    Return the number of providers enabled by default.
    """
    return sum(
        defaults.enabled
        for defaults in _PROVIDER_DEFAULTS.values()
    )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Dataclass
    "ProviderDefaults",

    # Global defaults
    "DEFAULT_TIMEOUT",
    "DEFAULT_CONNECT_TIMEOUT",
    "DEFAULT_READ_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_RETRY_DELAY",
    "DEFAULT_TEMPERATURE",
    "DEFAULT_TOP_P",
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_STREAMING",
    "DEFAULT_VERIFY_SSL",
    "DEFAULT_SAVE_API_KEYS",
    "DEFAULT_ENABLE_LOGGING",
    "DEFAULT_TEST_CONNECTION_ON_SAVE",
    "DEFAULT_AUTO_DISCOVER_MODELS",
    "DEFAULT_REQUESTS_PER_MINUTE",

    # Registry
    "get_provider_defaults",
    "get_all_provider_defaults",
    "provider_has_defaults",

    # Convenience helpers
    "get_default_model",
    "get_default_base_url",
    "get_default_timeout",
    "get_default_temperature",
    "get_default_max_tokens",
    "is_provider_enabled_by_default",

    # Builders
    "build_default_provider_config",
    "build_default_api_settings",

    # Statistics
    "total_registered_providers",
    "enabled_provider_count",
]