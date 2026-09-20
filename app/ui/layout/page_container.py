"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Layout System
File         : app/ui/layout/page_container.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable page container component for the Streamlit UI.

    Responsibilities:
        - Provide consistent page structure.
        - Render page title and subtitle.
        - Apply theme-based spacing.
        - Wrap page content sections.

    Non-Responsibilities:
        - Page-specific business logic.
        - Data loading.
        - Navigation handling.

Dependencies:
    Internal:
        - app.ui.theme
        - app.ui.theme.components
        - app.ui.theme.spacing
        - app.ui.theme.typography

    External:
        - streamlit
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.layout.page_container import (
        PageContainer,
        render_page_container,
    )

    with render_page_container(
        title="Analyze Research Paper",
        subtitle="AI-powered academic analysis",
    ):
        render_content()

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass
from typing import Final

from contextlib import contextmanager
from typing import Iterator, Optional


import streamlit as st


from app.ui.theme import (
    COLORS,
    COMPONENTS,
    SPACING,
    TYPOGRAPHY,
)


@dataclass(frozen=True)
class PageContainer:
    """
    Configuration for a page container.

    Attributes:
        title:
            Main page heading.

        subtitle:
            Supporting description below title.

        icon:
            Optional page icon.

        show_divider:
            Display separator after header.
    """

    title: str

    subtitle: Optional[str] = None

    icon: Optional[str] = None

    show_divider: bool = True


def render_page_header(
    config: PageContainer,
) -> None:
    """
    Render page title section.

    Args:
        config:
            Page container configuration.
    """

    title = config.title

    if config.icon:
        title = f"{config.icon} {title}"


    render_html(f"""
        <div class="ara-page-header">

            <h1>
                {title}
            </h1>

        </div>
        """)


    if config.subtitle:

        render_html(f"""
            <p class="ara-page-subtitle">
                {config.subtitle}
            </p>
            """)


    if config.show_divider:

        st.divider()


@contextmanager
def render_page_container(
    title: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    show_divider: bool = True,
) -> Iterator[None]:
    """
    Render a complete page container.

    Provides a context manager so pages can define content naturally.

    Example:

        with render_page_container(
            title="Dashboard",
            subtitle="Research intelligence overview",
        ):
            render_dashboard()

    Args:
        title:
            Page title.

        subtitle:
            Optional page description.

        icon:
            Optional emoji/icon.

        show_divider:
            Whether to show divider.

    Yields:
        None
    """

    config = PageContainer(
        title=title,
        subtitle=subtitle,
        icon=icon,
        show_divider=show_divider,
    )


    render_page_header(config)


    render_html(f"""
        <div class="ara-page-container">
        """)


    try:

        yield


    finally:

        render_html("""
            </div>
            """)


def render_section_title(
    title: str,
    description: Optional[str] = None,
) -> None:
    """
    Render subsection heading.

    Used inside pages for sections like:
        - Upload Paper
        - Analysis Result
        - Research Summary

    Args:
        title:
            Section title.

        description:
            Optional explanation.
    """

    render_html(f"""
        <h2 class="ara-section-title">
            {title}
        </h2>
        """)


    if description:

        st.caption(description)


__all__: Final = [
    "PageContainer",
    "render_page_container",
    "render_page_header",
    "render_section_title",
]