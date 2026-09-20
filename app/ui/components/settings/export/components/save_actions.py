"""
Export Settings Save Actions Component

Reusable Streamlit component for export settings
action controls.

Responsibilities:
- Render Save / Reset buttons
- Provide user interaction events
- Return selected action

Does NOT contain:
- Settings persistence logic
- Export execution
- Validation rules
- Configuration mutation

Version:
    1.0.0
"""

from __future__ import annotations

from enum import Enum

import streamlit as st


# ---------------------------------------------------------------------------
# Action Enum
# ---------------------------------------------------------------------------


class ExportAction(str, Enum):
    """
    Available export settings actions.
    """

    SAVE = "save"
    RESET = "reset"


# ---------------------------------------------------------------------------
# Component
# ---------------------------------------------------------------------------


def render_save_actions(
    *,
    save_label: str = "Save Export Settings",
    reset_label: str = "Reset Defaults",
    key_prefix: str = "export_settings",
) -> ExportAction | None:
    """
    Render export settings action buttons.

    Args:
        save_label:
            Save button label.

        reset_label:
            Reset button label.

        key_prefix:
            Unique Streamlit key prefix.

    Returns:
        Selected ExportAction or None.
    """

    col1, col2 = st.columns(
        2,
        gap="medium",
    )

    with col1:
        save_clicked = st.button(
            save_label,
            key=f"{key_prefix}_save",
            type="primary",
            use_container_width=True,
        )

    with col2:
        reset_clicked = st.button(
            reset_label,
            key=f"{key_prefix}_reset",
            use_container_width=True,
        )

    if save_clicked:
        return ExportAction.SAVE

    if reset_clicked:
        return ExportAction.RESET

    return None