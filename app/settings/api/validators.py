"""
app/settings/api/validators.py

Production-ready validation utilities for API provider settings.

This module provides reusable validation logic for provider
configuration, global API settings, import/export validation,
and future configuration management.

No UI framework code should exist in this module.

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List
from urllib.parse import urlparse

from .enums import APIProvider


# ============================================================================
# Validation Severity
# ============================================================================


class ValidationSeverity(str, Enum):
    """
    Validation message severity.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# ============================================================================
# Validation Result
# ============================================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned from validation routines.
    """

    valid: bool = True

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    info: List[str] = field(default_factory=list)

    severity: ValidationSeverity = ValidationSeverity.INFO

    def add_error(self, message: str) -> None:
        self.valid = False
        self.severity = ValidationSeverity.ERROR
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        if self.severity != ValidationSeverity.ERROR:
            self.severity = ValidationSeverity.WARNING
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        self.info.append(message)

    def merge(self, other: "ValidationResult") -> None:
        """
        Merge another ValidationResult.
        """
        if not other.valid:
            self.valid = False

        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)

        if self.errors:
            self.severity = ValidationSeverity.ERROR
        elif self.warnings:
            self.severity = ValidationSeverity.WARNING

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    @property
    def has_warnings(self) -> bool:
        return bool(self.warnings)


# ============================================================================
# Generic Validators
# ============================================================================


def validate_required(
    value: str,
    field_name: str,
) -> ValidationResult:
    """
    Validate a required text field.
    """
    result = ValidationResult()

    if not str(value).strip():
        result.add_error(f"{field_name} is required.")

    return result


def validate_url(url: str) -> ValidationResult:
    """
    Validate an HTTP/HTTPS URL.
    """
    result = ValidationResult()

    url = url.strip()

    if not url:
        result.add_error("Base URL is required.")
        return result

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            result.add_error(
                "URL must begin with http:// or https://."
            )

        if not parsed.netloc:
            result.add_error("Invalid host name.")

    except Exception:
        result.add_error("Invalid URL format.")

    return result


def validate_api_key(
    api_key: str,
    provider: APIProvider,
    required: bool = True,
) -> ValidationResult:
    """
    Validate an API key.
    """
    result = ValidationResult()

    api_key = api_key.strip()

    if not api_key:
        if (
            required
            and provider != APIProvider.OLLAMA
        ):
            result.add_error("API key is required.")
        return result

    if len(api_key) < 10:
        result.add_warning(
            "API key appears unusually short."
        )

    return result


def validate_model_name(model: str) -> ValidationResult:
    """
    Validate a model name.
    """
    result = ValidationResult()

    model = model.strip()

    if not model:
        result.add_error("Model name is required.")
        return result

    if len(model) > 150:
        result.add_error(
            "Model name is too long."
        )

    return result


def validate_timeout(timeout: int) -> ValidationResult:
    """
    Validate request timeout.
    """
    result = ValidationResult()

    if timeout <= 0:
        result.add_error(
            "Timeout must be greater than zero."
        )
    elif timeout < 5:
        result.add_warning(
            "Very small timeout may cause failures."
        )
    elif timeout > 600:
        result.add_warning(
            "Large timeout may delay failure detection."
        )

    return result


def validate_retry_count(
    retries: int,
) -> ValidationResult:
    """
    Validate retry count.
    """
    result = ValidationResult()

    if retries < 0:
        result.add_error(
            "Retry count cannot be negative."
        )
    elif retries > 10:
        result.add_warning(
            "Retry count is unusually high."
        )

    return result


def validate_temperature(
    temperature: float,
) -> ValidationResult:
    """
    Validate model temperature.
    """
    result = ValidationResult()

    if not 0.0 <= temperature <= 2.0:
        result.add_error(
            "Temperature must be between 0.0 and 2.0."
        )

    return result


def validate_top_p(
    top_p: float,
) -> ValidationResult:
    """
    Validate nucleus sampling value.
    """
    result = ValidationResult()

    if not 0.0 <= top_p <= 1.0:
        result.add_error(
            "Top-p must be between 0.0 and 1.0."
        )

    return result


def validate_max_tokens(
    max_tokens: int,
) -> ValidationResult:
    """
    Validate maximum token count.
    """
    result = ValidationResult()

    if max_tokens <= 0:
        result.add_error(
            "Maximum tokens must be greater than zero."
        )
    elif max_tokens > 1_000_000:
        result.add_warning(
            "Maximum tokens is unusually large."
        )

    return result

# ============================================================================
# Provider-Specific Validators
# ============================================================================


def validate_base_url(
    provider: APIProvider,
    base_url: str,
) -> ValidationResult:
    """
    Validate the provider base URL.

    Provider-specific rules may be added here as additional
    providers are supported.
    """
    result = validate_url(base_url)

    if not result.valid:
        return result

    url = base_url.lower()

    if provider == APIProvider.OLLAMA:
        if not (
            url.startswith("http://")
            or url.startswith("https://")
        ):
            result.add_error(
                "Ollama endpoint must use HTTP or HTTPS."
            )

    return result


def validate_provider_configuration(
    config: dict,
) -> tuple[bool, str]:
    """
    Validate a provider configuration.

    Parameters
    ----------
    config:
        Provider configuration dictionary.

    Returns
    -------
    tuple[bool, str]
        (is_valid, message)

    This return type intentionally matches the existing UI usage,
    e.g.:

        valid, message = validate_provider_configuration(state)
    """
    validation = ValidationResult()

    provider_value = config.get("provider")

    if not provider_value:
        validation.add_error("Provider is required.")
        return False, validation.errors[0]

    try:
        provider = (
            provider_value
            if isinstance(provider_value, APIProvider)
            else APIProvider(provider_value)
        )
    except Exception:
        return False, "Unsupported provider."

    validation.merge(
        validate_base_url(
            provider,
            str(config.get("base_url", "")),
        )
    )

    validation.merge(
        validate_api_key(
            str(config.get("api_key", "")),
            provider,
            required=True,
        )
    )

    validation.merge(
        validate_model_name(
            str(config.get("model", ""))
        )
    )

    validation.merge(
        validate_timeout(
            int(config.get("timeout", 120))
        )
    )

    validation.merge(
        validate_retry_count(
            int(config.get("max_retries", 3))
        )
    )

    validation.merge(
        validate_temperature(
            float(config.get("temperature", 0.2))
        )
    )

    validation.merge(
        validate_top_p(
            float(config.get("top_p", 0.95))
        )
    )

    validation.merge(
        validate_max_tokens(
            int(config.get("max_tokens", 4096))
        )
    )

    # ------------------------------------------------------------------
    # Provider-specific recommendations
    # ------------------------------------------------------------------

    if provider == APIProvider.OLLAMA:
        base_url = str(
            config.get("base_url", "")
        ).lower()

        if "localhost" not in base_url and "127.0.0.1" not in base_url:
            validation.add_warning(
                "Ollama is typically hosted on localhost."
            )

    if provider == APIProvider.OPENAI:
        model = str(config.get("model", ""))

        if model.startswith("gpt-3"):
            validation.add_warning(
                "GPT-3 models are legacy models."
            )

    if provider == APIProvider.GEMINI:
        if not str(config.get("api_key", "")).startswith("AIza"):
            validation.add_warning(
                "Gemini API keys usually begin with 'AIza'."
            )

    if provider == APIProvider.DEEPSEEK:
        if (
            str(config.get("base_url", ""))
            .rstrip("/")
            != "https://api.deepseek.com"
        ):
            validation.add_info(
                "Using a custom DeepSeek endpoint."
            )

    # ------------------------------------------------------------------
    # Return
    # ------------------------------------------------------------------

    if validation.errors:
        return False, validation.errors[0]

    if validation.warnings:
        return True, validation.warnings[0]

    return True, "Configuration is valid."


# ============================================================================
# Batch Provider Validation
# ============================================================================


def validate_provider_collection(
    providers: dict,
) -> ValidationResult:
    """
    Validate multiple provider configurations.

    Parameters
    ----------
    providers:
        Mapping of provider name -> configuration.
    """
    result = ValidationResult()

    if not providers:
        result.add_error(
            "No provider configurations found."
        )
        return result

    for provider_name, configuration in providers.items():
        valid, message = validate_provider_configuration(
            configuration
        )

        if not valid:
            result.add_error(
                f"{provider_name}: {message}"
            )

    return result

# ============================================================================
# Global Settings Validation
# ============================================================================


def validate_api_settings(settings: dict) -> ValidationResult:
    """
    Validate global API settings.

    Parameters
    ----------
    settings:
        Global API settings dictionary.
    """
    result = ValidationResult()

    if not isinstance(settings, dict):
        result.add_error("Settings must be a dictionary.")
        return result

    timeout = settings.get("timeout")
    if timeout is not None:
        result.merge(validate_timeout(int(timeout)))

    retries = settings.get("max_retries")
    if retries is not None:
        result.merge(validate_retry_count(int(retries)))

    temperature = settings.get("temperature")
    if temperature is not None:
        result.merge(validate_temperature(float(temperature)))

    top_p = settings.get("top_p")
    if top_p is not None:
        result.merge(validate_top_p(float(top_p)))

    max_tokens = settings.get("max_tokens")
    if max_tokens is not None:
        result.merge(validate_max_tokens(int(max_tokens)))

    default_provider = settings.get("default_provider")
    if default_provider is not None:
        try:
            if not isinstance(default_provider, APIProvider):
                APIProvider(default_provider)
        except Exception:
            result.add_error(
                f"Unsupported default provider '{default_provider}'."
            )

    return result


# ============================================================================
# Complete Configuration Validation
# ============================================================================


def validate_complete_configuration(
    configuration: dict,
) -> ValidationResult:
    """
    Validate the complete API configuration structure.

    Expected structure::

        {
            "global": {...},
            "providers": {
                "ollama": {...},
                "openai": {...}
            }
        }
    """
    result = ValidationResult()

    if not isinstance(configuration, dict):
        result.add_error("Configuration must be a dictionary.")
        return result

    global_settings = configuration.get("global", {})
    result.merge(validate_api_settings(global_settings))

    providers = configuration.get("providers")

    if providers is None:
        result.add_error("Missing 'providers' section.")
        return result

    result.merge(
        validate_provider_collection(providers)
    )

    enabled_count = 0

    for provider_cfg in providers.values():
        if provider_cfg.get("enabled", False):
            enabled_count += 1

    if enabled_count == 0:
        result.add_warning(
            "No providers are currently enabled."
        )

    return result


# ============================================================================
# Message Helpers
# ============================================================================


def summarize_validation(
    result: ValidationResult,
) -> str:
    """
    Return a concise validation summary.
    """
    if result.has_errors:
        return result.errors[0]

    if result.has_warnings:
        return result.warnings[0]

    return "Validation successful."


def validation_statistics(
    result: ValidationResult,
) -> dict[str, int]:
    """
    Return validation statistics.
    """
    return {
        "errors": len(result.errors),
        "warnings": len(result.warnings),
        "info": len(result.info),
    }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    "ValidationSeverity",

    # Models
    "ValidationResult",

    # Generic validators
    "validate_required",
    "validate_url",
    "validate_api_key",
    "validate_model_name",
    "validate_timeout",
    "validate_retry_count",
    "validate_temperature",
    "validate_top_p",
    "validate_max_tokens",

    # Provider validators
    "validate_base_url",
    "validate_provider_configuration",
    "validate_provider_collection",

    # Global validators
    "validate_api_settings",
    "validate_complete_configuration",

    # Helpers
    "summarize_validation",
    "validation_statistics",
]