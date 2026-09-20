"""
AI Research Assistant
General Settings - Theme Selector Component

Reusable UI component for selecting application theme.

Responsibilities:
    - Render theme selection widget
    - Display theme metadata
    - Update GeneralSettingsState

No business logic.
No validation logic.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import ThemeMode
from ..metadata import THEME_METADATA
from ..state import GeneralSettingsState


class ThemeSelector:
    """
    Theme selection UI component.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
    ) -> None:
        """
        Initialize component.

        Args:
            state:
                General settings state object.
        """

        self.state = state


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render theme selector.
        """

        st.markdown(
            "### Application Theme"
        )


        options = list(
            ThemeMode
        )


        selected = st.selectbox(
            label="Theme Mode",
            options=options,
            index=options.index(
                self.state.theme_mode
            ),
            format_func=self._format_theme,
            help=(
                "Select application appearance mode."
            ),
        )


        if (
            selected
            != self.state.theme_mode
        ):

            self.state.update(
                "theme_mode",
                selected,
            )


        self._render_description(
            selected
        )


    # ========================================================
    # Helpers
    # ========================================================

    @staticmethod
    def _format_theme(
        theme: ThemeMode,
    ) -> str:
        """
        Convert enum value to display label.
        """

        metadata = THEME_METADATA[theme]

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _render_description(
        theme: ThemeMode,
    ) -> None:
        """
        Display theme information.
        """

        metadata = THEME_METADATA[theme]

        st.caption(
            metadata.description
        )


__all__ = [
    "ThemeSelector",
]