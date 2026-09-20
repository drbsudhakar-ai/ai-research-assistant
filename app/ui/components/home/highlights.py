"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/highlights.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Project highlights component for Home page.

Responsibilities:
    - Display important application capabilities.
    - Present product strengths.

Non-Responsibilities:
    - Feature execution.
    - Application configuration.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Iterable

import streamlit as st


@dataclass(frozen=True)
class Highlight:
    """
    Represents a single project highlight.
    """

    title: str

    description: str

    icon: str = "✨"


@dataclass(frozen=True)
class Highlights:
    """
    Collection of project highlights.
    """

    items: Iterable[Highlight]


    def render(self) -> None:
        """
        Render highlight cards.
        """

        columns = st.columns(3)

        for index, item in enumerate(self.items):

            with columns[index % 3]:

                render_html(f"""
                    <div class="highlight-card">

                        <h4>
                            {item.icon} {item.title}
                        </h4>

                        <p>
                            {item.description}
                        </p>

                    </div>
                    """)


def render_highlights(
    items: Iterable[Highlight],
) -> None:
    """
    Render project highlights.
    """

    Highlights(
        items=items,
    ).render()


__all__ = [
    "Highlight",
    "Highlights",
    "render_highlights",
]