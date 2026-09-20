"""
Export Format Selector Component

Reusable Streamlit UI component for selecting
the report export format.

Responsibilities:
- Render export format selector
- Convert UI selection into ExportFormat enum
- Provide consistent settings UI behavior

Does NOT contain:
- Export generation logic
- File handling
- Persistence
- Validation rules

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from app.ui.components.settings.export.enums import (
    ExportFormat,
)
from app.ui.components.settings.export.metadata import (
    ExportMetadata,
)


# ---------------------------------------------------------------------------
# Component
# ---------------------------------------------------------------------------


def render_export_format_selector(
    current_value: ExportFormat,
    key: str = "export_format",
) -> ExportFormat:
    """
    Render export format selection component.

    Args:
        current_value:
            Currently selected export format.

        key:
            Streamlit widget key.

    Returns:
        Selected ExportFormat.
    """

    metadata = ExportMetadata.FORMAT

    options = list(ExportFormat)

    selected_index = (
        options.index(current_value)
        if current_value in options
        else 0
    )

    selected = st.selectbox(
        label=metadata.label,
        options=options,
        index=selected_index,
        key=key,
        format_func=_format_label,
        help=metadata.help_text,
    )

    return selected


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _format_label(
    export_format: ExportFormat,
) -> str:
    """
    Convert enum value into user-friendly label.

    Example:
        ExportFormat.PDF
        ->
        PDF Document

    Args:
        export_format:
            Export format enum.

    Returns:
        Display label.
    """

    labels = {
        ExportFormat.PDF: "PDF Document",
        ExportFormat.MARKDOWN: "Markdown",
        ExportFormat.DOCX: "Word Document",
        ExportFormat.HTML: "HTML Web Report",
    }

    return labels.get(
        export_format,
        export_format.value,
    )