"""
Export Settings Panel

Main orchestrator for Export Settings UI.

Responsibilities:
- Initialize export settings state
- Render export configuration components
- Validate user configuration
- Handle save/reset actions
- Provide user feedback

Does NOT contain:
- Export generation logic
- Report rendering
- File operations

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from app.ui.components.settings.export.components import (
    ExportAction,
    render_citation_toggle,
    render_export_format_selector,
    render_filename_editor,
    render_save_actions,
    render_summary_toggle,
)
from app.ui.components.settings.export.defaults import (
    DefaultExportSettings,
)
from app.ui.components.settings.export.validators import (
    validate_export_settings,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXPORT_SETTINGS_STATE_KEY = (
    "export_settings"
)


# ---------------------------------------------------------------------------
# State Management
# ---------------------------------------------------------------------------


def _initialize_export_settings() -> None:
    """
    Initialize export settings in Streamlit session state.

    Uses defaults when no existing state exists.
    """

    if EXPORT_SETTINGS_STATE_KEY not in st.session_state:

        st.session_state[
            EXPORT_SETTINGS_STATE_KEY
        ] = (
            DefaultExportSettings
            .as_dict()
        )


def _get_settings() -> dict:
    """
    Retrieve current export settings.

    Returns:
        Export settings dictionary.
    """

    return st.session_state[
        EXPORT_SETTINGS_STATE_KEY
    ]


def _update_settings(
    key: str,
    value: object,
) -> None:
    """
    Update export setting value.

    Args:
        key:
            Setting key.

        value:
            Updated value.
    """

    settings = _get_settings()

    settings[key] = value


# ---------------------------------------------------------------------------
# Main Renderer
# ---------------------------------------------------------------------------


def render_export_settings() -> None:
    """
    Render Export Settings UI.

    This is the entry point called by
    the Settings page.
    """

    _initialize_export_settings()

    settings = _get_settings()

    st.subheader(
        "Export Settings"
    )

    st.caption(
        "Configure report export format, "
        "content options, and naming preferences."
    )


    # -------------------------------------------------
    # Export Format
    # -------------------------------------------------

    selected_format = (
        render_export_format_selector(
            current_value=settings[
                "export_format"
            ],
        )
    )

    _update_settings(
        "export_format",
        selected_format,
    )


    st.divider()


    # -------------------------------------------------
    # Export Options
    # -------------------------------------------------

    include_summary = (
        render_summary_toggle(
            current_value=settings[
                "include_summary"
            ],
        )
    )

    _update_settings(
        "include_summary",
        include_summary,
    )


    include_citations = (
        render_citation_toggle(
            current_value=settings[
                "include_citations"
            ],
        )
    )

    _update_settings(
        "include_citations",
        include_citations,
    )

    from app.ui.components.settings.export.components import (
        render_metadata_toggle,
    )
    include_metadata = render_metadata_toggle(
        current_value=settings["include_metadata"]
    )


    # include_metadata = st.toggle(
    #     "Include Analysis Metadata",
    #     value=settings[
    #         "include_metadata"
    #     ],
    #     key="include_metadata_toggle",
    #     help=(
    #         "Include model, execution time, "
    #         "and analysis details."
    #     ),
    # )

    _update_settings(
        "include_metadata",
        include_metadata,
    )


    st.divider()


    # -------------------------------------------------
    # Filename Configuration
    # -------------------------------------------------

    filename_pattern = (
        render_filename_editor(
            current_value=settings[
                "file_naming_pattern"
            ],
        )
    )

    _update_settings(
        "file_naming_pattern",
        filename_pattern,
    )


    st.divider()


    # -------------------------------------------------
    # Actions
    # -------------------------------------------------

    action = render_save_actions()


    if action == ExportAction.SAVE:

        _save_export_settings()


    elif action == ExportAction.RESET:

        _reset_export_settings()



# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def _save_export_settings() -> None:
    """
    Validate and save export settings.

    Persistence integration will be connected
    with SettingsManager.
    """

    settings = _get_settings()

    is_valid, errors = (
        validate_export_settings(
            settings
        )
    )

    if not is_valid:

        for error in errors:
            st.error(error)

        return


    # Future integration:
    #
    # SettingsManager.save(
    #     "export",
    #     settings
    # )

    st.success(
        "Export settings saved successfully."
    )


def _reset_export_settings() -> None:
    """
    Restore export settings defaults.
    """

    st.session_state[
        EXPORT_SETTINGS_STATE_KEY
    ] = (
        DefaultExportSettings
        .as_dict()
    )

    st.success(
        "Export settings restored to defaults."
    )

    st.rerun()