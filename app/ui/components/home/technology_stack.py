"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/technology_stack.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Technology stack showcase component.

Responsibilities:
    - Display technologies used by application.
    - Present architecture highlights.

Non-Responsibilities:
    - Dependency management.
    - Package installation.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Iterable

import streamlit as st


@dataclass(frozen=True)
class TechnologyStack:
    """
    Represents technology showcase.
    """

    technologies: Iterable[str]


    def render(self) -> None:
        """
        Render technology list.
        """

        items = " ".join(
            [
                f"`{technology}`"
                for technology in self.technologies
            ]
        )

        render_html(f"""
            <div class="technology-stack">

                <h3>
                    🛠 Technology Stack
                </h3>

                <p>
                    {items}
                </p>

            </div>
            """)


def render_technology_stack(
    technologies: Iterable[str],
) -> None:
    """
    Render technology stack.
    """

    TechnologyStack(
        technologies=technologies,
    ).render()


__all__ = [
    "TechnologyStack",
    "render_technology_stack",
]