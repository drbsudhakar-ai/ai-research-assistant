"""
AI Research Assistant
General Settings - Storage Section

Responsible for rendering storage-related preferences.

Includes:
    - Workspace directory
    - History storage mode
    - History database location
    - Cache behaviour
    - Temporary file cleanup

No business logic.
State is managed by GeneralSettingsState.

Version:
    1.0.0
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from ..enums import HistoryStorageMode

from ..metadata import (
    HISTORY_STORAGE_METADATA,
)

from ..state import GeneralSettingsState


class StorageSection:
    """
    Storage settings UI renderer.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
    ) -> None:
        """
        Initialize storage section.

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
        Render storage settings section.
        """

        st.subheader(
            "💾 Storage"
        )

        st.caption(
            "Configure workspace, history storage, and local data behaviour."
        )


        self._render_workspace()

        st.divider()

        self._render_history_storage()

        st.divider()

        self._render_cache_settings()

        st.divider()

        self._render_cleanup_settings()


    # ========================================================
    # Workspace
    # ========================================================

    def _render_workspace(self) -> None:
        """
        Render workspace path configuration.
        """

        st.markdown(
            "### Workspace Directory"
        )


        workspace = st.text_input(
            label="Workspace Path",
            value=str(
                self.state.workspace_path
            ),
            help=(
                "Root directory for application files."
            ),
        )


        workspace_path = Path(
            workspace
        )


        if (
            workspace_path
            != self.state.workspace_path
        ):

            self.state.update(
                "workspace_path",
                workspace_path,
            )


    # ========================================================
    # History Storage
    # ========================================================

    def _render_history_storage(self) -> None:
        """
        Render history storage options.
        """

        st.markdown(
            "### Analysis History Storage"
        )


        options = list(
            HistoryStorageMode
        )


        selected = st.radio(
            label="Storage Type",
            options=options,
            index=options.index(
                self.state.history_storage_mode
            ),
            format_func=lambda item: (
                HISTORY_STORAGE_METADATA[item].label
            ),
            horizontal=True,
            help=(
                "Select where analysis history is stored."
            ),
        )


        if (
            selected
            != self.state.history_storage_mode
        ):

            self.state.update(
                "history_storage_mode",
                selected,
            )


        metadata = HISTORY_STORAGE_METADATA[selected]

        st.info(
            f"{metadata.icon} {metadata.description}"
        )


        self._render_history_path()


    def _render_history_path(self) -> None:
        """
        Render database path input.
        """

        history_path = st.text_input(
            label="History Database Path",
            value=str(
                self.state.history_path
            ),
            help=(
                "SQLite database location for analysis history."
            ),
        )


        path = Path(
            history_path
        )


        if (
            path
            != self.state.history_path
        ):

            self.state.update(
                "history_path",
                path,
            )


    # ========================================================
    # Cache
    # ========================================================

    def _render_cache_settings(self) -> None:
        """
        Render caching preferences.
        """

        st.markdown(
            "### Performance"
        )


        cache_enabled = st.toggle(
            "Enable Application Cache",
            value=self.state.cache_enabled,
            help=(
                "Improves performance by reusing processed data."
            ),
        )


        if (
            cache_enabled
            != self.state.cache_enabled
        ):

            self.state.update(
                "cache_enabled",
                cache_enabled,
            )


    # ========================================================
    # Cleanup
    # ========================================================

    def _render_cleanup_settings(self) -> None:
        """
        Render temporary file cleanup option.
        """

        st.markdown(
            "### Cleanup"
        )


        cleanup = st.toggle(
            "Remove Temporary Files on Exit",
            value=self.state.clear_temp_files_on_exit,
            help=(
                "Deletes temporary processing files when application closes."
            ),
        )


        if (
            cleanup
            != self.state.clear_temp_files_on_exit
        ):

            self.state.update(
                "clear_temp_files_on_exit",
                cleanup,
            )


__all__ = [
    "StorageSection",
]