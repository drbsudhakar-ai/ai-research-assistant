"""
===============================================================================
Project      : AI Research Assistant
File         : navigation.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Application page routing.

Responsibilities:
    - Map page keys to page rendering functions.
    - Render the selected page.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

from app.config.navigation_config import PageKey
from app.ui.pages.about import show_about_page
from app.ui.pages.analyze import show_analyze_page
from app.ui.pages.history import show_history_page
from app.ui.pages.settings import show_settings_page
from app.ui.pages.dashboard import show_dashboard_page

__all__ = [
    "render_page",
]


# =============================================================================
# Page Routes
# =============================================================================

PAGE_ROUTES = {
    PageKey.DASHBOARD: show_dashboard_page,
    PageKey.ANALYZE: show_analyze_page,
    PageKey.HISTORY: show_history_page,
    PageKey.SETTINGS: show_settings_page,
    PageKey.ABOUT: show_about_page,
}




# =============================================================================
# Public API
# =============================================================================

def render_page(page_key: str) -> None:
    """
    Render the selected application page.

    Parameters
    ----------
    page_key : str
        Unique page identifier.
    """

    page = PAGE_ROUTES.get(
        page_key,
        show_dashboard_page,
    )

    page()