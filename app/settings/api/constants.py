"""
app/settings/api/constants.py

Central constants for the API settings subsystem.

This module contains:
- Configuration keys
- Environment variable names
- Schema identifiers
- Secret handling constants

No runtime configuration logic should exist here.

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations


# ============================================================================
# Configuration Schema
# ============================================================================


API_SETTINGS_SCHEMA_VERSION = "1.0"

API_SETTINGS_SCHEMA_NAME = (
    "ai_research_assistant_api_settings"
)


# ============================================================================
# Top-Level Configuration Keys
# ============================================================================


CONFIG_KEY_GLOBAL = "global"

CONFIG_KEY_PROVIDERS = "providers"

CONFIG_KEY_ACTIVE_PROVIDER = (
    "active_provider"
)

CONFIG_KEY_DEFAULT_PROVIDER = (
    "default_provider"
)


# ============================================================================
# Global Settings Keys
# ============================================================================


GLOBAL_KEY_ENABLE_LOGGING = (
    "enable_logging"
)

GLOBAL_KEY_VERIFY_SSL = (
    "verify_ssl"
)

GLOBAL_KEY_TEST_CONNECTION = (
    "test_connection_on_save"
)

GLOBAL_KEY_SAVE_API_KEYS = (
    "save_api_keys"
)

GLOBAL_KEY_STREAMING = (
    "streaming"
)


# ============================================================================
# Provider Configuration Keys
# ============================================================================


PROVIDER_KEY_NAME = (
    "provider"
)

PROVIDER_KEY_ENABLED = (
    "enabled"
)

PROVIDER_KEY_API_KEY = (
    "api_key"
)

PROVIDER_KEY_BASE_URL = (
    "base_url"
)

PROVIDER_KEY_MODEL = (
    "model"
)

PROVIDER_KEY_TIMEOUT = (
    "timeout"
)

PROVIDER_KEY_CONNECT_TIMEOUT = (
    "connect_timeout"
)

PROVIDER_KEY_READ_TIMEOUT = (
    "read_timeout"
)

PROVIDER_KEY_MAX_RETRIES = (
    "max_retries"
)

PROVIDER_KEY_RETRY_DELAY = (
    "retry_delay"
)

PROVIDER_KEY_TEMPERATURE = (
    "temperature"
)

PROVIDER_KEY_TOP_P = (
    "top_p"
)

PROVIDER_KEY_MAX_TOKENS = (
    "max_tokens"
)

PROVIDER_KEY_STREAMING = (
    "streaming"
)

PROVIDER_KEY_VERIFY_SSL = (
    "verify_ssl"
)

PROVIDER_KEY_SAVE_API_KEY = (
    "save_api_key"
)

PROVIDER_KEY_AUTO_DISCOVER_MODELS = (
    "auto_discover_models"
)

PROVIDER_KEY_REQUESTS_PER_MINUTE = (
    "requests_per_minute"
)


# ============================================================================
# Environment Variables
# ============================================================================


ENV_PREFIX = (
    "AI_RA_"
)


ENV_API_PROVIDER = (
    f"{ENV_PREFIX}API_PROVIDER"
)

ENV_OPENAI_API_KEY = (
    f"{ENV_PREFIX}OPENAI_API_KEY"
)

ENV_GEMINI_API_KEY = (
    f"{ENV_PREFIX}GEMINI_API_KEY"
)

ENV_ANTHROPIC_API_KEY = (
    f"{ENV_PREFIX}ANTHROPIC_API_KEY"
)

ENV_DEEPSEEK_API_KEY = (
    f"{ENV_PREFIX}DEEPSEEK_API_KEY"
)

ENV_OLLAMA_BASE_URL = (
    f"{ENV_PREFIX}OLLAMA_BASE_URL"
)


# ============================================================================
# Secret Handling
# ============================================================================


SECRET_FIELDS = (
    PROVIDER_KEY_API_KEY,
)


MASKED_SECRET_VALUE = (
    "********"
)


EMPTY_SECRET_VALUE = (
    ""
)


SECRET_MIN_LENGTH = 10


# ============================================================================
# File Names
# ============================================================================


DEFAULT_API_SETTINGS_FILENAME = (
    "api_settings.json"
)

BACKUP_API_SETTINGS_FILENAME = (
    "api_settings.backup.json"
)


# ============================================================================
# Validation Limits
# ============================================================================


MIN_TIMEOUT_SECONDS = 5

MAX_TIMEOUT_SECONDS = 600


MIN_CONNECT_TIMEOUT_SECONDS = 1

MAX_CONNECT_TIMEOUT_SECONDS = 120


MIN_READ_TIMEOUT_SECONDS = 5

MAX_READ_TIMEOUT_SECONDS = 900


MIN_RETRY_COUNT = 0

MAX_RETRY_COUNT = 10


MIN_RETRY_DELAY_SECONDS = 0.5

MAX_RETRY_DELAY_SECONDS = 30.0


MIN_TEMPERATURE = 0.0

MAX_TEMPERATURE = 2.0


MIN_TOP_P = 0.0

MAX_TOP_P = 1.0


MIN_MAX_TOKENS = 1

MAX_MAX_TOKENS = 1_000_000


MIN_REQUESTS_PER_MINUTE = 1

MAX_REQUESTS_PER_MINUTE = 10_000


# ============================================================================
# Provider Configuration States
# ============================================================================


PROVIDER_STATUS_ENABLED = (
    "enabled"
)

PROVIDER_STATUS_DISABLED = (
    "disabled"
)

PROVIDER_STATUS_NOT_CONFIGURED = (
    "not_configured"
)

PROVIDER_STATUS_CONNECTED = (
    "connected"
)

PROVIDER_STATUS_FAILED = (
    "failed"
)


# ============================================================================
# Connection Testing
# ============================================================================


CONNECTION_TEST_TIMEOUT = 15


CONNECTION_TEST_SUCCESS = (
    "connection_successful"
)

CONNECTION_TEST_FAILED = (
    "connection_failed"
)

CONNECTION_TEST_UNAUTHORIZED = (
    "authentication_failed"
)

CONNECTION_TEST_TIMEOUT_ERROR = (
    "connection_timeout"
)


# ============================================================================
# Import / Export
# ============================================================================


EXPORT_FORMAT_JSON = (
    "json"
)

EXPORT_FORMAT_YAML = (
    "yaml"
)


SUPPORTED_EXPORT_FORMATS = (
    EXPORT_FORMAT_JSON,
    EXPORT_FORMAT_YAML,
)


EXPORT_INCLUDE_SECRETS = (
    "include_secrets"
)

EXPORT_REMOVE_SECRETS = (
    "remove_secrets"
)


DEFAULT_EXPORT_REMOVE_SECRETS = True


# ============================================================================
# Configuration Change Tracking
# ============================================================================


CHANGE_CREATED = (
    "created"
)

CHANGE_UPDATED = (
    "updated"
)

CHANGE_DELETED = (
    "deleted"
)

CHANGE_RESET = (
    "reset"
)


# ============================================================================
# Provider Field Groups
# ============================================================================


CONNECTION_FIELDS = (
    PROVIDER_KEY_BASE_URL,
    PROVIDER_KEY_API_KEY,
    PROVIDER_KEY_TIMEOUT,
)


MODEL_FIELDS = (
    PROVIDER_KEY_MODEL,
    PROVIDER_KEY_TEMPERATURE,
    PROVIDER_KEY_TOP_P,
    PROVIDER_KEY_MAX_TOKENS,
)


RETRY_FIELDS = (
    PROVIDER_KEY_MAX_RETRIES,
    PROVIDER_KEY_RETRY_DELAY,
)


BEHAVIOR_FIELDS = (
    PROVIDER_KEY_STREAMING,
    PROVIDER_KEY_VERIFY_SSL,
    PROVIDER_KEY_AUTO_DISCOVER_MODELS,
)


# ============================================================================
# UI Integration Keys
# ============================================================================


UI_SECTION_PROVIDER = (
    "provider"
)

UI_SECTION_CONNECTION = (
    "connection"
)

UI_SECTION_MODEL = (
    "model"
)

UI_SECTION_ADVANCED = (
    "advanced"
)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [

    # Schema
    "API_SETTINGS_SCHEMA_VERSION",
    "API_SETTINGS_SCHEMA_NAME",

    # Configuration keys
    "CONFIG_KEY_GLOBAL",
    "CONFIG_KEY_PROVIDERS",
    "CONFIG_KEY_ACTIVE_PROVIDER",
    "CONFIG_KEY_DEFAULT_PROVIDER",

    # Provider keys
    "PROVIDER_KEY_NAME",
    "PROVIDER_KEY_ENABLED",
    "PROVIDER_KEY_API_KEY",
    "PROVIDER_KEY_BASE_URL",
    "PROVIDER_KEY_MODEL",
    "PROVIDER_KEY_TIMEOUT",
    "PROVIDER_KEY_CONNECT_TIMEOUT",
    "PROVIDER_KEY_READ_TIMEOUT",
    "PROVIDER_KEY_MAX_RETRIES",
    "PROVIDER_KEY_RETRY_DELAY",
    "PROVIDER_KEY_TEMPERATURE",
    "PROVIDER_KEY_TOP_P",
    "PROVIDER_KEY_MAX_TOKENS",
    "PROVIDER_KEY_STREAMING",
    "PROVIDER_KEY_VERIFY_SSL",
    "PROVIDER_KEY_SAVE_API_KEY",
    "PROVIDER_KEY_AUTO_DISCOVER_MODELS",
    "PROVIDER_KEY_REQUESTS_PER_MINUTE",

    # Environment
    "ENV_PREFIX",
    "ENV_API_PROVIDER",
    "ENV_OPENAI_API_KEY",
    "ENV_GEMINI_API_KEY",
    "ENV_ANTHROPIC_API_KEY",
    "ENV_DEEPSEEK_API_KEY",
    "ENV_OLLAMA_BASE_URL",

    # Secrets
    "SECRET_FIELDS",
    "MASKED_SECRET_VALUE",
    "EMPTY_SECRET_VALUE",
    "SECRET_MIN_LENGTH",

    # Validation limits
    "MIN_TIMEOUT_SECONDS",
    "MAX_TIMEOUT_SECONDS",
    "MIN_RETRY_COUNT",
    "MAX_RETRY_COUNT",
    "MIN_TEMPERATURE",
    "MAX_TEMPERATURE",
    "MIN_TOP_P",
    "MAX_TOP_P",
    "MIN_MAX_TOKENS",
    "MAX_MAX_TOKENS",

    # Connection testing
    "CONNECTION_TEST_TIMEOUT",
    "CONNECTION_TEST_SUCCESS",
    "CONNECTION_TEST_FAILED",

    # Export
    "EXPORT_FORMAT_JSON",
    "EXPORT_FORMAT_YAML",
    "SUPPORTED_EXPORT_FORMATS",
    "DEFAULT_EXPORT_REMOVE_SECRETS",

    # Field groups
    "CONNECTION_FIELDS",
    "MODEL_FIELDS",
    "RETRY_FIELDS",
    "BEHAVIOR_FIELDS",

    # UI
    "UI_SECTION_PROVIDER",
    "UI_SECTION_CONNECTION",
    "UI_SECTION_MODEL",
    "UI_SECTION_ADVANCED",
]