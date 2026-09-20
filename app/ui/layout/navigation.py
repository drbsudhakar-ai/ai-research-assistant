"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Layout System
File         : app/ui/layout/navigation.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Application navigation component.

    Responsibilities:
        - Define application navigation structure.
        - Render sidebar navigation menu.
        - Manage page selection state.
        - Provide route metadata.

    Non-Responsibilities:
        - Page business logic.
        - Authentication.
        - Page implementation.

Dependencies:
    Internal:
        - app.ui.theme

    External:
        - streamlit
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.layout.navigation import render_navigation

    selected_page = render_navigation()

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, List, Optional


import streamlit as st


from app.ui.html_renderer import render_sidebar_html


from app.ui.theme import (
    COLORS,
    SPACING,
    TYPOGRAPHY,
)


@dataclass(frozen=True)
class NavigationItem:
    """
    Navigation menu item definition.

    Attributes:
        name:
            Display name.

        icon:
            Menu icon.

        route:
            Internal route identifier.

        description:
            Short help text.
    """

    name: str

    icon: str

    route: str

    description: str = ""


@dataclass(frozen=True)
class Navigation:
    """
    Navigation configuration.

    Defines the application menu structure.
    """

    items: List[NavigationItem]


DEFAULT_NAVIGATION: Final = Navigation(
    items=[
        NavigationItem(
            name="Home",
            icon="🏠",
            route="home",
            description="Research assistant dashboard",
        ),

        NavigationItem(
            name="Analyze Paper",
            icon="📄",
            route="analyze",
            description="AI-powered paper analysis",
        ),

        NavigationItem(
            name="Analysis History",
            icon="📚",
            route="history",
            description="Previous research analyses",
        ),

        NavigationItem(
            name="Settings",
            icon="⚙️",
            route="settings",
            description="Application configuration",
        ),

        NavigationItem(
            name="About",
            icon="ℹ️",
            route="about",
            description="Project information",
        ),
    ]
)


def render_navigation(
    navigation: Navigation = DEFAULT_NAVIGATION,
    default_page: str = "home",
) -> str:
    """
    Render sidebar navigation.

    Args:
        navigation:
            Navigation configuration.

        default_page:
            Default selected route.

    Returns:
        str:
            Selected route identifier.
    """

    if "selected_page" not in st.session_state:

        st.session_state.selected_page = (
            default_page
        )


    render_sidebar_html("""
        <div class="ara-sidebar-navigation-title">
            Pages
        </div>
        """)


    selected_route = st.session_state.selected_page


    for item in navigation.items:

        is_selected = (
            selected_route == item.route
        )


        label = (
            f"{item.icon} {item.name}"
        )


        if st.sidebar.button(
            label,
            key=f"nav_{item.route}",
            use_container_width=True,
        ):

            st.session_state.selected_page = (
                item.route
            )

            selected_route = item.route


    return selected_route


def get_navigation_items(
    navigation: Navigation = DEFAULT_NAVIGATION,
) -> List[NavigationItem]:
    """
    Return available navigation items.

    Args:
        navigation:
            Navigation configuration.

    Returns:
        List[NavigationItem]:
            Navigation items.
    """

    return list(navigation.items)


def get_page_title(
    route: str,
    navigation: Navigation = DEFAULT_NAVIGATION,
) -> Optional[str]:
    """
    Get display title for a route.

    Args:
        route:
            Internal route identifier.

        navigation:
            Navigation configuration.

    Returns:
        Optional[str]:
            Page title.
    """

    for item in navigation.items:

        if item.route == route:
            return item.name


    return None


__all__: Final = [
    "Navigation",
    "NavigationItem",
    "DEFAULT_NAVIGATION",
    "render_navigation",
    "get_navigation_items",
    "get_page_title",
]