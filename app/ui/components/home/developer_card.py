"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/developer_card.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Developer profile card component for Home page.

Responsibilities:
    - Display project creator information.
    - Present professional background.
    - Support portfolio-oriented presentation.

Non-Responsibilities:
    - User authentication.
    - External profile fetching.
    - Business logic.

===============================================================================
"""

from __future__ import annotations

from app.config.branding import get_brand_config
from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Optional

import streamlit as st


@dataclass(frozen=True)
class DeveloperCard:
    """
    Represents developer information card.
    """

    name: str

    title: str

    description: str

    icon: str = "👨‍💻"

    link: Optional[str] = None

    def render(self) -> None:
        """
        Render developer card.
        """

        link_html = (
            f"""
            <a href="{self.link}" target="_blank">
                Profile
            </a>
            """
            if self.link
            else ""
        )

        render_html(f"""
            <div class="developer-card">

                <h3>
                    {self.icon} {self.name}
                </h3>

                <h4>
                    {self.title}
                </h4>

                <p>
                    {self.description}
                </p>

                {link_html}

            </div>
            """)


def render_developer_card(
    *,
    name: str | None = None,
    title: str | None = None,
    description: str | None = None,
    link: Optional[str] = None,
) -> None:
    """
    Render developer profile card.
    """

    brand = get_brand_config()
    DeveloperCard(
        name=name or brand.author,
        title=title or brand.credit,
        description=description or brand.tagline,
        link=link,
    ).render()


__all__ = [
    "DeveloperCard",
    "render_developer_card",
]