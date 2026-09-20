"""
app/config/settings_manager.py

Persisted user-editable API settings manager.

Classification (T002):
    CANONICAL for persisted Settings-UI API settings (JSON file)
    NOT the runtime ApplicationConfig boundary

Runtime analysis configuration is ``ApplicationConfig`` loaded by
``app.config.loader``. This manager must not be treated as a second
independent runtime source. Settings UI (T016) may later apply user
settings onto ApplicationConfig through an explicit merge.

Secrets:
    ``export_settings(include_secrets=False)`` strips API keys.
    ``safe_diagnostics()`` never includes secret values.

Author : AI Research Assistant
Version: 2.1.0
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from app.config.loader import get_application_config
from app.settings.api import (
    APIProvider,
    APIProviderConfig,
    APISettings,
    ValidationResult,
    create_default_api_settings,
    validate_complete_configuration,
)


# ============================================================================
# Settings Manager
# ============================================================================


class SettingsManager:
    """
    Application-wide settings manager.

    Provides a single access point for configuration handling.
    """

    _instance: Optional["SettingsManager"] = None


    def __new__(cls):
        """
        Singleton implementation.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(self) -> None:
        """
        Initialize settings manager.
        """

        if getattr(
            self,
            "_initialized",
            False,
        ):
            return

        self.settings: APISettings = (
            create_default_api_settings()
        )

        runtime_paths = get_application_config().paths
        self.config_path: Path = runtime_paths.settings_file
        self.backup_path: Path = (
            runtime_paths.config_dir / "settings.backup.json"
        )

        self._initialized = True

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------


    def initialize(
        self,
        config_path: Optional[str] = None,
    ) -> None:
        """
        Initialize settings from disk.

        If no configuration exists,
        default settings are created.
        """

        if config_path:
            self.config_path = Path(config_path)

        if self.config_path.exists():
            self.load()

        else:
            self.settings = (
                create_default_api_settings()
            )


    def reset(self) -> None:
        """
        Reset all settings to application defaults.
        """
        self.settings = (
            create_default_api_settings()
        )


    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------


    def get_settings(self) -> APISettings:
        """
        Return current settings.

        Recovers from incomplete singleton initialization.
        """

        if not hasattr(
            self,
            "settings",
        ):
            self.settings = (
                create_default_api_settings()
            )

        return self.settings


    def get_active_provider(
        self,
    ) -> APIProvider:
        """
        Return currently active provider.
        """
        return (
            self.settings.active_provider
        )


    def get_provider_config(
        self,
        provider: APIProvider,
    ) -> APIProviderConfig:
        """
        Return provider configuration.
        """
        return (
            self.settings.get_provider(provider)
        )


# ============================================================================
# Persistence
# ============================================================================


    def load(self) -> None:
        """
        Load settings from the configuration file.

        Invalid or corrupted configuration files are handled
        safely by falling back to defaults.
        """

        try:

            with self.config_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)


            validation = validate_complete_configuration(
                data
            )


            if validation.has_errors:

                self.settings = (
                    create_default_api_settings()
                )

                return


            self.settings = (
                APISettings.from_dict(data)
            )


        except (
            FileNotFoundError,
            json.JSONDecodeError,
            OSError,
        ):

            self.settings = (
                create_default_api_settings()
            )


    def save(
        self,
        create_backup: bool = True,
    ) -> bool:
        """
        Save settings to disk.

        Parameters
        ----------
        create_backup:
            Create backup before overwriting.

        Returns
        -------
        bool
            True if save succeeds.
        """

        try:

            self.config_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )


            if (
                create_backup
                and self.config_path.exists()
            ):
                self.create_backup()


            with self.config_path.open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    self.settings.to_dict(),
                    file,
                    indent=4,
                )


            return True


        except OSError:

            return False



    def create_backup(self) -> bool:
        """
        Create a backup copy of current settings.
        """

        try:

            self.backup_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )


            with self.config_path.open(
                "r",
                encoding="utf-8",
            ) as source:

                data = json.load(source)


            with self.backup_path.open(
                "w",
                encoding="utf-8",
            ) as backup:

                json.dump(
                    data,
                    backup,
                    indent=4,
                )


            return True


        except (
            OSError,
            json.JSONDecodeError,
        ):

            return False



    def exists(self) -> bool:
        """
        Check whether configuration exists.
        """
        return self.config_path.exists()



    # ------------------------------------------------------------------
    # Raw Serialization
    # ------------------------------------------------------------------


    def to_dict(self) -> Dict[str, Any]:
        """
        Return current configuration as dictionary.
        """
        return self.settings.to_dict()



    def from_dict(
        self,
        data: Dict[str, Any],
    ) -> None:
        """
        Replace current settings from dictionary.
        """
        self.settings = (
            APISettings.from_dict(data)
        )

# ============================================================================
# Provider Management
# ============================================================================


    def set_active_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Change the currently active provider.
        """
        self.settings.activate_provider(
            provider
        )



    def enable_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Enable a provider.
        """
        config = (
            self.settings.get_provider(provider)
        )

        config.enabled = True



    def disable_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Disable a provider.
        """
        config = (
            self.settings.get_provider(provider)
        )

        config.enabled = False



    def update_provider(
        self,
        provider: APIProvider,
        values: Dict[str, Any],
    ) -> None:
        """
        Update provider configuration fields.
        """
        self.settings.update_provider(
            provider,
            values,
        )



    def update_active_provider(
        self,
        values: Dict[str, Any],
    ) -> None:
        """
        Update currently active provider.
        """
        self.update_provider(
            self.get_active_provider(),
            values,
        )



    def get_enabled_providers(
        self,
    ) -> Dict[APIProvider, APIProviderConfig]:
        """
        Return enabled providers.
        """
        return (
            self.settings.enabled_providers()
        )



    def provider_available(
        self,
        provider: APIProvider,
    ) -> bool:
        """
        Check whether provider exists.
        """
        return self.settings.has_provider(
            provider
        )


# ============================================================================
# API Key Management
# ============================================================================


    def set_api_key(
        self,
        provider: APIProvider,
        api_key: str,
    ) -> None:
        """
        Store provider API key.
        """
        config = (
            self.settings.get_provider(provider)
        )

        config.api_key = api_key.strip()



    def get_api_key(
        self,
        provider: APIProvider,
    ) -> str:
        """
        Retrieve provider API key.
        """
        config = (
            self.settings.get_provider(provider)
        )

        return config.api_key



    def remove_api_keys(self) -> None:
        """
        Remove all API keys.

        Useful before exporting configurations.
        """
        self.settings.remove_api_keys()



    def has_api_key(
        self,
        provider: APIProvider,
    ) -> bool:
        """
        Check whether provider has an API key.
        """
        return bool(
            self.get_api_key(provider)
        )


# ============================================================================
# Validation
# ============================================================================


    def validate(
        self,
    ) -> ValidationResult:
        """
        Validate current settings.
        """
        return self.settings.validate()



    def validate_provider(
        self,
        provider: APIProvider,
    ) -> ValidationResult:
        """
        Validate a single provider.
        """
        config = (
            self.settings.get_provider(provider)
        )

        return self.settings.validate()



    def is_valid(
        self,
    ) -> bool:
        """
        Return True when configuration is valid.
        """
        return self.validate().valid


# ============================================================================
# Import / Export
# ============================================================================


    def export_settings(
        self,
        include_secrets: bool = False,
    ) -> Dict[str, Any]:
        """
        Export settings as a dictionary.

        Parameters
        ----------
        include_secrets:
            Include API keys when True.

        Returns
        -------
        dict
            Serializable configuration.
        """

        data = self.settings.to_dict()


        if not include_secrets:

            for provider in data.get(
                "providers",
                {},
            ).values():

                provider["api_key"] = ""


        return data


    def safe_diagnostics(self) -> Dict[str, Any]:
        """
        Return a UI-safe summary with secrets removed.
        """

        settings = self.get_settings()
        return {
            "active_provider": settings.active_provider.value,
            "config_path": str(self.config_path),
            "export": self.export_settings(include_secrets=False),
        }



    def import_settings(
        self,
        data: Dict[str, Any],
        validate: bool = True,
    ) -> ValidationResult:
        """
        Import settings from dictionary.

        Parameters
        ----------
        data:
            Configuration dictionary.

        validate:
            Validate before applying.

        Returns
        -------
        ValidationResult
        """

        if validate:

            result = validate_complete_configuration(
                data
            )


            if result.has_errors:

                return result


        self.settings = (
            APISettings.from_dict(data)
        )


        return ValidationResult()



    def export_json(
        self,
        path: str,
        include_secrets: bool = False,
    ) -> bool:
        """
        Export settings to JSON file.
        """

        try:

            with Path(path).open(
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    self.export_settings(
                        include_secrets
                    ),
                    file,
                    indent=4,
                )


            return True


        except OSError:

            return False



    def import_json(
        self,
        path: str,
    ) -> ValidationResult:
        """
        Import settings from JSON file.
        """

        try:

            with Path(path).open(
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)


            return self.import_settings(
                data
            )


        except (
            OSError,
            json.JSONDecodeError,
        ):

            result = ValidationResult()

            result.add_error(
                "Unable to read settings file."
            )

            return result



# ============================================================================
# Utility Helpers
# ============================================================================


    def active_model(self) -> str:
        """
        Return model name of active provider.
        """
        return (
            self.settings
            .active_configuration
            .model
        )



    def active_base_url(self) -> str:
        """
        Return API endpoint of active provider.
        """
        return (
            self.settings
            .active_configuration
            .base_url
        )



    def active_configuration(
        self,
    ) -> APIProviderConfig:
        """
        Return active provider configuration.
        """
        return (
            self.settings.active_configuration
        )



    def provider_count(self) -> int:
        """
        Return total providers.
        """
        return (
            self.settings.provider_count
        )



    def enabled_provider_count(self) -> int:
        """
        Return enabled provider count.
        """
        return (
            self.settings
            .enabled_provider_count
        )


# ============================================================================
# Singleton Accessor
# ============================================================================


_settings_manager: Optional[SettingsManager] = None



def get_settings_manager() -> SettingsManager:
    """
    Return application-wide SettingsManager instance.
    """

    global _settings_manager


    if _settings_manager is None:

        _settings_manager = (
            SettingsManager()
        )


    return _settings_manager



# ============================================================================
# Module Exports
# ============================================================================


__all__ = [
    "SettingsManager",
    "get_settings_manager",
]