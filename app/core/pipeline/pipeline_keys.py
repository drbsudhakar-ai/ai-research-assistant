"""
Shared-data keys used by the pipeline.
"""

from __future__ import annotations

__all__ = ["PipelineKeys"]


class PipelineKeys:
    """Keys used to store shared data in PipelineContext."""

    PDF_PATH = "pdf_path"
    PREPARED_PAPER = "prepared_paper"
    PDF_RESULT = "pdf_result"
    PAPER_METADATA = "paper_metadata"
    ANALYSIS_RESULT = "analysis_result"
    ANALYSIS_METADATA = "analysis_metadata"
    ANALYSIS_RECORD = "analysis_record"
    HISTORY_RECORD_ID = "history_record_id"
    REPORT = "report"
    ANALYSIS_ID = "analysis_id"
    PROGRESS_REPORTER = "progress_reporter"
    ANALYSIS_TYPE = "analysis_type"
    FILENAME = "filename"
    FILE_SIZE = "file_size"
    PDF_MIME_TYPE = "application/pdf"
