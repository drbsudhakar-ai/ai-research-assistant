"""
===============================================================================
File: app/settings/api/enums.py
Project: AI Research Assistant

Description:
    Core enumerations used throughout the API Provider Configuration subsystem.

    These enums provide a strongly typed foundation for:

    - Provider definitions
    - Provider categories
    - Authentication methods
    - Connection states
    - Provider capabilities
    - Validation severity
    - Configuration scopes

Author:
    Dr B Sudhakar

Architecture:
    app/settings/api
        ├── enums.py          ← This file
        ├── metadata.py
        ├── registry.py
        ├── state.py
        ├── providers.py
        ├── validation.py
        ├── capabilities.py
        └── secrets.py

Python:
    3.11+

License:
    MIT

===============================================================================
"""

from __future__ import annotations

from enum import StrEnum


# =============================================================================
# Provider Categories
# =============================================================================


class ProviderCategory(StrEnum):
    """
    Classification of AI providers.
    """

    LOCAL = "local"
    CLOUD = "cloud"
    HYBRID = "hybrid"
    CUSTOM = "custom"


# =============================================================================
# Supported Providers
# =============================================================================


class APIProvider(StrEnum):
    """
    Supported AI providers.
    """

    OLLAMA = "ollama"

    LM_STUDIO = "lm_studio"

    OPENAI = "openai"

    AZURE_OPENAI = "azure_openai"

    GEMINI = "gemini"

    ANTHROPIC = "anthropic"

    DEEPSEEK = "deepseek"

    OPENROUTER = "openrouter"

    MISTRAL = "mistral"

    GROQ = "groq"

    COHERE = "cohere"

    HUGGINGFACE = "huggingface"

    CUSTOM_OPENAI = "custom_openai"

    CUSTOM = "custom"


# =============================================================================
# Authentication Types
# =============================================================================


class CredentialType(StrEnum):
    """
    Authentication mechanism required by a provider.
    """

    NONE = "none"

    API_KEY = "api_key"

    API_KEY_AND_ORGANIZATION = "api_key_and_organization"

    TOKEN = "token"

    USERNAME_PASSWORD = "username_password"

    OAUTH = "oauth"

    CUSTOM = "custom"


# =============================================================================
# Connection Status
# =============================================================================


class ConnectionStatus(StrEnum):
    """
    Current provider connectivity state.
    """

    UNKNOWN = "unknown"

    NOT_CONFIGURED = "not_configured"

    DISCONNECTED = "disconnected"

    CONNECTING = "connecting"

    CONNECTED = "connected"

    FAILED = "failed"

    TIMEOUT = "timeout"

    UNAVAILABLE = "unavailable"


# =============================================================================
# Provider Capabilities
# =============================================================================


class ProviderCapability(StrEnum):
    """
    Features supported by an AI provider.
    """

    CHAT = "chat"

    TEXT_COMPLETION = "text_completion"

    STREAMING = "streaming"

    VISION = "vision"

    IMAGE_INPUT = "image_input"

    IMAGE_GENERATION = "image_generation"

    AUDIO_INPUT = "audio_input"

    AUDIO_OUTPUT = "audio_output"

    EMBEDDINGS = "embeddings"

    TOOLS = "tools"

    FUNCTION_CALLING = "function_calling"

    MODEL_LISTING = "model_listing"

    LOCAL_MODELS = "local_models"

    REMOTE_MODELS = "remote_models"


# =============================================================================
# Validation Severity
# =============================================================================


class ValidationSeverity(StrEnum):
    """
    Severity of validation messages.
    """

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"


# =============================================================================
# Configuration Scope
# =============================================================================


class ConfigurationScope(StrEnum):
    """
    Scope where a configuration is applicable.
    """

    GLOBAL = "global"

    WORKSPACE = "workspace"

    SESSION = "session"

    TEMPORARY = "temporary"


# =============================================================================
# Public Exports
# =============================================================================

__all__ = [
    "APIProvider",
    "ProviderCapability",
    "ProviderCategory",
    "CredentialType",
    "ConnectionStatus",
    "ValidationSeverity",
    "ConfigurationScope",
]