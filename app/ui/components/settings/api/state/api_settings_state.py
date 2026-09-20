"""
app/ui/components/settings/api/state/api_settings_state.py

Streamlit state adapter for API Settings UI.

This module manages temporary UI state separately from
the application configuration layer.

Responsibilities:
- Load settings into UI state
- Track unsaved changes
- Update provider settings
- Commit changes

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from app.config.settings_manager import (
    get_settings_manager,
)

from app.settings.api import (
    APIProvider,
    APISettings,
    APIProviderConfig,
)


# ============================================================================
# Constants
# ============================================================================


SESSION_KEY = (
    "api_settings_state"
)


# ============================================================================
# API Settings UI State
# ============================================================================


@dataclass
class APISettingsState:
    """
    UI state container for API settings.

    This object represents the editable copy of
    application settings.
    """

    settings: APISettings

    changed: bool = False

    loaded: bool = False


    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------


    @classmethod
    def create(cls) -> "APISettingsState":
        """
        Create state from application settings.
        """

        manager = (
            get_settings_manager()
        )

        return cls(
            settings=manager.get_settings()
            .copy(),
            changed=False,
            loaded=True,
        )


    def reload(self) -> None:
        """
        Reload settings from SettingsManager.
        """

        manager = (
            get_settings_manager()
        )

        self.settings = (
            manager
            .get_settings()
            .copy()
        )

        self.changed = False

        self.loaded = True


    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------


    @property
    def active_provider(
        self,
    ) -> APIProvider:
        """
        Return selected provider.
        """
        return (
            self.settings
            .active_provider
        )


    @property
    def active_configuration(
        self,
    ) -> APIProviderConfig:
        """
        Return current provider configuration.
        """
        return (
            self.settings
            .active_configuration
        )


    def get_provider(
        self,
        provider: APIProvider,
    ) -> APIProviderConfig:
        """
        Return provider configuration.
        """
        return (
            self.settings
            .get_provider(provider)
        )

# ============================================================================
# Update Operations
# ============================================================================


    def update_provider(
        self,
        provider: APIProvider,
        values: Dict[str, Any],
    ) -> None:
        """
        Update provider configuration values.

        Changes are applied only to the UI copy.
        They are committed to application settings
        only after save.
        """

        self.settings.update_provider(
            provider,
            values,
        )

        self.changed = True



    def update_active_provider(
        self,
        values: Dict[str, Any],
    ) -> None:
        """
        Update active provider configuration.
        """

        self.update_provider(
            self.active_provider,
            values,
        )



    def set_active_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Change active provider.

        This does not save immediately.
        """

        if (
            provider
            != self.settings.active_provider
        ):

            self.settings.activate_provider(
                provider
            )

            self.changed = True



    # ------------------------------------------------------------------
    # Provider State
    # ------------------------------------------------------------------


    def enable_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Enable a provider.
        """

        config = (
            self.settings
            .get_provider(provider)
        )

        config.enabled = True

        self.changed = True



    def disable_provider(
        self,
        provider: APIProvider,
    ) -> None:
        """
        Disable a provider.
        """

        config = (
            self.settings
            .get_provider(provider)
        )

        config.enabled = False

        self.changed = True



    def set_api_key(
        self,
        provider: APIProvider,
        api_key: str,
    ) -> None:
        """
        Update provider API key.
        """

        config = (
            self.settings
            .get_provider(provider)
        )

        config.api_key = (
            api_key.strip()
        )

        self.changed = True



    def clear_api_keys(self) -> None:
        """
        Remove all API keys from UI state.
        """

        self.settings.remove_api_keys()

        self.changed = True



# ============================================================================
# Change Tracking
# ============================================================================


    def mark_saved(self) -> None:
        """
        Mark current state as synchronized.
        """

        self.changed = False



    def has_changes(self) -> bool:
        """
        Return whether unsaved changes exist.
        """

        return self.changed



    def snapshot(self) -> Dict[str, Any]:
        """
        Return current UI state snapshot.

        Useful for debugging and tests.
        """

        return self.settings.to_dict()



    def reset_changes(self) -> None:
        """
        Discard UI changes and reload
        from application configuration.
        """

        self.reload()

# ============================================================================
# Persistence Integration
# ============================================================================


    def validate(self):
        """
        Validate current UI state.

        Delegates validation to APISettings model.
        """
        return self.settings.validate()



    def save(self) -> bool:
        """
        Commit UI changes to application settings.

        Returns
        -------
        bool
            True when save succeeds.
        """

        validation = self.validate()

        if validation.has_errors:
            return False


        manager = (
            get_settings_manager()
        )

        manager.from_dict(
            self.settings.to_dict()
        )

        success = manager.save()


        if success:
            self.changed = False


        return success



    def discard(self) -> None:
        """
        Discard current UI changes.
        """

        self.reload()



    def reset_to_defaults(self) -> None:
        """
        Reset UI state to default configuration.
        """

        self.settings.reset_to_defaults()

        self.changed = True



# ============================================================================
# Streamlit Session State Integration
# ============================================================================


def get_api_settings_state() -> APISettingsState:
    """
    Return API settings UI state.

    Creates the state object inside Streamlit session
    state if it does not already exist.
    """

    import streamlit as st


    if SESSION_KEY not in st.session_state:

        st.session_state[SESSION_KEY] = (
            APISettingsState.create()
        )


    return st.session_state[
        SESSION_KEY
    ]



def reset_api_settings_state() -> None:
    """
    Remove API settings UI state from session.
    """

    import streamlit as st


    if SESSION_KEY in st.session_state:

        del st.session_state[
            SESSION_KEY
        ]



def initialize_api_settings_state() -> APISettingsState:
    """
    Initialize and return API settings state.

    Intended to be called by the settings page.
    """

    state = get_api_settings_state()


    if not state.loaded:

        state.reload()


    return state



# ============================================================================
# Convenience Functions
# ============================================================================


def save_api_settings() -> bool:
    """
    Save current API settings state.
    """

    state = (
        get_api_settings_state()
    )

    return state.save()



def discard_api_settings_changes() -> None:
    """
    Discard pending API settings changes.
    """

    state = (
        get_api_settings_state()
    )

    state.discard()



# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "APISettingsState",
    "get_api_settings_state",
    "initialize_api_settings_state",
    "reset_api_settings_state",
    "save_api_settings",
    "discard_api_settings_changes",
]