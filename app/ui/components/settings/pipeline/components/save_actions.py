"""
AI Research Assistant
Pipeline Settings - Save Actions Component

Reusable action bar for Pipeline Settings.

Responsibilities:
    - Save configuration
    - Reset configuration
    - Display validation status
    - Show unsaved changes indicator

No persistence logic.
No Streamlit page routing.

Persistence is handled by the Settings Manager layer.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st


class SaveActions:
    """
    Pipeline settings save/reset action component.
    """


    def __init__(
        self,
        state,
        on_save=None,
        on_reset=None,
        key: str = "pipeline_settings_actions",
    ) -> None:
        """
        Initialize save actions.

        Args:
            state:
                PipelineSettingsState instance.

            on_save:
                Callback executed on save.

            on_reset:
                Callback executed on reset.

            key:
                Streamlit widget key prefix.
        """

        self.state = state

        self.on_save = on_save

        self.on_reset = on_reset

        self.key = key


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render action buttons.
        """

        st.divider()

        self._render_status()

        col1, col2 = st.columns(
            2
        )


        with col1:

            if st.button(
                "💾 Save Changes",
                use_container_width=True,
                key=f"{self.key}_save",
            ):

                self._save()


        with col2:

            if st.button(
                "↩️ Reset Defaults",
                use_container_width=True,
                key=f"{self.key}_reset",
            ):

                self._reset()


    # ========================================================
    # Status
    # ========================================================

    def _render_status(self) -> None:
        """
        Display current settings state.
        """

        if self.state.is_dirty():

            st.warning(
                "⚠️ You have unsaved changes."
            )

        else:

            st.success(
                "✅ Settings are saved."
            )


    # ========================================================
    # Save
    # ========================================================

    def _save(self) -> None:
        """
        Execute save workflow.
        """

        valid, errors = (
            self.state.validate()
        )


        if not valid:

            st.error(
                "❌ Validation failed."
            )

            for error in errors:

                st.write(
                    f"- {error}"
                )

            return


        if self.on_save:

            self.on_save(
                self.state
            )

        else:

            self.state.mark_saved()


        st.success(
            "Pipeline settings saved."
        )


    # ========================================================
    # Reset
    # ========================================================

    def _reset(self) -> None:
        """
        Restore defaults.
        """

        self.state.reset()


        if self.on_reset:

            self.on_reset(
                self.state
            )


        st.info(
            "Pipeline settings restored to defaults."
        )


__all__ = [
    "SaveActions",
]