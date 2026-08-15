"""
Shared-data keys used by the pipeline.
"""

from __future__ import annotations

__all__ = ["PipelineKeys"]


class PipelineKeys:
    """Keys used to store shared data in PipelineContext."""

    # Input
    PREPARED_PAPER = "prepared_paper"
    PDF_RESULT = "pdf_result"

    # Output
    ANALYSIS_RECORD = "analysis_record"
    REPORT = "report"
    ANALYSIS_ID = "analysis_id"

    # Pipeline Services
    PROGRESS_REPORTER = "progress_reporter"
    ANALYSIS_TYPE = "analysis_type"

    # Metadata
    FILENAME = "filename"
    FILE_SIZE = "file_size"
    PDF_MIME_TYPE = "application/pdf"