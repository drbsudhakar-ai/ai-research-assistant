"""
===============================================================================
Project      : AI Research Assistant
Module       : History UI Components
File         : app/ui/components/history/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Public interface for the Analysis History UI components.

Responsibilities:
    - Expose reusable History UI components.
    - Provide clean import boundaries.
    - Hide implementation details.
    - Maintain a stable public API.

Components:
    - SearchToolbar
    - FilterPanel
    - HistoryTable
    - Pagination

Usage:
    from app.ui.components.history import (
        SearchToolbar,
        FilterPanel,
        HistoryTable,
        Pagination,
    )

===============================================================================
"""

from __future__ import annotations

from app.ui.components.history.search_toolbar import (
    SearchToolbar,
    SearchToolbarState,
)

from app.ui.components.history.filter_panel import (
    FilterPanel,
    FilterState,
    SortDirection,
    SortField,
)

from app.ui.components.history.history_table import (
    HistoryTable,
)

from app.ui.components.history.pagination import (
    Pagination,
    PaginationState,
)

__version__ = "1.0.0"

__all__ = [
    # Search
    "SearchToolbar",
    "SearchToolbarState",

    # Filters
    "FilterPanel",
    "FilterState",
    "SortField",
    "SortDirection",

    # Table
    "HistoryTable",

    # Pagination
    "Pagination",
    "PaginationState",
]