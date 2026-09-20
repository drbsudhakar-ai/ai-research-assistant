"""
AI Research Assistant
Export Settings Enums

Defines strongly typed enums used by Export Settings.

Responsibilities:
    - Report format selection
    - Export quality presets
    - Report content types
    - File naming strategies
    - Export behaviour modes

No UI logic.
No persistence logic.

Version:
    1.0.0
"""

from __future__ import annotations

from enum import Enum


# ============================================================
# Export Format
# ============================================================


class ExportFormat(str, Enum):
    """
    Supported report export formats.
    """

    PDF = "pdf"

    MARKDOWN = "markdown"

    DOCX = "docx"

    HTML = "html"


# ============================================================
# Report Type
# ============================================================


class ReportType(str, Enum):
    """
    Types of research reports.
    """

    FULL_REPORT = "full_report"

    EXECUTIVE_SUMMARY = "executive_summary"

    RESEARCH_SUMMARY = "research_summary"

    CITATION_REPORT = "citation_report"


# ============================================================
# Export Quality
# ============================================================


class ExportQuality(str, Enum):
    """
    Export rendering quality.
    """

    STANDARD = "standard"

    HIGH = "high"

    ACADEMIC = "academic"


# ============================================================
# File Naming Strategy
# ============================================================


class FileNamingStrategy(str, Enum):
    """
    Generated file naming rules.
    """

    PAPER_TITLE = "paper_title"

    TITLE_WITH_DATE = "title_with_date"

    TIMESTAMP = "timestamp"

    CUSTOM = "custom"


# ============================================================
# Export Destination
# ============================================================


class ExportDestination(str, Enum):
    """
    Export storage destination.
    """

    DOWNLOAD = "download"

    LOCAL_FOLDER = "local_folder"

    CUSTOM_PATH = "custom_path"


# ============================================================
# Include Options
# ============================================================


class ReportSection(str, Enum):
    """
    Optional report sections.
    """

    ABSTRACT = "abstract"

    INTRODUCTION = "introduction"

    RESEARCH_GAP = "research_gap"

    METHODOLOGY = "methodology"

    CONTRIBUTIONS = "contributions"

    RESULTS = "results"

    LIMITATIONS = "limitations"

    FUTURE_WORK = "future_work"

    REFERENCES = "references"


__all__ = [

    "ExportFormat",

    "ReportType",

    "ExportQuality",

    "FileNamingStrategy",

    "ExportDestination",

    "ReportSection",
]