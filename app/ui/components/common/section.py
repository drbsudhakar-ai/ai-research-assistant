"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Components
File         : section.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable section header component.

Responsibilities:
    - Display section title.
    - Display subtitle.
    - Display optional icon.
    - Display optional divider.

Non-Responsibilities:
    - Render business content.
    - Navigation.
    - Theme initialization.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from app.ui.base.component import UIComponent


@dataclass(slots=True)
class Section(UIComponent):
    """
    Reusable section header.
    """

    title: str

    subtitle: str | None = None

    icon: str | None = None

    divider: bool = True

    def render(self) -> None:
        """
        Render the section.
        """

        if self.divider:
            st.divider()

        title = self.title

        if self.icon:
            title = f"{self.icon} {title}"

        st.subheader(title)

        if self.subtitle:
            st.caption(self.subtitle)