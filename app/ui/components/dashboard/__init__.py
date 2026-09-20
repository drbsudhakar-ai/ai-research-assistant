"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/dashboard/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Public interface for dashboard UI components.

    Provides:

        - Analysis summary metrics
        - Recent activity timeline
        - Quick workflow actions
        - System health monitoring

Usage:

    from app.ui.components.dashboard import (
        AnalysisSummary,
        RecentActivity,
        QuickActions,
        SystemHealth,
    )

===============================================================================
"""


# =============================================================================
# Analysis Summary
# =============================================================================

from app.ui.components.dashboard.analysis_summary import (
    AnalysisSummary,
    AnalysisSummaryData,
)



# =============================================================================
# Recent Activity
# =============================================================================

from app.ui.components.dashboard.recent_activity import (
    RecentActivity,
    ActivityItem,
)



# =============================================================================
# Quick Actions
# =============================================================================

from app.ui.components.dashboard.quick_actions import (
    QuickActions,
    QuickAction,
)



# =============================================================================
# System Health
# =============================================================================

from app.ui.components.dashboard.system_health import (
    SystemHealth,
    HealthStatus,
)



# =============================================================================
# Public API
# =============================================================================


__all__ = [

    # Analysis Summary
    "AnalysisSummary",
    "AnalysisSummaryData",


    # Recent Activity
    "RecentActivity",
    "ActivityItem",


    # Quick Actions
    "QuickActions",
    "QuickAction",


    # System Health
    "SystemHealth",
    "HealthStatus",

]



__version__ = "1.0.0"