"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/status_message.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Reusable status message UI component for Streamlit pages.

Responsibilities:
    - Render consistent success, error, warning, and information messages.
    - Provide a unified interface for application notifications.
    - Support optional titles and icons.

Non-Responsibilities:
    - Exception handling.
    - Logging.
    - Pipeline status management.
    - Business logic.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import streamlit as st


class MessageType(str, Enum):
    """
    Supported status message types.
    """

    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class StatusMessage:
    """
    Represents a reusable status message component.

    Attributes:
        message:
            Message content.

        message_type:
            Type of status notification.

        title:
            Optional heading.

        icon:
            Optional custom icon.

        expanded:
            Whether the message content should be emphasized.
    """

    message: str

    message_type: MessageType = MessageType.INFO

    title: Optional[str] = None
    icon: Optional[str] = None
    expanded: bool = False

    def render(self) -> None:
        """
        Render status message in Streamlit.
        """

        icon = self.icon

        prefix = (
            f"**{self.title}**  \n"
            if self.title
            else ""
        )

        content = (
            f"{prefix}{self.message}"
        )

        if self.message_type == MessageType.SUCCESS:

            st.success(
                content,
                icon=icon,
            )

        elif self.message_type == MessageType.ERROR:

            st.error(
                content,
                icon=icon,
            )

        elif self.message_type == MessageType.WARNING:

            st.warning(
                content,
                icon=icon,
            )

        else:

            st.info(
                content,
                icon=icon,
            )


def render_status_message(
    message: str,
    *,
    message_type: MessageType = MessageType.INFO,
    title: Optional[str] = None,
    icon: Optional[str] = None,
    expanded: bool = False,
) -> None:
    """
    Functional helper for rendering status messages.

    Examples:

        render_status_message(
            "Analysis completed successfully.",
            message_type=MessageType.SUCCESS,
            icon="✅"
        )

        render_status_message(
            "Pipeline execution failed.",
            message_type=MessageType.ERROR,
            icon="❌"
        )
    """

    status = StatusMessage(
        message=message,
        message_type=message_type,
        title=title,
        icon=icon,
        expanded=expanded,
    )

    status.render()


__all__ = [
    "MessageType",
    "StatusMessage",
    "render_status_message",
]