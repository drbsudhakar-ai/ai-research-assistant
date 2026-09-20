"""
===============================================================================
Project      : AI Research Assistant
File         : dashboard.py
Version      : 2.1.0
Author       : Dr. B. Sudhakar

Description:
Dashboard page controller.

Responsibilities:
    - Coordinate dashboard data loading.
    - Prepare component view models.
    - Render dashboard components.

Business logic:
    Implemented in services layer.

===============================================================================
"""

from __future__ import annotations


import streamlit as st


from app.config.branding import get_brand_config
from app.config.loader import get_application_config
from app.config.navigation_config import PageKey
from app.core.session import set_session_value
from app.services.history_service import HistoryService


from app.ui.components import (
    AnalysisSummary,
    QuickActions,
    RecentActivity,
    SystemHealth,
)


from app.ui.components.shared import (
    HeroBanner,
)


__all__ = [
    "show_dashboard_page",
]



# =============================================================================
# Data Preparation
# =============================================================================


def _load_dashboard_data() -> dict:
    """
    Load dashboard data from services.

    Returns
    -------
    dict
        Dashboard data.
    """

    history_service = HistoryService()


    records = history_service.get_recent_analyses(
        limit=5
    )


    return {

        "records": records,

        "count": history_service.get_analysis_count(),

    }



# =============================================================================
# Navigation Actions
# =============================================================================


def _navigate_analyze() -> None:
    """
    Navigate to analyze page.
    """

    set_session_value("current_page", PageKey.ANALYZE)
    st.rerun()



def _navigate_history() -> None:
    """
    Navigate to history page.
    """

    set_session_value("current_page", PageKey.HISTORY)
    st.rerun()



def _navigate_settings() -> None:
    """
    Navigate to settings page.
    """

    set_session_value("current_page", PageKey.SETTINGS)
    st.rerun()


def _navigate_reports() -> None:
    """Open the report workspace."""

    set_session_value("current_page", PageKey.REPORT)
    st.rerun()



# =============================================================================
# Component Renderers
# =============================================================================


def _render_header() -> None:
    """
    Render dashboard hero banner.
    """

    brand = get_brand_config()
    HeroBanner.render(

        title=brand.application_name,

        subtitle=brand.tagline,

    )



def _render_summary(
    records,
) -> None:
    """
    Render analysis summary.
    """

    summary = AnalysisSummary.from_records(
        records
    )


    AnalysisSummary.render(
        summary
    )



def _render_actions() -> None:
    """
    Render quick actions.
    """

    actions = QuickActions.default_actions(

        analyze_callback=_navigate_analyze,

        history_callback=_navigate_history,

        settings_callback=_navigate_settings,

        export_callback=_navigate_reports,

    )

    actions = [action for action in actions if action.callback is not None]


    QuickActions.render(
        actions
    )



def _render_activity(
    records,
) -> None:
    """
    Render recent activity.
    """

    activities = RecentActivity.from_records(
        records
    )


    RecentActivity.render(
        activities
    )



def _render_health() -> None:
    """
    Render system health.
    """

    health = SystemHealth.default_checks(

        llm_available=True,

        database_available=True,

        pipeline_ready=True,

        provider_name=get_application_config().llm.provider.title(),

    )


    SystemHealth.render(
        health
    )



# =============================================================================
# Public API
# =============================================================================


def show_dashboard_page() -> None:
    """
    Render Dashboard page.
    """

    dashboard = _load_dashboard_data()


    _render_header()


    st.divider()


    _render_summary(
        dashboard["records"]
    )


    _render_actions()


    _render_activity(
        dashboard["records"]
    )


    _render_health()
