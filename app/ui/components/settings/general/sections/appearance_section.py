"""
File: app/ui/components/settings/general/sections/appearance_section.py
AI Research Assistant
General Settings - Appearance Section

Responsible for rendering appearance-related settings.

Includes:
    - Theme selection
    - UI density
    - Tooltips
    - Animations
    - Advanced UI options

No business logic.
State is managed by GeneralSettingsState.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import ThemeMode, UIDensity
from ..metadata import (
    THEME_METADATA,
    UI_DENSITY_METADATA,
)
from ..state import GeneralSettingsState


class AppearanceSection:
    """
    Appearance settings UI renderer.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
    ) -> None:
        """
        Initialize appearance section.

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
        Render appearance settings section.
        """

        st.subheader(
            "🎨 Appearance"
        )

        st.caption(
            "Customize application look and user interface behaviour."
        )


        self._render_theme()

        st.divider()

        self._render_density()

        st.divider()

        self._render_ui_preferences()


    # ========================================================
    # Theme
    # ========================================================

    def _render_theme(self) -> None:
        """
        Render theme selector.
        """

        st.markdown(
            "### Theme"
        )

        options = list(
            ThemeMode
        )

        selected = st.selectbox(
            label="Application Theme",
            options=options,
            index=options.index(
                self.state.theme_mode
            ),
            format_func=lambda item: (
                THEME_METADATA[item].label
            ),
            help=(
                "Choose application appearance mode."
            ),
        )


        if selected != self.state.theme_mode:

            self.state.update(
                "theme_mode",
                selected,
            )


        metadata = THEME_METADATA[selected]

        st.info(
            f"{metadata.icon} {metadata.description}"
        )


    # ========================================================
    # UI Density
    # ========================================================

    def _render_density(self) -> None:
        """
        Render UI density selector.
        """

        st.markdown(
            "### Interface Density"
        )

        options = list(
            UIDensity
        )

        selected = st.radio(
            label="Layout Density",
            options=options,
            index=options.index(
                self.state.ui_density
            ),
            format_func=lambda item: (
                UI_DENSITY_METADATA[item].label
            ),
            horizontal=True,
            help=(
                "Controls spacing between UI elements."
            ),
        )


        if selected != self.state.ui_density:

            self.state.update(
                "ui_density",
                selected,
            )


        metadata = UI_DENSITY_METADATA[selected]

        st.caption(
            f"{metadata.icon} {metadata.description}"
        )


    # ========================================================
    # UI Preferences
    # ========================================================

    def _render_ui_preferences(self) -> None:
        """
        Render additional UI options.
        """

        st.markdown(
            "### Interface Preferences"
        )


        show_tooltips = st.toggle(
            "Show Helpful Tooltips",
            value=self.state.show_tooltips,
            help=(
                "Display contextual help information."
            ),
        )

        if (
            show_tooltips
            != self.state.show_tooltips
        ):

            self.state.update(
                "show_tooltips",
                show_tooltips,
            )


        enable_animation = st.toggle(
            "Enable UI Animations",
            value=self.state.enable_animations,
            help=(
                "Enable visual transition effects."
            ),
        )

        if (
            enable_animation
            != self.state.enable_animations
        ):

            self.state.update(
                "enable_animations",
                enable_animation,
            )


        advanced_options = st.toggle(
            "Show Advanced Options",
            value=self.state.show_advanced_options,
            help=(
                "Display advanced configuration controls."
            ),
        )


        if (
            advanced_options
            != self.state.show_advanced_options
        ):

            self.state.update(
                "show_advanced_options",
                advanced_options,
            )


__all__ = [
    "AppearanceSection",
]