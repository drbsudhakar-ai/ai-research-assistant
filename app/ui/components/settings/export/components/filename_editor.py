"""
Filename Editor Component

Reusable Streamlit component for configuring
export report filename patterns.

Responsibilities:
- Render filename pattern input
- Provide user guidance
- Return updated filename pattern

Does NOT contain:
- Filename generation logic
- File system operations
- Validation rules
- Persistence handling

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


def render_filename_editor(
    current_value: str,
    key: str = "file_naming_pattern",
) -> str:
    """
    Render export filename pattern editor.

    Args:
        current_value:
            Current filename pattern.

        key:
            Streamlit widget key.

    Returns:
        Updated filename pattern.
    """

    metadata = ExportMetadata.FILE_NAMING

    st.caption(
        "Available variables: "
        "{title}, {timestamp}"
    )

    return st.text_input(
        label=metadata.label,
        value=current_value,
        key=key,
        help=metadata.help_text,
        placeholder="{title}_{timestamp}",
    )