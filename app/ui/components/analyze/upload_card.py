"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/analyze/upload_card.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Research paper upload card component.

Responsibilities:
    - Render PDF upload interface.
    - Provide consistent upload experience.

Non-Responsibilities:
    - PDF validation.
    - File processing.
    - Analysis execution.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


@dataclass(frozen=True)
class UploadCard:
    """
    PDF upload component.
    """

    label: str = "Upload Research Paper (PDF)"

    help_text: Optional[str] = (
        "Upload a research paper for AI-powered analysis."
    )


    def render(self):
        """
        Render uploader.
        """

        return st.file_uploader(
            label=self.label,
            type=["pdf"],
            help=self.help_text,
        )


def render_upload_card(
    *,
    label: str = "Upload Research Paper (PDF)",
):
    """
    Render upload card.
    """

    return UploadCard(
        label=label,
    ).render()


__all__ = [
    "UploadCard",
    "render_upload_card",
]