"""
AI Research Assistant
General Settings - Language Selector Component

Reusable UI component for selecting application language.

Responsibilities:
    - Render language selection widget
    - Display language metadata
    - Update GeneralSettingsState

No business logic.
No validation logic.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import ApplicationLanguage
from ..metadata import LANGUAGE_METADATA
from ..state import GeneralSettingsState


class LanguageSelector:
    """
    Application language selection component.
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
        Render language selector.
        """

        st.markdown(
            "### Application Language"
        )


        options = list(
            ApplicationLanguage
        )


        selected = st.selectbox(
            label="Language",
            options=options,
            index=options.index(
                self.state.language
            ),
            format_func=self._format_language,
            help=(
                "Select application display language."
            ),
        )


        if (
            selected
            != self.state.language
        ):

            self.state.update(
                "language",
                selected,
            )


        self._render_description(
            selected
        )


    # ========================================================
    # Formatting
    # ========================================================

    @staticmethod
    def _format_language(
        language: ApplicationLanguage,
    ) -> str:
        """
        Convert language enum into UI label.
        """

        metadata = LANGUAGE_METADATA[language]

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    # ========================================================
    # Information
    # ========================================================

    @staticmethod
    def _render_description(
        language: ApplicationLanguage,
    ) -> None:
        """
        Display language information.
        """

        metadata = LANGUAGE_METADATA[language]

        st.caption(
            metadata.description
        )


__all__ = [
    "LanguageSelector",
]