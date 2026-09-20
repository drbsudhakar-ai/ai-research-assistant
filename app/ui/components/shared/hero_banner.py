"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/shared/hero_banner.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable hero banner component for the AI Research Assistant UI.

    Provides:
        - Application branding area
        - Page introduction
        - Optional badge
        - Optional action buttons
        - Consistent theme integration

Dependencies:
        - Streamlit
        - UI Theme System

===============================================================================
"""


from __future__ import annotations

from app.ui.html_renderer import render_html

from dataclasses import dataclass
from typing import Callable, Optional


import streamlit as st



from app.ui.theme import (
    ThemeManager,
)



# =============================================================================
# Data Model
# =============================================================================


@dataclass(
    frozen=True,
)
class HeroAction:
    """
    Represents a hero section action button.

    Attributes:
        label:
            Button display text.

        callback:
            Function executed when clicked.
    """

    label: str

    callback: Callable[[], None]



# =============================================================================
# Hero Banner Component
# =============================================================================


class HeroBanner:
    """
    Professional hero banner renderer.

    Example:

        HeroBanner.render(
            title="AI Research Assistant",
            subtitle="Analyze research papers using AI",
            badge="Research Intelligence Engine",
        )

    """



    # -------------------------------------------------------------------------
    # Render Component
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        *,
        title: str,
        subtitle: str,
        badge: Optional[str] = None,
        actions: Optional[list[HeroAction]] = None,
    ) -> None:
        """
        Render hero banner.

        Args:
            title:
                Main heading.

            subtitle:
                Supporting description.

            badge:
                Optional label above title.

            actions:
                Optional action buttons.
        """

        ThemeManager.initialize()


        badge_html = ""


        if badge:

            badge_html = f"""
            <div class="badge badge-info">
                {badge}
            </div>
            """



        render_html(f"""
            <div class="hero">

                {badge_html}

                <div class="ara-page-kicker">Research Intelligence Workspace</div>

                <div class="hero-title">
                    {title}
                </div>

                <div class="hero-subtitle">
                    {subtitle}
                </div>

            </div>
            """)



        # ---------------------------------------------------------------------
        # Action Buttons
        # ---------------------------------------------------------------------

        if actions:


            columns = st.columns(
                len(actions)
            )


            for column, action in zip(
                columns,
                actions,
            ):

                with column:

                    if st.button(
                        action.label,
                        key=f"hero_{action.label}",
                    ):

                        action.callback()



    # -------------------------------------------------------------------------
    # Simple Renderer
    # -------------------------------------------------------------------------

    @staticmethod
    def simple(
        title: str,
        subtitle: str,
    ) -> None:
        """
        Render minimal hero banner.

        Args:
            title:
                Heading.

            subtitle:
                Description.
        """

        HeroBanner.render(

            title=title,

            subtitle=subtitle,

        )



    # -------------------------------------------------------------------------
    # Research Assistant Preset
    # -------------------------------------------------------------------------

    @staticmethod
    def research_assistant() -> None:
        """
        Default AI Research Assistant branding banner.
        """

        HeroBanner.render(

            title=
                "AI Research Assistant",

            subtitle=
                (
                    "Analyze research papers, "
                    "extract insights, and generate "
                    "structured scientific reports "
                    "using AI."
                ),

            badge=
                "Research Intelligence Engine",

        )
