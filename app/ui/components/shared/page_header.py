"""
app/ui/components/shared/page_header.py

Production-ready reusable page header component.

Provides a consistent header across all application pages.

Features
--------
- Page icon
- Title
- Subtitle
- Optional status badge
- Optional breadcrumb
- Optional action area
- Optional divider
- Responsive Streamlit layout

Author:
    AI Research Assistant

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import streamlit as st


# ============================================================================
# Models
# ============================================================================


@dataclass(slots=True)
class PageHeaderConfig:
    """
    Configuration for a page header.
    """

    title: str

    subtitle: str = ""

    icon: str = ""

    badge: str | None = None

    breadcrumb: str | None = None

    show_divider: bool = True


# ============================================================================
# Public API
# ============================================================================


def render_page_header(
    config: PageHeaderConfig,
    action_renderer: Callable[[], None] | None = None,
) -> None:
    """
    Render a reusable page header.

    Parameters
    ----------
    config:
        Header configuration.

    action_renderer:
        Optional callback that renders action widgets
        on the right side of the header.

    Example
    -------
    render_page_header(
        PageHeaderConfig(
            icon="📄",
            title="Analyze Paper",
            subtitle="Upload a research paper for AI-powered analysis.",
        )
    )
    """

    if config.breadcrumb:
        st.caption(config.breadcrumb)

    left_col, right_col = st.columns(
        [5, 1],
        vertical_alignment="center",
    )

    with left_col:

        title = (
            f"{config.icon} {config.title}"
            if config.icon
            else config.title
        )

        st.title(title)

        if config.subtitle:
            st.caption(config.subtitle)

    with right_col:

        if config.badge:
            st.badge(config.badge)

        if action_renderer is not None:
            action_renderer()

    if config.show_divider:
        st.divider()


# ============================================================================
# Convenience Helpers
# ============================================================================


def render_simple_header(
    title: str,
    *,
    icon: str = "",
    subtitle: str = "",
) -> None:
    """
    Render a simple page header.

    Parameters
    ----------
    title:
        Page title.

    icon:
        Optional icon.

    subtitle:
        Optional subtitle.
    """

    render_page_header(
        PageHeaderConfig(
            title=title,
            subtitle=subtitle,
            icon=icon,
        )
    )


# ============================================================================
# Module Exports
# ============================================================================


__all__ = [
    "PageHeaderConfig",
    "render_page_header",
    "render_simple_header",
]