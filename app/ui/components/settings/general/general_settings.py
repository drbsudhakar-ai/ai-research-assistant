"""
AI Research Assistant
General Settings Controller

Main controller for General Settings module.

Responsibilities:
    - Initialize General Settings state
    - Render settings sections
    - Coordinate save/reset actions
    - Provide interface for settings page

No direct business logic.
No persistence implementation.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from .state import GeneralSettingsState

from .sections import (
    AppearanceSection,
    ApplicationSection,
    StorageSection,
)

from .components import (
    SaveActions,
)


class GeneralSettings:
    """
    General Settings module controller.
    """


    def __init__(
        self,
        state: GeneralSettingsState | None = None,
    ) -> None:
        """
        Initialize General Settings.

        Args:
            state:
                Optional existing settings state.
        """

        self.state = (
            state
            if state is not None
            else GeneralSettingsState.load_defaults()
        )


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render complete General Settings UI.
        """

        st.header(
            "⚙️ General Settings"
        )

        st.caption(
            "Manage application preferences, "
            "appearance, and local storage."
        )


        self._render_sections()

        self._render_actions()


    # ========================================================
    # Sections
    # ========================================================

    def _render_sections(self) -> None:
        """
        Render settings sections.
        """

        appearance = AppearanceSection(
            self.state
        )

        application = ApplicationSection(
            self.state
        )

        storage = StorageSection(
            self.state
        )


        appearance.render()

        st.divider()

        application.render()

        st.divider()

        storage.render()


    # ========================================================
    # Actions
    # ========================================================

    def _render_actions(self) -> None:
        """
        Render save/reset actions.
        """

        actions = SaveActions(
            state=self.state,
            on_save=self._save_settings,
        )

        actions.render()


    # ========================================================
    # Persistence Hook
    # ========================================================

    def _save_settings(
        self,
        state: GeneralSettingsState,
    ) -> None:
        """
        Save callback.

        Actual persistence will be handled later by:

            app/config/settings_manager.py

        Currently keeps controller independent.
        """

        settings = (
            state.export_json_ready()
        )

        # Future integration:
        #
        # SettingsManager.save(settings)

        _ = settings


    # ========================================================
    # Public API
    # ========================================================

    def get_state(
        self,
    ) -> GeneralSettingsState:
        """
        Return current settings state.
        """

        return self.state


__all__ = [
    "GeneralSettings",
]