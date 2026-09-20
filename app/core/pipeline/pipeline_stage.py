"""
===============================================================================
Project      : AI Research Assistant
Module       : Analysis Pipeline
File         : pipeline_stage.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Defines the standard pipeline stages used throughout the
    Research Paper Intelligence Engine.

Responsibilities:
    - Centralize all pipeline stage definitions.
    - Eliminate hardcoded stage names.
    - Provide strongly typed stages for the pipeline.
    - Support logging, diagnostics, progress reporting,
      metrics, and UI updates.

Notes:
    Every pipeline component should reference PipelineStage
    instead of using string literals.
===============================================================================
"""

from __future__ import annotations

from enum import Enum


class PipelineStage(str, Enum):
    """
    Standard pipeline stages.

    These stages represent the complete lifecycle of
    research paper analysis.
    """

    INITIALIZATION = "Initialization"

    PDF_VALIDATION = "PDF Validation"

    PDF_LOADING = "PDF Loading"

    TEXT_EXTRACTION = "Text Extraction"

    TEXT_CLEANING = "Text Cleaning"

    PAPER_PREPROCESSING = "Paper Preprocessing"

    METADATA_EXTRACTION = "Metadata Extraction"

    PROMPT_BUILDING = "Prompt Building"

    LLM_ANALYSIS = "LLM Analysis"

    RESPONSE_PROCESSING = "Response Processing"

    REPORT_GENERATION = "Report Generation"

    HISTORY_SAVING = "History Saving"

    CLEANUP = "Cleanup"

    COMPLETED = "Completed"

    FAILED = "Failed"

    CANCELLED = "Cancelled"

    BUILD_CONTEXT = "Build Context"

    @property
    def label(self) -> str:
        """
        Human-readable stage name.
        """
        return self.value

    def __str__(self) -> str:
        return self.value