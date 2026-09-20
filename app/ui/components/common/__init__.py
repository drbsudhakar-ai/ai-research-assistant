"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Common UI component package initialization.

Responsibilities:
    - Expose reusable UI components.
    - Provide clean import boundaries.
    - Maintain modular Streamlit architecture.

===============================================================================
"""

from __future__ import annotations


from app.ui.components.common.badge import (
    Badge,
    BadgeVariant,
    render_badge,
)

from app.ui.components.common.divider import (
    Divider,
    render_divider,
)

from app.ui.components.common.download_button import (
    DownloadButton,
    render_download_button,
)

from app.ui.components.common.empty_state import (
    EmptyState,
    render_empty_state,
)

from app.ui.components.common.footer import (
    Footer,
    render_footer,
)

from app.ui.components.common.info_card import (
    InfoCard,
    render_info_card,
)

from app.ui.components.common.metric_card import (
    MetricCard,
    render_metric_card,
)

from app.ui.components.common.section_header import (
    SectionHeader,
    render_section_header,
)

from app.ui.components.common.status_message import (
    MessageType,
    StatusMessage,
    render_status_message,
)


__version__ = "1.0.0"


__all__ = [
    "Badge",
    "BadgeVariant",
    "render_badge",

    "Divider",
    "render_divider",

    "DownloadButton",
    "render_download_button",

    "EmptyState",
    "render_empty_state",

    "Footer",
    "render_footer",

    "InfoCard",
    "render_info_card",

    "MetricCard",
    "render_metric_card",

    "SectionHeader",
    "render_section_header",

    "MessageType",
    "StatusMessage",
    "render_status_message",
]