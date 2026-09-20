"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/shared/status_badge.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable status badge component for UI state visualization.

    Provides:
        - Success indicators
        - Warning indicators
        - Error indicators
        - Information states
        - Pipeline/API/analysis status display

Dependencies:
        - Streamlit
        - Theme System

===============================================================================
"""


from __future__ import annotations

from app.ui.html_renderer import render_html

from enum import StrEnum
from typing import Optional


import streamlit as st


from app.ui.theme import (
    ThemeManager,
)



# =============================================================================
# Status Definitions
# =============================================================================


class StatusType(StrEnum):
    """
    Supported status categories.
    """

    SUCCESS = "success"

    WARNING = "warning"

    ERROR = "danger"

    INFO = "info"

    NEUTRAL = "neutral"



# =============================================================================
# Status Metadata
# =============================================================================


_STATUS_ICONS = {

    StatusType.SUCCESS:
        "✓",

    StatusType.WARNING:
        "⚠",

    StatusType.ERROR:
        "✕",

    StatusType.INFO:
        "ℹ",

    StatusType.NEUTRAL:
        "●",

}



_STATUS_LABELS = {

    StatusType.SUCCESS:
        "Success",

    StatusType.WARNING:
        "Warning",

    StatusType.ERROR:
        "Error",

    StatusType.INFO:
        "Info",

    StatusType.NEUTRAL:
        "Status",

}



# =============================================================================
# Status Badge Component
# =============================================================================


class StatusBadge:
    """
    Render reusable status badges.

    Example:

        StatusBadge.render(
            "Completed",
            StatusType.SUCCESS,
        )

    """



    # -------------------------------------------------------------------------
    # Render Badge
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        text: str,
        status: StatusType = StatusType.INFO,
        *,
        icon: Optional[str] = None,
    ) -> None:
        """
        Render status badge.

        Args:
            text:
                Display text.

            status:
                Badge category.

            icon:
                Optional custom icon.
        """

        ThemeManager.initialize()


        badge_icon = (
            icon
            if icon
            else _STATUS_ICONS[status]
        )


        css_class = (
            "badge-"
            + status.value
        )


        render_html(f"""
            <span class="
                badge
                {css_class}
            ">
                {badge_icon}
                &nbsp;
                {text}
            </span>
            """)



    # -------------------------------------------------------------------------
    # Compact Badge
    # -------------------------------------------------------------------------

    @staticmethod
    def compact(
        status: StatusType,
    ) -> None:
        """
        Render only status label.

        Args:
            status:
                Status type.
        """

        StatusBadge.render(

            text=
                _STATUS_LABELS[status],

            status=
                status,

        )



    # -------------------------------------------------------------------------
    # Pipeline Status
    # -------------------------------------------------------------------------

    @staticmethod
    def pipeline(
        state: str,
    ) -> None:
        """
        Render pipeline execution status.

        Args:
            state:
                Pipeline state name.
        """

        normalized = state.lower()


        mapping = {

            "completed":
                StatusType.SUCCESS,

            "success":
                StatusType.SUCCESS,

            "running":
                StatusType.INFO,

            "processing":
                StatusType.INFO,

            "pending":
                StatusType.WARNING,

            "cancelled":
                StatusType.WARNING,

            "failed":
                StatusType.ERROR,

            "error":
                StatusType.ERROR,

        }


        StatusBadge.render(

            text=
                state.title(),

            status=
                mapping.get(
                    normalized,
                    StatusType.NEUTRAL,
                ),

        )



    # -------------------------------------------------------------------------
    # API Provider Status
    # -------------------------------------------------------------------------

    @staticmethod
    def provider(
        name: str,
        available: bool,
    ) -> None:
        """
        Render AI provider availability.

        Args:
            name:
                Provider name.

            available:
                Provider health.
        """

        StatusBadge.render(

            text=
                (
                    f"{name} Available"
                    if available
                    else
                    f"{name} Offline"
                ),

            status=
                (
                    StatusType.SUCCESS
                    if available
                    else StatusType.ERROR
                ),

        )



    # -------------------------------------------------------------------------
    # Analysis Status
    # -------------------------------------------------------------------------

    @staticmethod
    def analysis(
        status: str,
    ) -> None:
        """
        Render analysis status.

        Args:
            status:
                Analysis lifecycle state.
        """

        StatusBadge.pipeline(
            status
        )