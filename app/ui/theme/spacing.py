"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme System
File         : spacing.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Spacing system for the Streamlit UI.

    Defines:
    - Global spacing scale
    - Layout spacing
    - Component spacing
    - Container spacing
    - Responsive layout helpers

Purpose:
    - Maintain consistent spacing across all pages.
    - Eliminate hardcoded margins and paddings.
    - Support professional dashboard-style layouts.

Usage:
    from app.ui.theme.spacing import SPACING

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class SpacingScale:
    """
    Base spacing scale.

    Uses a 4px-based spacing system.
    """

    ZERO: str = "0px"

    XS: str = "4px"

    SM: str = "8px"

    MD: str = "16px"

    LG: str = "24px"

    XL: str = "32px"

    XXL: str = "48px"

    XXXL: str = "64px"


@dataclass(frozen=True)
class LayoutSpacing:
    """
    Page and layout level spacing.
    """

    PAGE_PADDING_TOP: str = "24px"

    PAGE_PADDING_BOTTOM: str = "48px"

    PAGE_PADDING_HORIZONTAL: str = "32px"

    SECTION_GAP: str = "32px"

    SUBSECTION_GAP: str = "24px"

    CONTENT_GAP: str = "16px"


@dataclass(frozen=True)
class ComponentSpacing:
    """
    Component internal spacing.

    Used for cards, buttons, forms, metrics, etc.
    """

    CARD_PADDING: str = "20px"

    CARD_HEADER_GAP: str = "12px"

    CARD_CONTENT_GAP: str = "16px"

    BUTTON_PADDING_VERTICAL: str = "10px"

    BUTTON_PADDING_HORIZONTAL: str = "20px"

    INPUT_PADDING: str = "12px"

    BADGE_PADDING: str = "6px"


@dataclass(frozen=True)
class DashboardSpacing:
    """
    Dashboard-specific spacing.

    Used by:
    - Home page
    - History dashboard
    - Analysis results dashboard
    """

    METRIC_CARD_GAP: str = "16px"

    GRID_GAP: str = "24px"

    PANEL_GAP: str = "32px"

    CHART_PADDING: str = "16px"


@dataclass(frozen=True)
class SidebarSpacing:
    """
    Sidebar layout spacing.
    """

    SIDEBAR_PADDING: str = "16px"

    MENU_ITEM_PADDING: str = "12px"

    MENU_ITEM_GAP: str = "8px"


@dataclass(frozen=True)
class ResponsiveSpacing:
    """
    Responsive layout spacing adjustments.

    Streamlit applications need simpler responsive rules
    because browser-level CSS control is limited.
    """

    MOBILE_PADDING: str = "16px"

    TABLET_PADDING: str = "24px"

    DESKTOP_PADDING: str = "32px"


@dataclass(frozen=True)
class Spacing:
    """
    Root spacing token container.
    """

    SCALE: Final = SpacingScale()

    LAYOUT: Final = LayoutSpacing()

    COMPONENTS: Final = ComponentSpacing()

    DASHBOARD: Final = DashboardSpacing()

    SIDEBAR: Final = SidebarSpacing()

    RESPONSIVE: Final = ResponsiveSpacing()


# Global spacing instance
SPACING: Final = Spacing()