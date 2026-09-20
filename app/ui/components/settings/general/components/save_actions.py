"""
AI Research Assistant
General Settings - Save Actions Component

Reusable action bar for settings modules.

Responsibilities:
    - Validate settings
    - Save current state
    - Reset settings
    - Display validation feedback

No persistence logic.
No file/database operations.

Version:
    1.0.0
"""

from __future__ import annotations

from typing import Callable

import streamlit as st

from ..state import GeneralSettingsState


class SaveActions:
    """
    Settings save/reset action component.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
        on_save: Callable[
            [GeneralSettingsState],
            None,
        ] | None = None,
    ) -> None:
        """
        Initialize save actions.

        Args:
            state:
                General settings state object.

            on_save:
                Optional callback executed after validation.
        """

        self.state = state
        self.on_save = on_save


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render action buttons.
        """

        st.divider()

        col1, col2, col3 = st.columns(
            3
        )


        with col1:

            self._render_save_button()


        with col2:

            self._render_reset_button()


        with col3:

            self._render_status()


    # ========================================================
    # Save
    # ========================================================

    def _render_save_button(self) -> None:
        """
        Render save button.
        """

        if st.button(
            "💾 Save Settings",
            use_container_width=True,
        ):

            valid, errors = (
                self.state.validate()
            )


            if not valid:

                for error in errors:

                    st.error(
                        error
                    )

                return


            if self.on_save:

                self.on_save(
                    self.state
                )


            self.state.mark_saved()


            st.success(
                "Settings saved successfully."
            )


    # ========================================================
    # Reset
    # ========================================================

    def _render_reset_button(self) -> None:
        """
        Render reset button.
        """

        if st.button(
            "↩️ Reset Defaults",
            use_container_width=True,
        ):

            self.state.reset()

            st.info(
                "Settings restored to defaults."
            )


    # ========================================================
    # Status
    # ========================================================

    def _render_status(self) -> None:
        """
        Display state status.
        """

        if self.state.is_dirty():

            st.warning(
                "Unsaved changes"
            )

        else:

            st.success(
                "All changes saved"
            )


__all__ = [
    "SaveActions",
]