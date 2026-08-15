"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Layout System
File         : app/ui/layout/sidebar.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Application sidebar component.

    Responsibilities:
        - Render sidebar branding.
        - Provide navigation container.
        - Display application information.
        - Provide future extension points for:
            * Authentication
            * User profile
            * Settings
            * Theme switching

    Non-Responsibilities:
        - Page routing logic.
        - Authentication implementation.
        - Business operations.

Dependencies:
    Internal:
        - app.ui.theme

    External:
        - streamlit
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.layout.sidebar import render_sidebar

    render_sidebar()

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

import streamlit as st

from app.config.branding import get_brand_config
from app.ui.html_renderer import render_html


@dataclass(frozen=True)
class Sidebar:
    """
    Sidebar configuration.

    Defaults come from BrandConfig. Do not hard-code product identity here.
    """

    title: str = field(default_factory=lambda: get_brand_config().application_name)
    description: str = field(default_factory=lambda: get_brand_config().tagline)
    icon: str = field(default_factory=lambda: get_brand_config().icon)
    version: str = field(default_factory=lambda: get_brand_config().version_label)


def render_sidebar(
    config: Sidebar | None = None,
) -> None:
    """
    Render application sidebar.

    Args:
        config:
            Optional sidebar configuration.
    """

    if config is None:
        brand = get_brand_config()
        config = Sidebar(
            title=brand.application_name,
            description=brand.tagline,
            icon=brand.icon,
            version=brand.version_label,
        )

    with st.sidebar:

        render_html(f"""
            <div class="ara-sidebar-brand">

                <div class="ara-sidebar-icon">
                    {config.icon}
                </div>


                <h2 class="ara-sidebar-title">
                    {config.title}
                </h2>


                <p class="ara-sidebar-description">
                    {config.description}
                </p>


                <small class="ara-sidebar-version">
                    {config.version}
                </small>

            </div>
            """)

        st.divider()

        render_html("""
            <div class="ara-sidebar-section-title">
                Navigation
            </div>
            """)


def render_sidebar_footer(
    text: str | None = None,
) -> None:
    """
    Render sidebar footer.
    """

    brand = get_brand_config()
    message = text or brand.credit

    with st.sidebar:

        render_html(f"""
            <div class="ara-sidebar-footer">

                {message}

            </div>
            """)


__all__: Final = [
    "Sidebar",
    "render_sidebar",
    "render_sidebar_footer",
]
