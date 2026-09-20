"""
app/ui/components/settings/export_settings.py

Export Settings UI Component

Provides configuration controls for analysis report
export preferences in the AI Research Assistant application.

Version:
    1.0.0

Author:
    Dr B Sudhakar

Description:
    - Configure default export format
    - Configure report content options
    - Configure research report preferences
    - Manage export behaviour

This component handles only UI configuration.

Actual persistence should be handled by:

    app/config/settings_manager.py

Related configuration:

    app/config/export_config.py
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPONENT_TITLE = "Export Settings"


DEFAULT_EXPORT_SETTINGS: Dict[str, Any] = {
    "default_export_format": "PDF",
    "include_metadata": True,
    "include_analysis_summary": True,
    "include_research_sections": True,
    "include_citations": False,
    "include_raw_extracted_text": False,
}


EXPORT_FORMATS = [
    "PDF",
    "Markdown",
    "DOCX",
    "HTML",
]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def _get_setting(
    key: str,
    default: Any,
) -> Any:
    """
    Retrieve export setting from session state.

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
    Store export setting in session state.

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


def render_export_settings() -> Dict[str, Any]:
    """
    Render export configuration panel.

    Returns:
        Dictionary containing export settings.
    """

    st.subheader(
        COMPONENT_TITLE
    )

    st.caption(
        "Configure report generation and export preferences."
    )

    settings: Dict[str, Any] = {}


    # ------------------------------------------------------------------
    # Export Format
    # ------------------------------------------------------------------

    st.markdown(
        "### Default Export Format"
    )

    default_export_format = st.selectbox(
        label="Preferred Report Format",
        options=EXPORT_FORMATS,
        index=EXPORT_FORMATS.index(
            _get_setting(
                "default_export_format",
                DEFAULT_EXPORT_SETTINGS[
                    "default_export_format"
                ],
            )
        ),
    )


    settings[
        "default_export_format"
    ] = default_export_format


    _set_setting(
        "default_export_format",
        default_export_format,
    )


    # ------------------------------------------------------------------
    # Report Content
    # ------------------------------------------------------------------

    st.markdown(
        "### Report Content Options"
    )


    include_metadata = st.checkbox(
        label="Include paper metadata",
        value=bool(
            _get_setting(
                "include_metadata",
                DEFAULT_EXPORT_SETTINGS[
                    "include_metadata"
                ],
            )
        ),
    )


    include_analysis_summary = st.checkbox(
        label="Include AI analysis summary",
        value=bool(
            _get_setting(
                "include_analysis_summary",
                DEFAULT_EXPORT_SETTINGS[
                    "include_analysis_summary"
                ],
            )
        ),
    )


    include_research_sections = st.checkbox(
        label=(
            "Include research sections "
            "(gap, methodology, contribution, limitations)"
        ),
        value=bool(
            _get_setting(
                "include_research_sections",
                DEFAULT_EXPORT_SETTINGS[
                    "include_research_sections"
                ],
            )
        ),
    )


    include_citations = st.checkbox(
        label="Include citation-ready references",
        value=bool(
            _get_setting(
                "include_citations",
                DEFAULT_EXPORT_SETTINGS[
                    "include_citations"
                ],
            )
        ),
    )


    include_raw_extracted_text = st.checkbox(
        label="Include extracted paper text",
        value=bool(
            _get_setting(
                "include_raw_extracted_text",
                DEFAULT_EXPORT_SETTINGS[
                    "include_raw_extracted_text"
                ],
            )
        ),
        help=(
            "Adds extracted PDF text to exported reports. "
            "May increase file size."
        ),
    )


    settings.update(
        {
            "include_metadata": include_metadata,
            "include_analysis_summary": include_analysis_summary,
            "include_research_sections": include_research_sections,
            "include_citations": include_citations,
            "include_raw_extracted_text": include_raw_extracted_text,
        }
    )


    _set_setting(
        "include_metadata",
        include_metadata,
    )

    _set_setting(
        "include_analysis_summary",
        include_analysis_summary,
    )

    _set_setting(
        "include_research_sections",
        include_research_sections,
    )

    _set_setting(
        "include_citations",
        include_citations,
    )

    _set_setting(
        "include_raw_extracted_text",
        include_raw_extracted_text,
    )


    # ------------------------------------------------------------------
    # Preview
    # ------------------------------------------------------------------

    st.markdown(
        "### Export Preview"
    )


    st.info(
        f"""
        **Format:** {default_export_format}

        **Metadata:** {"Included" if include_metadata else "Excluded"}

        **AI Summary:**
        {"Included" if include_analysis_summary else "Excluded"}

        **Research Sections:**
        {"Included" if include_research_sections else "Excluded"}

        **Citations:**
        {"Included" if include_citations else "Excluded"}
        """
    )


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    st.divider()

    if st.button(
        "Reset Export Settings",
        type="secondary",
    ):

        for key, value in DEFAULT_EXPORT_SETTINGS.items():

            _set_setting(
                key,
                value,
            )

        st.success(
            "Export settings restored to defaults."
        )

        st.rerun()


    return settings


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "render_export_settings",
]