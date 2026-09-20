"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Layout Package
File         : app/ui/layout/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Public interface for the UI layout system.

    Provides reusable application shell components:
        - Page containers
        - Header
        - Sidebar
        - Footer
        - Navigation

Purpose:
    - Maintain consistent page structure.
    - Separate layout logic from page business logic.
    - Provide reusable UI building blocks.

Dependencies:
    Internal:
        - app.ui.layout.page_container
        - app.ui.layout.header
        - app.ui.layout.sidebar
        - app.ui.layout.footer
        - app.ui.layout.navigation

    External:
        - Python >= 3.11

Usage:
    from app.ui.layout import (
        render_page_container,
        render_header,
    )

===============================================================================
"""

from __future__ import annotations


# Layout container
from app.ui.layout.page_container import (
    PageContainer,
    render_page_container,
)


# Header
from app.ui.layout.header import (
    Header,
    render_header,
)


# Sidebar
from app.ui.layout.sidebar import (
    Sidebar,
    render_sidebar,
)


# Footer
from app.ui.layout.footer import (
    Footer,
    render_footer,
)


# Navigation
from app.ui.layout.navigation import (
    Navigation,
    render_navigation,
)


__all__ = [
    # Page container
    "PageContainer",
    "render_page_container",

    # Header
    "Header",
    "render_header",

    # Sidebar
    "Sidebar",
    "render_sidebar",

    # Footer
    "Footer",
    "render_footer",

    # Navigation
    "Navigation",
    "render_navigation",
]