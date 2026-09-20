"""
AI Research Assistant
General Settings - Toggle Card Component

Reusable UI component for boolean settings.

Responsibilities:
    - Render toggle controls consistently
    - Display title, description, and help text
    - Update GeneralSettingsState

No business logic.
No validation logic.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..state import GeneralSettingsState


class ToggleCard:
    """
    Reusable boolean setting card component.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
        setting_key: str,
        title: str,
        description: str = "",
        help_text: str = "",
        icon: str = "⚙️",
    ) -> None:
        """
        Initialize toggle card.

        Args:
            state:
                General settings state object.

            setting_key:
                Boolean state attribute name.

            title:
                Display title.

            description:
                Supporting text.

            help_text:
                Tooltip text.

            icon:
                Display icon.
        """

        self.state = state
        self.setting_key = setting_key
        self.title = title
        self.description = description
        self.help_text = help_text
        self.icon = icon


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render toggle card.
        """

        if not hasattr(
            self.state,
            self.setting_key,
        ):
            raise AttributeError(
                f"Unknown setting: {self.setting_key}"
            )


        current_value = getattr(
            self.state,
            self.setting_key,
        )


        with st.container():

            st.markdown(
                f"#### {self.icon} {self.title}"
            )


            if self.description:

                st.caption(
                    self.description
                )


            updated_value = st.toggle(
                label=self.title,
                value=current_value,
                help=self.help_text,
                key=(
                    f"toggle_{self.setting_key}"
                ),
            )


            if updated_value != current_value:

                self.state.update(
                    self.setting_key,
                    updated_value,
                )


__all__ = [
    "ToggleCard",
]