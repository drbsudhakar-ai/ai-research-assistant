"""
app/ui/components/settings/api/components/status_badge.py

Reusable status badge component.

Provides consistent UI indicators for:
- Connected
- Disconnected
- Error
- Warning
- Pending
- Unsaved changes

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from enum import Enum

import streamlit as st



# ============================================================================
# Status Types
# ============================================================================


class StatusType(str, Enum):
    """
    Supported status badge types.
    """

    SUCCESS = "success"

    ERROR = "error"

    WARNING = "warning"

    INFO = "info"

    PENDING = "pending"

    DISABLED = "disabled"

    DEFAULT = "default"



# ============================================================================
# Badge Renderer
# ============================================================================


def render_status_badge(
    label: str,
    status: StatusType = StatusType.DEFAULT,
) -> None:
    """
    Render status badge.

    Parameters
    ----------
    label:
        Display text.

    status:
        Badge status type.
    """


    icon = (
        get_status_icon(
            status
        )
    )


    text = (
        f"{icon} {label}"
    )


    if status == StatusType.SUCCESS:

        st.success(
            text
        )


    elif status == StatusType.ERROR:

        st.error(
            text
        )


    elif status == StatusType.WARNING:

        st.warning(
            text
        )


    elif status == StatusType.INFO:

        st.info(
            text
        )


    elif status == StatusType.PENDING:

        st.warning(
            text
        )


    elif status == StatusType.DISABLED:

        st.caption(
            text
        )


    else:

        st.write(
            text
        )



# ============================================================================
# Icon Mapping
# ============================================================================


def get_status_icon(
    status: StatusType,
) -> str:
    """
    Return icon for status.
    """

    icons = {

        StatusType.SUCCESS:
            "🟢",

        StatusType.ERROR:
            "🔴",

        StatusType.WARNING:
            "🟡",

        StatusType.INFO:
            "🔵",

        StatusType.PENDING:
            "⏳",

        StatusType.DISABLED:
            "⚪",

        StatusType.DEFAULT:
            "⚫",
    }


    return icons.get(
        status,
        "⚫",
    )



# ============================================================================
# Convenience Renderers
# ============================================================================


def render_connected_badge() -> None:
    """
    Render connected status.
    """

    render_status_badge(
        "Connected",
        StatusType.SUCCESS,
    )



def render_error_badge(
    message: str = "Error",
) -> None:
    """
    Render error status.
    """

    render_status_badge(
        message,
        StatusType.ERROR,
    )



def render_pending_badge(
    message: str = "Testing...",
) -> None:
    """
    Render pending status.
    """

    render_status_badge(
        message,
        StatusType.PENDING,
    )



def render_disabled_badge() -> None:
    """
    Render disabled status.
    """

    render_status_badge(
        "Disabled",
        StatusType.DISABLED,
    )



# ============================================================================
# Exports
# ============================================================================


__all__ = [
    "StatusType",
    "render_status_badge",
    "render_connected_badge",
    "render_error_badge",
    "render_pending_badge",
    "render_disabled_badge",
]