"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Components Package
File         : app/ui/components/__init__.py
Version      : 2.1.0
Author       : Dr. B. Sudhakar

Description:
    Root package interface for all UI components.

    This module exposes the public API for every UI component package and keeps
    imports synchronized with the actual project structure.

===============================================================================
"""

from __future__ import annotations


# =============================================================================
# Common Components
# =============================================================================

from app.ui.components.common import (
    Badge,
    BadgeVariant,
    Divider,
    DownloadButton,
    EmptyState,
    Footer,
    InfoCard,
    MessageType,
    MetricCard,
    SectionHeader,
    StatusMessage,
    render_badge,
    render_divider,
    render_download_button,
    render_empty_state,
    render_footer,
    render_info_card,
    render_metric_card,
    render_section_header,
    render_status_message,
)


# =============================================================================
# Home Components
# =============================================================================

from app.ui.components.home import (
    DeveloperCard,
    FeatureCard,
    Highlight,
    Highlights,
    HeroSection,
    ResearchDomains,
    StatisticItem,
    StatisticsPanel,
    TechnologyStack,
    Workflow,
    WorkflowStep,
    render_developer_card,
    render_feature_card,
    render_highlights,
    render_hero_section,
    render_research_domains,
    render_statistics_panel,
    render_technology_stack,
    render_workflow,
)


# =============================================================================
# Analyze Components
# =============================================================================

from app.ui.components.analyze import (
    render_analysis_report,
    render_paper_info,
    render_paper_preview,
    render_progress_panel,
    render_report_export,
    render_upload_card,
)


# =============================================================================
# Dashboard Components
# =============================================================================

from app.ui.components.dashboard import (
    AnalysisSummary,
    AnalysisSummaryData,
    ActivityItem,
    HealthStatus,
    QuickAction,
    QuickActions,
    RecentActivity,
    SystemHealth,
)


# =============================================================================
# History Components
# =============================================================================

from app.ui.components.history import (
    FilterPanel,
    FilterState,
    HistoryTable,
    Pagination,
    PaginationState,
    SearchToolbar,
    SearchToolbarState,
    SortDirection,
    SortField,
)


# =============================================================================
# Settings Components
# =============================================================================

from app.ui.components.settings import (
    render_about_settings,
    render_export_settings,
    render_general_settings,
    render_llm_settings,
    render_provider_settings,
)


__version__ = "2.1.0"


__all__ = [

    # -------------------------------------------------------------------------
    # Common
    # -------------------------------------------------------------------------

    "Badge",
    "BadgeVariant",
    "Divider",
    "DownloadButton",
    "EmptyState",
    "Footer",
    "InfoCard",
    "MetricCard",
    "SectionHeader",
    "StatusMessage",
    "MessageType",

    "render_badge",
    "render_divider",
    "render_download_button",
    "render_empty_state",
    "render_footer",
    "render_info_card",
    "render_metric_card",
    "render_section_header",
    "render_status_message",


    # -------------------------------------------------------------------------
    # Home
    # -------------------------------------------------------------------------

    "HeroSection",
    "StatisticItem",
    "StatisticsPanel",
    "FeatureCard",
    "Highlight",
    "Highlights",
    "ResearchDomains",
    "Workflow",
    "WorkflowStep",
    "TechnologyStack",
    "DeveloperCard",

    "render_hero_section",
    "render_statistics_panel",
    "render_feature_card",
    "render_highlights",
    "render_research_domains",
    "render_workflow",
    "render_technology_stack",
    "render_developer_card",


    # -------------------------------------------------------------------------
    # Analyze
    # -------------------------------------------------------------------------

    "render_upload_card",
    "render_paper_info",
    "render_paper_preview",
    "render_progress_panel",
    "render_analysis_report",
    "render_report_export",


    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    "AnalysisSummary",
    "AnalysisSummaryData",

    "RecentActivity",
    "ActivityItem",

    "QuickActions",
    "QuickAction",

    "SystemHealth",
    "HealthStatus",


    # -------------------------------------------------------------------------
    # History
    # -------------------------------------------------------------------------

    "SearchToolbar",
    "SearchToolbarState",
    "FilterPanel",
    "FilterState",
    "SortField",
    "SortDirection",
    "HistoryTable",
    "Pagination",
    "PaginationState",


    # -------------------------------------------------------------------------
    # Settings
    # -------------------------------------------------------------------------

    "render_general_settings",
    "render_llm_settings",
    "render_provider_settings",
    "render_export_settings",
    "render_about_settings",

]