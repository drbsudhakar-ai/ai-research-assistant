"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/analyze/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Analyze page component package initialization.

Responsibilities:
    - Expose Analyze UI components.
    - Maintain clean component imports.
    - Support modular Streamlit architecture.

Non-Responsibilities:
    - Pipeline execution.
    - AI analysis.
    - Data persistence.

===============================================================================
"""

from __future__ import annotations


# Upload component
from .upload_card import (
    render_upload_card,
)


# Paper information component
from .paper_info import (
    render_paper_info,
)


# Paper preview component
from .paper_preview import (
    render_paper_preview,
)


# Progress component
from .progress_panel import (
    render_progress_panel,
)


# Analysis report component
from .analysis_report import (
    render_analysis_report,
)


# Report export component
from .report_export import (
    render_report_export,
)


__all__ = [

    "render_upload_card",

    "render_paper_info",

    "render_paper_preview",

    "render_progress_panel",

    "render_analysis_report",

    "render_report_export",

]