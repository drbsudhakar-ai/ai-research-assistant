"""
app/settings/api/models.py

Typed configuration models for API provider settings.

This module defines immutable and serializable configuration
objects used throughout the application. These models are
consumed by the Settings UI, configuration manager,
provider services, validators, and import/export modules.

No UI code should exist in this module.

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict

from .defaults import (
    build_default_provider_config,
    get_provider_defaults,
)
from .enums import APIProvider


# ============================================================================
# Provider Configuration
# ============================================================================


@dataclass(slots=True)
class APIProviderConfig:
    """
    Configuration for a single LLM provider.
    """

    provider: APIProvider

    enabled: bool

    api_key: str

    base_url: str

    model: str

    timeout: int

    connect_timeout: int

    read_timeout: int

    max_retries: int

    retry_delay: float

    temperature: float

    top_p: float

    max_tokens: int

    streaming: bool

    verify_ssl: bool

    save_api_key: bool

    auto_discover_models: bool

    requests_per_minute: int

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        provider: APIProvider,
    ) -> "APIProviderConfig":
        """
        Create a provider configuration using default values.
        """
        defaults = build_default_provider_config(provider)

        return cls.from_dict(defaults)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "APIProviderConfig":
        """
        Build a configuration object from a dictionary.
        """
        provider = data.get("provider", APIProvider.OLLAMA)

        if not isinstance(provider, APIProvider):
            provider = APIProvider(provider)

        defaults = get_provider_defaults(provider)

        return cls(
            provider=provider,
            enabled=bool(
                data.get(
                    "enabled",
                    defaults.enabled,
                )
            ),
            api_key=str(
                data.get("api_key", "")
            ),
            base_url=str(
                data.get(
                    "base_url",
                    defaults.base_url,
                )
            ),
            model=str(
                data.get(
                    "model",
                    defaults.default_model,
                )
            ),
            timeout=int(
                data.get(
                    "timeout",
                    defaults.timeout,
                )
            ),
            connect_timeout=int(
                data.get(
                    "connect_timeout",
                    defaults.connect_timeout,
                )
            ),
            read_timeout=int(
                data.get(
                    "read_timeout",
                    defaults.read_timeout,
                )
            ),
            max_retries=int(
                data.get(
                    "max_retries",
                    defaults.max_retries,
                )
            ),
            retry_delay=float(
                data.get(
                    "retry_delay",
                    defaults.retry_delay,
                )
            ),
            temperature=float(
                data.get(
                    "temperature",
                    defaults.temperature,
                )
            ),
            top_p=float(
                data.get(
                    "top_p",
                    defaults.top_p,
                )
            ),
            max_tokens=int(
                data.get(
                    "max_tokens",
                    defaults.max_tokens,
                )
            ),
            streaming=bool(
                data.get(
                    "streaming",
                    defaults.streaming,
                )
            ),
            verify_ssl=bool(
                data.get(
                    "verify_ssl",
                    defaults.verify_ssl,
                )
            ),
            save_api_key=bool(
                data.get(
                    "save_api_key",
                    defaults.save_api_key,
                )
            ),
            auto_discover_models=bool(
                data.get(
                    "auto_discover_models",
                    defaults.auto_discover_models,
                )
            ),
            requests_per_minute=int(
                data.get(
                    "requests_per_minute",
                    defaults.requests_per_minute,
                )
            ),
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a serializable dictionary.
        """
        data = asdict(self)
        data["provider"] = self.provider.value
        return data

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def copy(self) -> "APIProviderConfig":
        """
        Return a deep copy of the configuration.
        """
        return APIProviderConfig.from_dict(
            self.to_dict()
        )

    def reset_to_defaults(self) -> None:
        """
        Reset this configuration to provider defaults.
        """
        defaults = APIProviderConfig.create(
            self.provider
        )

        self.enabled = defaults.enabled
        self.api_key = defaults.api_key
        self.base_url = defaults.base_url
        self.model = defaults.model
        self.timeout = defaults.timeout
        self.connect_timeout = defaults.connect_timeout
        self.read_timeout = defaults.read_timeout
        self.max_retries = defaults.max_retries
        self.retry_delay = defaults.retry_delay
        self.temperature = defaults.temperature
        self.top_p = defaults.top_p
        self.max_tokens = defaults.max_tokens
        self.streaming = defaults.streaming
        self.verify_ssl = defaults.verify_ssl
        self.save_api_key = defaults.save_api_key
        self.auto_discover_models = (
            defaults.auto_discover_models
        )
        self.requests_per_minute = (
            defaults.requests_per_minute
        )
        

# ============================================================================
# Global API Settings
# ============================================================================


@dataclass(slots=True)
class GlobalAPISettings:
    """
    Application-wide API settings shared by all providers.
    """

    default_provider: APIProvider

    active_provider: APIProvider

    enable_logging: bool = True

    verify_ssl: bool = True

    test_connection_on_save: bool = True

    save_api_keys: bool = False

    streaming: bool = True

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def create(cls) -> "GlobalAPISettings":
        """
        Create a GlobalAPISettings instance with default values.
        """
        return cls(
            default_provider=APIProvider.OLLAMA,
            active_provider=APIProvider.OLLAMA,
            enable_logging=True,
            verify_ssl=True,
            test_connection_on_save=True,
            save_api_keys=False,
            streaming=True,
        )

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "GlobalAPISettings":
        """
        Create a GlobalAPISettings instance from a dictionary.
        """
        default_provider = data.get(
            "default_provider",
            APIProvider.OLLAMA,
        )

        active_provider = data.get(
            "active_provider",
            default_provider,
        )

        if not isinstance(default_provider, APIProvider):
            default_provider = APIProvider(default_provider)

        if not isinstance(active_provider, APIProvider):
            active_provider = APIProvider(active_provider)

        return cls(
            default_provider=default_provider,
            active_provider=active_provider,
            enable_logging=bool(
                data.get("enable_logging", True)
            ),
            verify_ssl=bool(
                data.get("verify_ssl", True)
            ),
            test_connection_on_save=bool(
                data.get(
                    "test_connection_on_save",
                    True,
                )
            ),
            save_api_keys=bool(
                data.get(
                    "save_api_keys",
                    False,
                )
            ),
            streaming=bool(
                data.get(
                    "streaming",
                    True,
                )
            ),
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert settings to a serializable dictionary.
        """
        return {
            "default_provider": self.default_provider.value,
            "active_provider": self.active_provider.value,
            "enable_logging": self.enable_logging,
            "verify_ssl": self.verify_ssl,
            "test_connection_on_save": (
                self.test_connection_on_save
            ),
            "save_api_keys": self.save_api_keys,
            "streaming": self.streaming,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def copy(self) -> "GlobalAPISettings":
        """
        Return a deep copy of these settings.
        """
        return GlobalAPISettings.from_dict(
            self.to_dict()
        )

    def reset_to_defaults(self) -> None:
        """
        Reset global settings to their default values.
        """
        defaults = GlobalAPISettings.create()

        self.default_provider = defaults.default_provider
        self.active_provider = defaults.active_provider
        self.enable_logging = defaults.enable_logging
        self.verify_ssl = defaults.verify_ssl
        self.test_connection_on_save = (
            defaults.test_connection_on_save
        )
        self.save_api_keys = defaults.save_api_keys
        self.streaming = defaults.streaming

    @property
    def provider_changed(self) -> bool:
        """
        Return True when the active provider differs from the
        configured default provider.
        """
        return (
            self.active_provider
            != self.default_provider
        )

    def activate(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Set the active provider.
        """
        self.active_provider = provider

    def set_default_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Set the application's default provider.
        """
        self.default_provider = provider

# ============================================================================
# Complete API Settings
# ============================================================================


@dataclass(slots=True)
class APISettings:
    """
    Complete API configuration for the application.

    This object aggregates:

    - Global API settings
    - Provider configurations

    It is the primary configuration model exchanged between the
    Settings UI, SettingsManager, import/export, and provider layer.
    """

    global_settings: GlobalAPISettings

    providers: Dict[APIProvider, APIProviderConfig]

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def create(cls) -> "APISettings":
        """
        Create a complete API settings object populated with
        provider defaults.
        """
        providers = {
            provider: APIProviderConfig.create(provider)
            for provider in APIProvider
        }

        return cls(
            global_settings=GlobalAPISettings.create(),
            providers=providers,
        )

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "APISettings":
        """
        Construct APISettings from a serialized dictionary.
        """
        global_settings = GlobalAPISettings.from_dict(
            data.get("global", {})
        )

        provider_configs: Dict[
            APIProvider,
            APIProviderConfig,
        ] = {}

        raw_providers = data.get("providers", {})

        # Build provider configurations from serialized data.
        for provider in APIProvider:
            provider_data = raw_providers.get(
                provider.value,
                {"provider": provider.value},
            )

            provider_data.setdefault(
                "provider",
                provider.value,
            )

            provider_configs[
                provider
            ] = APIProviderConfig.from_dict(
                provider_data
            )

        return cls(
            global_settings=global_settings,
            providers=provider_configs,
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the complete configuration into a serializable
        dictionary.
        """
        return {
            "global": self.global_settings.to_dict(),
            "providers": {
                provider.value: config.to_dict()
                for provider, config
                in self.providers.items()
            },
        }

    # ------------------------------------------------------------------
    # Provider Access
    # ------------------------------------------------------------------

    def get_provider(
        self,
        provider: APIProvider,
    ) -> APIProviderConfig:
        """
        Return the configuration for a provider.
        """
        return self.providers[provider]

    def set_provider(
        self,
        configuration: APIProviderConfig,
    ) -> None:
        """
        Replace the configuration for a provider.
        """
        self.providers[
            configuration.provider
        ] = configuration

    def has_provider(
        self,
        provider: APIProvider,
    ) -> bool:
        """
        Return True if the provider exists.
        """
        return provider in self.providers

    # ------------------------------------------------------------------
    # Active Provider
    # ------------------------------------------------------------------

    @property
    def active_provider(self) -> APIProvider:
        return self.global_settings.active_provider

    @property
    def active_configuration(
        self,
    ) -> APIProviderConfig:
        return self.providers[
            self.active_provider
        ]

    def activate_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Make the supplied provider active.
        """
        self.global_settings.activate(provider)

    # ------------------------------------------------------------------
    # Collection Helpers
    # ------------------------------------------------------------------

    def enabled_providers(
        self,
    ) -> Dict[APIProvider, APIProviderConfig]:
        """
        Return only enabled providers.
        """
        return {
            provider: config
            for provider, config
            in self.providers.items()
            if config.enabled
        }

    def disabled_providers(
        self,
    ) -> Dict[APIProvider, APIProviderConfig]:
        """
        Return only disabled providers.
        """
        return {
            provider: config
            for provider, config
            in self.providers.items()
            if not config.enabled
        }

    @property
    def provider_count(self) -> int:
        """
        Total configured providers.
        """
        return len(self.providers)

    @property
    def enabled_provider_count(self) -> int:
        """
        Number of enabled providers.
        """
        return sum(
            config.enabled
            for config in self.providers.values()
        )

# ============================================================================
# Utility Methods
# ============================================================================


    def copy(self) -> "APISettings":
        """
        Create a deep copy of the complete API settings.
        """
        return APISettings.from_dict(
            self.to_dict()
        )


    def reset_to_defaults(self) -> None:
        """
        Reset the entire API configuration.
        """
        defaults = APISettings.create()

        self.global_settings = (
            defaults.global_settings
        )

        self.providers = defaults.providers


    def update_provider(
        self,
        provider: APIProvider,
        values: Dict[str, Any],
    ) -> None:
        """
        Update selected fields of a provider configuration.

        Unknown fields are ignored intentionally to support
        forward compatibility with imported configurations.
        """
        if provider not in self.providers:
            self.providers[provider] = (
                APIProviderConfig.create(provider)
            )

        config = self.providers[provider]

        for key, value in values.items():

            if hasattr(config, key):

                if key == "provider":
                    continue

                setattr(
                    config,
                    key,
                    value,
                )


    def update_global(
        self,
        values: Dict[str, Any],
    ) -> None:
        """
        Update selected global settings.
        """
        for key, value in values.items():

            if hasattr(
                self.global_settings,
                key,
            ):
                setattr(
                    self.global_settings,
                    key,
                    value,
                )


    def remove_api_keys(self) -> None:
        """
        Remove stored API keys.

        Useful before exporting configuration files.
        """
        for config in self.providers.values():
            config.api_key = ""


    def validate(self):
        """
        Validate this configuration.

        Lazy import avoids circular dependency between
        models and validators.
        """
        from .validators import (
            validate_complete_configuration,
        )

        return validate_complete_configuration(
            self.to_dict()
        )


# ============================================================================
# Factory Functions
# ============================================================================


def create_default_api_settings() -> APISettings:
    """
    Create a fresh default API settings instance.
    """
    return APISettings.create()


def load_api_settings(
    data: Dict[str, Any],
) -> APISettings:
    """
    Load API settings from a dictionary.
    """
    return APISettings.from_dict(data)


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Models
    "APIProviderConfig",
    "GlobalAPISettings",
    "APISettings",

    # Factories
    "create_default_api_settings",
    "load_api_settings",
]