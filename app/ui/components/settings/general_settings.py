"""
app/ui/components/settings/general_settings.py

General Settings UI Component

Provides application-level general configuration controls
for the AI Research Assistant Streamlit interface.

Version:
    1.0.0

Author:
    Dr B Sudhakar

Description:
    - Application appearance settings
    - Default analysis preferences
    - UI behavior controls
    - General user preferences

This component is UI-only.
Actual persistence should be handled by:
    app/config/settings_manager.py
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPONENT_TITLE = "General Settings"


DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "Light",
    "auto_save_history": True,
    "show_preview": True,
    "enable_notifications": True,
    "default_analysis_depth": "Detailed",
}


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def _get_setting(
    key: str,
    default: Any,
) -> Any:
    """
    Retrieve setting value from Streamlit session state.

    Args:
        key:
            Setting key.

        default:
            Default value.

    Returns:
        Stored value or default.
    """

    return st.session_state.get(
        key,
        default,
    )


def _set_setting(
    key: str,
    value: Any,
) -> None:
    """
    Store setting value in Streamlit session state.

    Args:
        key:
            Setting key.

        value:
            Setting value.
    """

    st.session_state[key] = value


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_general_settings() -> Dict[str, Any]:
    """
    Render General Settings panel.

    Returns:
        Dictionary containing updated settings.
    """

    st.subheader(COMPONENT_TITLE)

    st.caption(
        "Configure general application preferences."
    )

    settings: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Appearance
    # ------------------------------------------------------------------

    st.markdown(
        "### Appearance"
    )

    theme = st.selectbox(
        label="Application Theme",
        options=[
            "Light",
            "Dark",
            "System Default",
        ],
        index=[
            "Light",
            "Dark",
            "System Default",
        ].index(
            _get_setting(
                "theme",
                DEFAULT_SETTINGS["theme"],
            )
        ),
    )

    settings["theme"] = theme

    _set_setting(
        "theme",
        theme,
    )

    # ------------------------------------------------------------------
    # Analysis Preferences
    # ------------------------------------------------------------------

    st.markdown(
        "### Analysis Preferences"
    )

    analysis_depth = st.selectbox(
        label="Default Analysis Depth",
        options=[
            "Quick",
            "Standard",
            "Detailed",
            "Research Grade",
        ],
        index=[
            "Quick",
            "Standard",
            "Detailed",
            "Research Grade",
        ].index(
            _get_setting(
                "default_analysis_depth",
                DEFAULT_SETTINGS["default_analysis_depth"],
            )
        ),
    )

    settings[
        "default_analysis_depth"
    ] = analysis_depth

    _set_setting(
        "default_analysis_depth",
        analysis_depth,
    )

    # ------------------------------------------------------------------
    # UI Behaviour
    # ------------------------------------------------------------------

    st.markdown(
        "### Interface Behaviour"
    )

    auto_save_history = st.checkbox(
        label="Automatically save analysis history",
        value=_get_setting(
            "auto_save_history",
            DEFAULT_SETTINGS["auto_save_history"],
        ),
    )

    show_preview = st.checkbox(
        label="Show extracted paper preview",
        value=_get_setting(
            "show_preview",
            DEFAULT_SETTINGS["show_preview"],
        ),
    )

    enable_notifications = st.checkbox(
        label="Enable application notifications",
        value=_get_setting(
            "enable_notifications",
            DEFAULT_SETTINGS["enable_notifications"],
        ),
    )

    settings.update(
        {
            "auto_save_history": auto_save_history,
            "show_preview": show_preview,
            "enable_notifications": enable_notifications,
        }
    )

    _set_setting(
        "auto_save_history",
        auto_save_history,
    )

    _set_setting(
        "show_preview",
        show_preview,
    )

    _set_setting(
        "enable_notifications",
        enable_notifications,
    )

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    st.divider()

    if st.button(
        "Reset General Settings",
        type="secondary",
    ):
        for key, value in DEFAULT_SETTINGS.items():
            _set_setting(
                key,
                value,
            )

        st.success(
            "General settings restored to defaults."
        )

        st.rerun()

    return settings


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    "render_general_settings",
]