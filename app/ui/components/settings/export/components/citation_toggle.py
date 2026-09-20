"""
Citation Toggle Component

Reusable Streamlit component for controlling whether
citation information is included in exported reports.

Responsibilities:
- Render citation inclusion toggle
- Use export metadata for UI text
- Return updated UI state

Does NOT contain:
- Citation extraction logic
- Report generation logic
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


def render_citation_toggle(
    current_value: bool,
    key: str = "include_citations",
) -> bool:
    """
    Render citation information export toggle.

    Args:
        current_value:
            Current citation inclusion state.

        key:
            Streamlit widget key.

    Returns:
        Updated toggle value.
    """

    metadata = ExportMetadata.INCLUDE_CITATIONS

    return st.toggle(
        label=metadata.label,
        value=current_value,
        key=key,
        help=metadata.help_text,
    )