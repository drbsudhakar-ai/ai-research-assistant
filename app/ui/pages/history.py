"""
===============================================================================
Project      : AI Research Assistant
File         : history.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
History page controller.

Responsibilities:
    - Load analysis history.
    - Coordinate history UI components.
    - Manage page-level state.

Business logic:
    Implemented in services layer.

===============================================================================
"""

from __future__ import annotations


import streamlit as st


from app.config.branding import get_brand_config
from app.services.history_service import HistoryService


from app.ui.components.history import (
    FilterPanel,
    FilterState,
    SortField,
    SortDirection,
    HistoryTable,
    Pagination,
    SearchToolbar,
)


from app.ui.components.common import (
    EmptyState,
)


from app.ui.components.history.filter_panel import FilterState
from app.ui.components.shared import (
    HeroBanner,
)



__all__ = [
    "show_history_page",
]



# =============================================================================
# Data Loading
# =============================================================================


def _load_history() -> list:
    """
    Load analysis history.

    Returns
    -------
    list
        Analysis records.
    """

    service = HistoryService()

    return service.get_all_analyses()



# =============================================================================
# Filtering
# =============================================================================


def _apply_search(
    records: list,
    query: str,
) -> list:
    """
    Filter records using search query.

    Parameters
    ----------
    records:
        History records.

    query:
        Search text.

    Returns
    -------
    list
        Filtered records.
    """

    if not query:

        return records


    query = query.lower()


    return [

        record

        for record in records

        if query in record.title.lower()

        or query in record.model.lower()

        or query in record.provider.lower()

    ]



# =============================================================================
# Render Sections
# =============================================================================


def _render_header() -> None:
    """
    Render history header.
    """

    brand = get_brand_config()
    HeroBanner.render(

        title="Analysis History",

        subtitle=brand.tagline,

    )



def _render_toolbar() -> str:
    """
    Render search toolbar.

    Returns
    -------
    str
        Search query.
    """

    return SearchToolbar().render().query



def _render_filters() -> FilterState:
    """
    Render filter controls.

    Returns
    -------
    FilterState
        Selected filter options.
    """

    panel = FilterPanel()

    return panel.render()

def _apply_filters(
    records: list,
    state: FilterState,
) -> list:
    """
    Apply history filters.

    Parameters
    ----------
    records:
        Analysis records.

    state:
        Filter configuration.

    Returns
    -------
    list
        Filtered records.
    """

    result = records


    if state.provider != "All":

        result = [

            r

            for r in result

            if r.provider == state.provider

        ]


    if state.model != "All":

        result = [

            r

            for r in result

            if r.model == state.model

        ]


    if state.status != "All":

        result = [

            r

            for r in result

            if getattr(
                r,
                "status",
                "Completed",
            ).lower()
            ==
            state.status.lower()

        ]


    if state.date_from:

        result = [

            r

            for r in result

            if r.created_at.date()
            >=
            state.date_from

        ]


    if state.date_to:

        result = [

            r

            for r in result

            if r.created_at.date()
            <=
            state.date_to

        ]


    reverse = (
        state.sort_direction
        == SortDirection.DESC
    )


    if state.sort_field == SortField.TITLE:

        result.sort(
            key=lambda x: x.title,
            reverse=reverse,
        )


    elif state.sort_field == SortField.EXECUTION_TIME:

        result.sort(
            key=lambda x: x.execution_time,
            reverse=reverse,
        )


    elif state.sort_field == SortField.PROVIDER:

        result.sort(
            key=lambda x: x.provider,
            reverse=reverse,
        )


    elif state.sort_field == SortField.MODEL:

        result.sort(
            key=lambda x: x.model,
            reverse=reverse,
        )


    return result

def _render_table(
    records: list,
) -> None:
    """
    Render history table.
    """

    if not records:

        EmptyState.render(

            title="No Analyses Found",

            message=(
                "Your completed research analyses "
                "will appear here."
            ),

        )

        return



    table = HistoryTable()


    event = table.render(
        _to_table_records(records)
    )
    table._handle_table_event(event)


# =============================================================================
# Public API
# =============================================================================


def show_history_page() -> None:
    """
    Render History page.
    """

    _render_header()


    st.divider()


    records = _load_history()


    if not records:

        EmptyState.render(

            title="No History Available",

            message=(
                "Analyze a research paper to "
                "create your first history entry."
            ),

        )

        return



    query = _render_toolbar()


    filtered_records = _apply_search(

        records,

        query,

    )


    filter_state = _render_filters()


    filtered_records = _apply_filters(
        filtered_records,
        filter_state,
    )


    _render_table(
        filtered_records
    )

def _to_table_records(
    records: list,
) -> list[dict]:
    """
    Convert AnalysisRecord objects
    into HistoryTable input format.
    """

    return [

        {
            "id": record.id,

            "title": record.title,

            "filename": record.filename,

            "input_source": record.input_source,

            "provider": record.provider,

            "model": record.model,

            "created_at": record.created_at,

            "analysis": record.analysis,

            "research_gap": record.research_gap,

            "future_scope": record.future_scope,

        }

        for record in records

    ]
