"""
===============================================================================
Project      : AI Research Assistant
File         : navigation_config.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Application navigation configuration.

Responsibilities:
    - Define sidebar navigation items.
    - Provide stable page identifiers.
    - Expose the default navigation page.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from enum import StrEnum



class PageKey(StrEnum):
    DASHBOARD = "dashboard"
    ANALYZE = "analyze"
    HISTORY = "history"
    SETTINGS = "settings"
    ABOUT = "about"



@dataclass(frozen=True, slots=True)
class NavigationItem:
    """
    Represents a navigation item displayed in the application sidebar.
    """

    key: str
    label: str
    icon: str

    @property
    def display_name(self) -> str:
        """
        Return the formatted display name.

        Example:
            🏠 Dashboard
        """
        return f"{self.icon} {self.label}"


# =============================================================================
# Navigation Items
# =============================================================================

NAVIGATION_ITEMS: list[NavigationItem] = [
    NavigationItem(
        key=PageKey.DASHBOARD,
        label="Dashboard",
        icon="🏠",
    ),
    NavigationItem(
        key=PageKey.ANALYZE,
        label="Analyze Paper",
        icon="📄",
    ),
    NavigationItem(
        key=PageKey.HISTORY,
        label="Analysis History",
        icon="🕒",
    ),
    NavigationItem(
        key=PageKey.SETTINGS,
        label="Settings",
        icon="⚙️",
    ),
    NavigationItem(
        key=PageKey.ABOUT,
        label="About",
        icon="ℹ️",
    ),
]


# =============================================================================
# Navigation Constants
# =============================================================================

DEFAULT_PAGE = NAVIGATION_ITEMS[0].key


PAGE_KEYS: tuple[str, ...] = tuple(
    item.key
    for item in NAVIGATION_ITEMS
)


PAGE_LABELS: tuple[str, ...] = tuple(
    item.label
    for item in NAVIGATION_ITEMS
)


PAGE_DISPLAY_NAMES: tuple[str, ...] = tuple(
    item.display_name
    for item in NAVIGATION_ITEMS
)


PAGE_MAP: dict[str, NavigationItem] = {
    item.key: item
    for item in NAVIGATION_ITEMS
}