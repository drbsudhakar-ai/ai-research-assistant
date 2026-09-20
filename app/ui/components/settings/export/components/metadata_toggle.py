"""
Metadata Toggle Component

Reusable Streamlit component for controlling whether
analysis metadata is included in exported reports.

Responsibilities:
- Render metadata inclusion toggle
- Use export metadata definitions
- Return updated UI state

Does NOT contain:
- Metadata generation logic
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


def render_metadata_toggle(
    current_value: bool,
    key: str = "include_metadata",
) -> bool:
    """
    Render analysis metadata export toggle.

    Args:
        current_value:
            Current metadata inclusion state.

        key:
            Streamlit widget key.

    Returns:
        Updated toggle value.
    """

    metadata = ExportMetadata.INCLUDE_METADATA

    return st.toggle(
        label=metadata.label,
        value=current_value,
        key=key,
        help=metadata.help_text,
    )