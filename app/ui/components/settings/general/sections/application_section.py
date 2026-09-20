"""
AI Research Assistant
General Settings - Application Section

Responsible for rendering application-level preferences.

Includes:
    - Application name
    - Default startup page
    - Application language
    - Startup behaviour

No business logic.
State is managed by GeneralSettingsState.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import (
    ApplicationLanguage,
    StartupPage,
)

from ..metadata import (
    LANGUAGE_METADATA,
    STARTUP_PAGE_METADATA,
)

from ..state import GeneralSettingsState


class ApplicationSection:
    """
    Application settings UI renderer.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
    ) -> None:
        """
        Initialize application section.

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
        Render application settings section.
        """

        st.subheader(
            "⚙️ Application"
        )

        st.caption(
            "Configure application behaviour and startup preferences."
        )


        self._render_application_name()

        st.divider()

        self._render_language()

        st.divider()

        self._render_startup_page()

        st.divider()

        self._render_startup_behaviour()


    # ========================================================
    # Application Name
    # ========================================================

    def _render_application_name(self) -> None:
        """
        Render application name input.
        """

        st.markdown(
            "### Application Identity"
        )


        app_name = st.text_input(
            label="Application Name",
            value=self.state.app_name,
            help=(
                "Display name used by the application."
            ),
        )


        if app_name != self.state.app_name:

            self.state.update(
                "app_name",
                app_name,
            )


    # ========================================================
    # Language
    # ========================================================

    def _render_language(self) -> None:
        """
        Render language selector.
        """

        st.markdown(
            "### Language"
        )


        options = list(
            ApplicationLanguage
        )


        selected = st.selectbox(
            label="Application Language",
            options=options,
            index=options.index(
                self.state.language
            ),
            format_func=lambda item: (
                LANGUAGE_METADATA[item].label
            ),
            help=(
                "Select application display language."
            ),
        )


        if selected != self.state.language:

            self.state.update(
                "language",
                selected,
            )


        metadata = LANGUAGE_METADATA[selected]

        st.caption(
            f"{metadata.icon} {metadata.description}"
        )


    # ========================================================
    # Startup Page
    # ========================================================

    def _render_startup_page(self) -> None:
        """
        Render default startup page selector.
        """

        st.markdown(
            "### Startup Page"
        )


        options = list(
            StartupPage
        )


        selected = st.radio(
            label="Open application with",
            options=options,
            index=options.index(
                self.state.startup_page
            ),
            format_func=lambda item: (
                STARTUP_PAGE_METADATA[item].label
            ),
            horizontal=True,
            help=(
                "Select page shown after application starts."
            ),
        )


        if selected != self.state.startup_page:

            self.state.update(
                "startup_page",
                selected,
            )


        metadata = STARTUP_PAGE_METADATA[selected]

        st.info(
            f"{metadata.icon} {metadata.description}"
        )


    # ========================================================
    # Startup Behaviour
    # ========================================================

    def _render_startup_behaviour(self) -> None:
        """
        Render startup preferences.
        """

        st.markdown(
            "### Startup Behaviour"
        )


        remember_page = st.toggle(
            "Remember Last Opened Page",
            value=self.state.remember_last_page,
            help=(
                "Restore previous page when application restarts."
            ),
        )


        if (
            remember_page
            != self.state.remember_last_page
        ):

            self.state.update(
                "remember_last_page",
                remember_page,
            )


__all__ = [
    "ApplicationSection",
]