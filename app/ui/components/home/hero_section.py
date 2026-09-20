"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/hero_section.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Hero section component for application landing page.

Responsibilities:
    - Display application introduction.
    - Present primary value proposition.
    - Provide professional landing experience.

Non-Responsibilities:
    - Navigation.
    - Authentication.
    - Business logic.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Optional

import streamlit as st


@dataclass(frozen=True)
class HeroSection:
    """
    Represents Home page hero banner.
    """

    title: str

    subtitle: str

    description: str

    icon: Optional[str] = "🤖"


    def render(self) -> None:
        """
        Render hero section.
        """

        render_html(f"""
            <div class="hero-section">

                <h1>
                    {self.icon} {self.title}
                </h1>

                <h3>
                    {self.subtitle}
                </h3>

                <p>
                    {self.description}
                </p>

            </div>
            """)


def render_hero_section(
    *,
    title: str = "AI Research Assistant",
    subtitle: str = "Research Intelligence Powered by Artificial Intelligence",
    description: str = (
        "Analyze research papers, extract insights, "
        "and generate academic-quality reports."
    ),
    icon: str = "🤖",
) -> None:
    """
    Render default hero section.
    """

    HeroSection(
        title=title,
        subtitle=subtitle,
        description=description,
        icon=icon,
    ).render()


__all__ = [
    "HeroSection",
    "render_hero_section",
]