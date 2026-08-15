"""
app/settings/api/__init__.py

Public API exports for the API settings subsystem.

This module provides a clean import surface for:
- Provider definitions
- Metadata
- Defaults
- Validation
- Configuration models

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations


# ============================================================================
# Enums
# ============================================================================

from .enums import (
    APIProvider,
)


# ============================================================================
# Metadata
# ============================================================================

from .metadata import (
    ProviderMetadata,
    get_provider_metadata,
    get_all_provider_metadata,
    get_all_providers,
    provider_exists,
)


# ============================================================================
# Defaults
# ============================================================================

from .defaults import (
    ProviderDefaults,
    get_provider_defaults,
    get_all_provider_defaults,
    build_default_api_settings,
    build_default_provider_config,
)


# ============================================================================
# Validation
# ============================================================================

from .validators import (
    ValidationResult,
    ValidationSeverity,
    validate_provider_configuration,
    validate_complete_configuration,
    validate_api_settings,
)


# ============================================================================
# Models
# ============================================================================

from .models import (
    APIProviderConfig,
    GlobalAPISettings,
    APISettings,
    create_default_api_settings,
    load_api_settings,
)


# ============================================================================
# Package Version
# ============================================================================

__version__ = "1.0.0"


# ============================================================================
# Public Exports
# ============================================================================

__all__ = [

    # Version
    "__version__",

    # Enums
    "APIProvider",

    # Metadata
    "ProviderMetadata",
    "get_provider_metadata",
    "get_all_provider_metadata",
    "get_all_providers",
    "provider_exists",

    # Defaults
    "ProviderDefaults",
    "get_provider_defaults",
    "get_all_provider_defaults",
    "build_default_api_settings",
    "build_default_provider_config",

    # Validation
    "ValidationResult",
    "ValidationSeverity",
    "validate_provider_configuration",
    "validate_complete_configuration",
    "validate_api_settings",

    # Models
    "APIProviderConfig",
    "GlobalAPISettings",
    "APISettings",
    "create_default_api_settings",
    "load_api_settings",
]