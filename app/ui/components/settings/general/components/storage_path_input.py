"""
AI Research Assistant
General Settings - Storage Path Input Component

Reusable UI component for selecting and editing filesystem paths.

Responsibilities:
    - Render path input widget
    - Handle workspace/history paths
    - Convert string input to Path objects
    - Update GeneralSettingsState

No business logic.
No validation logic.

Version:
    1.0.0
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import streamlit as st

from ..state import GeneralSettingsState


# ============================================================
# Supported Path Types
# ============================================================

PathType = Literal[
    "workspace",
    "history",
]


class StoragePathInput:
    """
    Reusable filesystem path input component.
    """


    def __init__(
        self,
        state: GeneralSettingsState,
        path_type: PathType,
    ) -> None:
        """
        Initialize component.

        Args:
            state:
                General settings state object.

            path_type:
                Type of path being edited.
        """

        self.state = state
        self.path_type = path_type


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render path input field.
        """

        label, key, help_text = (
            self._get_configuration()
        )


        current_path = getattr(
            self.state,
            key,
        )


        value = st.text_input(
            label=label,
            value=str(current_path),
            help=help_text,
        )


        new_path = Path(
            value
        )


        if new_path != current_path:

            self.state.update(
                key,
                new_path,
            )


        self._render_path_info(
            new_path
        )


    # ========================================================
    # Configuration
    # ========================================================

    def _get_configuration(
        self,
    ) -> tuple[str, str, str]:
        """
        Return configuration based on path type.
        """

        if self.path_type == "workspace":

            return (
                "Workspace Directory",
                "workspace_path",
                (
                    "Root directory used by "
                    "AI Research Assistant."
                ),
            )


        if self.path_type == "history":

            return (
                "History Database Path",
                "history_path",
                (
                    "SQLite database file "
                    "containing analysis history."
                ),
            )


        raise ValueError(
            f"Unsupported path type: {self.path_type}"
        )


    # ========================================================
    # Information Display
    # ========================================================

    @staticmethod
    def _render_path_info(
        path: Path,
    ) -> None:
        """
        Display path status information.
        """

        if path.exists():

            if path.is_dir():

                st.success(
                    "Directory exists."
                )

            else:

                st.success(
                    "Path exists."
                )

        else:

            st.warning(
                "Path does not exist yet."
            )


__all__ = [
    "StoragePathInput",
]