"""
app/settings/api/metadata.py

Production-ready provider metadata registry.

This module contains immutable metadata describing each supported
LLM provider. The metadata is intended for UI rendering, validation,
documentation links, feature discovery, and configuration defaults.

The registry intentionally contains no Streamlit code.

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional

from .enums import APIProvider


# ============================================================================
# Provider Metadata
# ============================================================================


@dataclass(frozen=True, slots=True)
class ProviderMetadata:
    """
    Immutable metadata describing a provider.

    This information is consumed by the Settings UI,
    validation layer, and future provider management
    components.
    """

    provider: APIProvider

    # Display
    display_name: str
    short_name: str
    icon: str
    color: str

    # Description
    description: str
    company: str

    # URLs
    website: str
    documentation_url: str
    api_reference_url: str

    # Configuration
    base_url_placeholder: str
    api_key_label: str

    # Models
    supports_custom_models: bool
    recommended_models: List[str] = field(default_factory=list)

    # Features
    supports_streaming: bool = True
    supports_embeddings: bool = False
    supports_function_calling: bool = False
    supports_vision: bool = False
    supports_json_mode: bool = False
    supports_system_prompt: bool = True

    # Connectivity
    local_provider: bool = False
    cloud_provider: bool = True

    # UI
    enabled_by_default: bool = True

    # Future expansion
    extra: Dict[str, str] = field(default_factory=dict)


# ============================================================================
# Provider Registry
# ============================================================================


_PROVIDER_METADATA: Dict[APIProvider, ProviderMetadata] = {
    APIProvider.OPENAI: ProviderMetadata(
        provider=APIProvider.OPENAI,
        display_name="OpenAI",
        short_name="OpenAI",
        icon="🤖",
        color="#10A37F",
        description=(
            "Industry-leading GPT models offering text generation, "
            "reasoning, coding, vision and structured outputs."
        ),
        company="OpenAI",
        website="https://openai.com",
        documentation_url="https://platform.openai.com/docs",
        api_reference_url="https://platform.openai.com/docs/api-reference",
        base_url_placeholder="https://api.openai.com/v1",
        api_key_label="OpenAI API Key",
        supports_custom_models=False,
        recommended_models=[
            "gpt-5",
            "gpt-5-mini",
            "gpt-4.1",
        ],
        supports_streaming=True,
        supports_embeddings=True,
        supports_function_calling=True,
        supports_vision=True,
        supports_json_mode=True,
        supports_system_prompt=True,
        local_provider=False,
        cloud_provider=True,
    ),

    APIProvider.GEMINI: ProviderMetadata(
        provider=APIProvider.GEMINI,
        display_name="Google Gemini",
        short_name="Gemini",
        icon="✨",
        color="#4285F4",
        description=(
            "Google Gemini models supporting multimodal reasoning, "
            "large context windows and developer APIs."
        ),
        company="Google",
        website="https://ai.google.dev",
        documentation_url="https://ai.google.dev/docs",
        api_reference_url="https://ai.google.dev/api",
        base_url_placeholder="https://generativelanguage.googleapis.com",
        api_key_label="Gemini API Key",
        supports_custom_models=False,
        recommended_models=[
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        ],
        supports_streaming=True,
        supports_embeddings=True,
        supports_function_calling=True,
        supports_vision=True,
        supports_json_mode=True,
        supports_system_prompt=True,
        local_provider=False,
        cloud_provider=True,
    ),

    APIProvider.ANTHROPIC: ProviderMetadata(
        provider=APIProvider.ANTHROPIC,
        display_name="Anthropic Claude",
        short_name="Claude",
        icon="🧠",
        color="#D97706",
        description=(
            "Claude models optimized for long-context reasoning, "
            "coding assistance and document understanding."
        ),
        company="Anthropic",
        website="https://www.anthropic.com",
        documentation_url="https://docs.anthropic.com",
        api_reference_url="https://docs.anthropic.com/en/api",
        base_url_placeholder="https://api.anthropic.com",
        api_key_label="Anthropic API Key",
        supports_custom_models=False,
        recommended_models=[
            "claude-opus",
            "claude-sonnet",
            "claude-haiku",
        ],
        supports_streaming=True,
        supports_embeddings=False,
        supports_function_calling=True,
        supports_vision=True,
        supports_json_mode=True,
        supports_system_prompt=True,
        local_provider=False,
        cloud_provider=True,
    ),

    APIProvider.OLLAMA: ProviderMetadata(
        provider=APIProvider.OLLAMA,
        display_name="Ollama",
        short_name="Ollama",
        icon="🦙",
        color="#4F46E5",
        description=(
            "Run open-source LLMs locally with complete privacy "
            "and offline support."
        ),
        company="Ollama",
        website="https://ollama.com",
        documentation_url="https://github.com/ollama/ollama",
        api_reference_url="https://github.com/ollama/ollama/blob/main/docs/api.md",
        base_url_placeholder="http://localhost:11434",
        api_key_label="API Key (Not Required)",
        supports_custom_models=True,
        recommended_models=[
            "qwen3:4b",
            "llama3.1:8b",
            "mistral",
            "phi4",
            "deepseek-r1",
        ],
        supports_streaming=True,
        supports_embeddings=True,
        supports_function_calling=False,
        supports_vision=True,
        supports_json_mode=False,
        supports_system_prompt=True,
        local_provider=True,
        cloud_provider=False,
    ),

    APIProvider.DEEPSEEK: ProviderMetadata(
        provider=APIProvider.DEEPSEEK,
        display_name="DeepSeek",
        short_name="DeepSeek",
        icon="🚀",
        color="#2563EB",
        description=(
            "High-performance reasoning and coding models with "
            "OpenAI-compatible APIs."
        ),
        company="DeepSeek",
        website="https://www.deepseek.com",
        documentation_url="https://api-docs.deepseek.com",
        api_reference_url="https://api-docs.deepseek.com/api",
        base_url_placeholder="https://api.deepseek.com",
        api_key_label="DeepSeek API Key",
        supports_custom_models=False,
        recommended_models=[
            "deepseek-chat",
            "deepseek-reasoner",
        ],
        supports_streaming=True,
        supports_embeddings=False,
        supports_function_calling=True,
        supports_vision=False,
        supports_json_mode=True,
        supports_system_prompt=True,
        local_provider=False,
        cloud_provider=True,
    ),
}

# ============================================================================
# Public API
# ============================================================================


def get_provider_metadata(provider: APIProvider) -> ProviderMetadata:
    """
    Return metadata for a provider.

    Raises
    ------
    KeyError
        If the provider is not registered.
    """
    try:
        return _PROVIDER_METADATA[provider]
    except KeyError as exc:
        raise KeyError(
            f"No metadata registered for provider '{provider.value}'."
        ) from exc


def get_all_provider_metadata() -> Mapping[APIProvider, ProviderMetadata]:
    """
    Return a read-only view of the provider registry.
    """
    return _PROVIDER_METADATA


def get_all_providers() -> List[APIProvider]:
    """
    Return all registered providers.
    """
    return list(_PROVIDER_METADATA.keys())


def get_enabled_providers() -> List[APIProvider]:
    """
    Return providers enabled by default.
    """
    return [
        provider
        for provider, metadata in _PROVIDER_METADATA.items()
        if metadata.enabled_by_default
    ]


def provider_exists(provider: APIProvider) -> bool:
    """
    Determine whether metadata exists for a provider.
    """
    return provider in _PROVIDER_METADATA


# ============================================================================
# Model Helpers
# ============================================================================


def get_supported_models(provider: APIProvider) -> List[str]:
    """
    Return recommended models for a provider.
    """
    return list(get_provider_metadata(provider).recommended_models)


def supports_custom_models(provider: APIProvider) -> bool:
    """
    Return True if users may enter arbitrary model names.
    """
    return get_provider_metadata(provider).supports_custom_models


# ============================================================================
# Capability Helpers
# ============================================================================


def supports_streaming(provider: APIProvider) -> bool:
    return get_provider_metadata(provider).supports_streaming


def supports_embeddings(provider: APIProvider) -> bool:
    return get_provider_metadata(provider).supports_embeddings


def supports_function_calling(provider: APIProvider) -> bool:
    return get_provider_metadata(provider).supports_function_calling


def supports_vision(provider: APIProvider) -> bool:
    return get_provider_metadata(provider).supports_vision


def supports_json_mode(provider: APIProvider) -> bool:
    return get_provider_metadata(provider).supports_json_mode


def supports_system_prompt(provider: APIProvider) -> bool:
    return get_provider_metadata(provider).supports_system_prompt


# ============================================================================
# Provider Classification
# ============================================================================


def is_local_provider(provider: APIProvider) -> bool:
    """
    Return True if the provider runs locally.
    """
    return get_provider_metadata(provider).local_provider


def is_cloud_provider(provider: APIProvider) -> bool:
    """
    Return True if the provider is cloud hosted.
    """
    return get_provider_metadata(provider).cloud_provider


# ============================================================================
# Convenience Accessors
# ============================================================================


def get_provider_display_name(provider: APIProvider) -> str:
    return get_provider_metadata(provider).display_name


def get_provider_description(provider: APIProvider) -> str:
    return get_provider_metadata(provider).description


def get_provider_icon(provider: APIProvider) -> str:
    return get_provider_metadata(provider).icon


def get_provider_color(provider: APIProvider) -> str:
    return get_provider_metadata(provider).color


def get_provider_company(provider: APIProvider) -> str:
    return get_provider_metadata(provider).company


def get_provider_website(provider: APIProvider) -> str:
    return get_provider_metadata(provider).website


def get_provider_documentation(provider: APIProvider) -> str:
    return get_provider_metadata(provider).documentation_url


def get_provider_api_reference(provider: APIProvider) -> str:
    return get_provider_metadata(provider).api_reference_url


def get_base_url_placeholder(provider: APIProvider) -> str:
    return get_provider_metadata(provider).base_url_placeholder


def get_api_key_label(provider: APIProvider) -> str:
    return get_provider_metadata(provider).api_key_label


# ============================================================================
# Registry Statistics
# ============================================================================


def total_registered_providers() -> int:
    """
    Return the total number of registered providers.
    """
    return len(_PROVIDER_METADATA)


def local_provider_count() -> int:
    """
    Return the number of local providers.
    """
    return sum(
        metadata.local_provider
        for metadata in _PROVIDER_METADATA.values()
    )


def cloud_provider_count() -> int:
    """
    Return the number of cloud providers.
    """
    return sum(
        metadata.cloud_provider
        for metadata in _PROVIDER_METADATA.values()
    )


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ProviderMetadata",
    "get_provider_metadata",
    "get_all_provider_metadata",
    "get_all_providers",
    "get_enabled_providers",
    "provider_exists",
    "get_supported_models",
    "supports_custom_models",
    "supports_streaming",
    "supports_embeddings",
    "supports_function_calling",
    "supports_vision",
    "supports_json_mode",
    "supports_system_prompt",
    "is_local_provider",
    "is_cloud_provider",
    "get_provider_display_name",
    "get_provider_description",
    "get_provider_icon",
    "get_provider_color",
    "get_provider_company",
    "get_provider_website",
    "get_provider_documentation",
    "get_provider_api_reference",
    "get_base_url_placeholder",
    "get_api_key_label",
    "total_registered_providers",
    "local_provider_count",
    "cloud_provider_count",
]