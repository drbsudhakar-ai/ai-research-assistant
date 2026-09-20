"""
Executive Summary Toggle Component

Reusable Streamlit component for controlling whether
an executive summary is included in exported reports.

Responsibilities:
- Render summary inclusion toggle
- Use export metadata for UI text
- Return updated UI state

Does NOT contain:
- Report generation logic
- Export processing
- Persistence handling
- Validation rules

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from app.ui.components.settings.export.metadata import (
    ExportMetadata,
)


# ---------------------------------------------------------------------------
# Component
# ---------------------------------------------------------------------------


def render_summary_toggle(
    current_value: bool,
    key: str = "include_summary",
) -> bool:
    """
    Render executive summary export toggle.

    Args:
        current_value:
            Current summary inclusion state.

        key:
            Streamlit widget key.

    Returns:
        Updated toggle value.
    """

    metadata = ExportMetadata.INCLUDE_SUMMARY

    return st.toggle(
        label=metadata.label,
        value=current_value,
        key=key,
        help=metadata.help_text,
    )