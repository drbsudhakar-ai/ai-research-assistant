"""
AI Research Assistant

File: app/ui/components/settings/pipeline/pipeline_settings.py
Pipeline Settings Controller

Main controller for Pipeline Settings UI.

Responsibilities:
    - Initialize pipeline settings state
    - Render settings sections
    - Handle save/reset actions
    - Provide integration point for Settings page

Architecture:

    settings.py
          |
          ▼
    PipelineSettings
          |
          ├── AnalysisSection
          ├── ProcessingSection
          ├── PerformanceSection
          │
          └── SaveActions

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from .state import (
    PipelineSettingsState,
)

from .sections import (
    AnalysisSection,
    ProcessingSection,
    PerformanceSection,
)

from .components import (
    SaveActions,
)


class PipelineSettings:
    """
    Pipeline Settings UI controller.
    """


    def __init__(
        self,
        state: PipelineSettingsState | None = None,
    ) -> None:
        """
        Initialize Pipeline Settings.

        Args:
            state:
                Existing settings state.
                If None, defaults are loaded.
        """

        self.state = (
            state
            if state
            else PipelineSettingsState.load_defaults()
        )


    # ========================================================
    # Public Render API
    # ========================================================

    def render(self) -> None:
        """
        Render complete Pipeline Settings page.
        """

        self._render_header()

        st.divider()

        self._render_sections()

        st.divider()

        self._render_actions()


    # ========================================================
    # Header
    # ========================================================

    def _render_header(self) -> None:
        """
        Render page heading.
        """

        st.title(
            "⚙️ Pipeline Settings"
        )

        st.caption(
            "Configure research analysis workflow, "
            "processing behaviour, and performance."
        )


    # ========================================================
    # Sections
    # ========================================================

    def _render_sections(self) -> None:
        """
        Render configuration sections.
        """

        AnalysisSection(
            state=self.state,
        ).render()


        st.divider()


        ProcessingSection(
            state=self.state,
        ).render()


        st.divider()


        PerformanceSection(
            state=self.state,
        ).render()


    # ========================================================
    # Actions
    # ========================================================

    def _render_actions(self) -> None:
        """
        Render save/reset actions.
        """

        SaveActions(
            state=self.state,
            on_save=self._save_settings,
            on_reset=self._reset_settings,
        ).render()


    # ========================================================
    # Callbacks
    # ========================================================

    def _save_settings(
        self,
        state: PipelineSettingsState,
    ) -> None:
        """
        Save callback.

        Future integration:
            SettingsManager
            Config persistence
            JSON export
        """

        state.mark_saved()


    def _reset_settings(
        self,
        state: PipelineSettingsState,
    ) -> None:
        """
        Reset callback.
        """

        state.reset()


    # ========================================================
    # State Access
    # ========================================================

    def get_state(
        self,
    ) -> PipelineSettingsState:
        """
        Return current state.

        Useful for:
            - Settings manager
            - Pipeline configuration builder
        """

        return self.state


__all__ = [
    "PipelineSettings",
]