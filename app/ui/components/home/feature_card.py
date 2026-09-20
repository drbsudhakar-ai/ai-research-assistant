"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/feature_card.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Feature card component for Home page.

Responsibilities:
    - Highlight application capabilities.
    - Display feature descriptions.

Non-Responsibilities:
    - Feature execution.
    - Navigation handling.

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class FeatureCard:
    """
    Represents application feature.
    """

    title: str

    description: str

    icon: str = "✨"


    def render(self) -> None:
        """
        Render feature card.
        """

        render_html(f"""
            <div class="feature-card">

                <h3>
                    {self.icon} {self.title}
                </h3>

                <p>
                    {self.description}
                </p>

            </div>
            """)


def render_feature_card(
    title: str,
    description: str,
    *,
    icon: str = "✨",
) -> None:
    """
    Render feature card.
    """

    FeatureCard(
        title=title,
        description=description,
        icon=icon,
    ).render()


__all__ = [
    "FeatureCard",
    "render_feature_card",
]