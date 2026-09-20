"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/divider.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable divider UI component for Streamlit pages.

Responsibilities:
    - Provide consistent visual separation between sections.
    - Support spacing customization.

Non-Responsibilities:
    - Page layout management.
    - Content rendering.
    - Business logic.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Divider:
    """
    Represents a visual divider.

    Attributes:
        spacing:
            Vertical spacing around divider.

        thickness:
            Divider line thickness.
    """

    spacing: int = 16
    thickness: int = 1

    def render(self) -> None:
        """
        Render divider.
        """

        render_html(f"""
            <div style="
                margin-top:{self.spacing}px;
                margin-bottom:{self.spacing}px;
                border-top:{self.thickness}px solid
                rgba(128,128,128,0.25);
            ">
            </div>
            """)


def render_divider(
    *,
    spacing: int = 16,
    thickness: int = 1,
) -> None:
    """
    Functional helper for divider rendering.
    """

    divider = Divider(
        spacing=spacing,
        thickness=thickness,
    )

    divider.render()


__all__ = [
    "Divider",
    "render_divider",
]