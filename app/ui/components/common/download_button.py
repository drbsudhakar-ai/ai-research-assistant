"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/download_button.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable download button component for Streamlit pages.

Responsibilities:
    - Provide consistent download button styling.
    - Support report export functionality.
    - Abstract Streamlit download button usage.

Non-Responsibilities:
    - Report generation.
    - File conversion.
    - Data formatting.
    - Storage management.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


@dataclass(frozen=True)
class DownloadButton:
    """
    Represents a reusable download button.

    Attributes:
        label:
            Button text.

        data:
            Content to download.

        file_name:
            Download file name.

        mime:
            MIME type.

        icon:
            Optional button icon.
    """

    label: str
    data: bytes | str

    file_name: str

    mime: str = "text/plain"

    icon: Optional[str] = None

    def render(self) -> None:
        """
        Render download button.
        """

        button_label = (
            f"{self.icon} {self.label}"
            if self.icon
            else self.label
        )

        st.download_button(
            label=button_label,
            data=self.data,
            file_name=self.file_name,
            mime=self.mime,
            use_container_width=True,
        )


def render_download_button(
    label: str,
    data: bytes | str,
    *,
    file_name: str,
    mime: str = "text/plain",
    icon: Optional[str] = None,
) -> None:
    """
    Functional helper for download button rendering.

    Examples:

        render_download_button(
            label="Download Markdown Report",
            data=markdown_content,
            file_name="analysis_report.md",
            mime="text/markdown",
            icon="⬇️"
        )
    """

    button = DownloadButton(
        label=label,
        data=data,
        file_name=file_name,
        mime=mime,
        icon=icon,
    )

    button.render()


__all__ = [
    "DownloadButton",
    "render_download_button",
]