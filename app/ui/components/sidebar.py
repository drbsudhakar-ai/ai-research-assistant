"""
===============================================================================
Project      : AI Research Assistant
File         : sidebar.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Sidebar component for the AI Research Assistant.

Responsibilities:
    - Render application branding
    - Render navigation
    - Render sidebar footer
    - Return the selected page

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import streamlit as st
from app.ui.html_renderer import render_sidebar_html

from app.config.branding import get_brand_config
from app.config.app_config import (
    APP_NAME,
    APP_VERSION,
)
from app.config.navigation_config import NAVIGATION_ITEMS

from app.config.ui_config import (
    SHOW_APP_VERSION,
    SHOW_AUTHOR,
    SIDEBAR_TITLE,
)
from app.core.session import (
    get_session_value,
    set_session_value,
)

from app.config.app_config import APP_ICON

# =============================================================================
# Private Components
# =============================================================================

def _render_branding() -> None:
    """Render the application branding."""

    version = f'<span class="ara-side-version">Version {APP_VERSION}</span>' if SHOW_APP_VERSION else ""
    render_sidebar_html(
        f"""
        <div class="ara-side-brand">
          <div class="ara-side-mark">{APP_ICON}</div>
          <div class="ara-side-name">{APP_NAME}</div>
          <div class="ara-side-subtitle">Research-paper intelligence for academic users.</div>
          {version}
        </div>
        """
    )

def _render_navigation() -> str:
    """
    Render the navigation menu.

    Returns
    -------
    str
        Selected page key.
    """

    current_page = get_session_value("current_page")

    current_index = next(
        (
            index
            for index, item in enumerate(NAVIGATION_ITEMS)
            if item.key == current_page
        ),
        0,
    )

    selected_item = st.radio(
        label=SIDEBAR_TITLE,
        options=NAVIGATION_ITEMS,
        index=current_index,
        format_func=lambda item: item.display_name,
    )

    set_session_value(
        "current_page",
        selected_item.key,
    )

    return selected_item.key


def _render_footer() -> None:
    """Render sidebar footer."""

    st.divider()

    if SHOW_AUTHOR:
        st.caption(get_brand_config().credit)


# =============================================================================
# Public Components
# =============================================================================
def render_sidebar() -> str:
    """
    Render the application sidebar.

    Returns
    -------
    str
        Selected page.
    """

    with st.sidebar:

        _render_branding()

        page = _render_navigation()

        _render_footer()

    return page
