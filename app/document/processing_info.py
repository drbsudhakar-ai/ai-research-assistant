"""
===============================================================================
Project      : AI Research Assistant
Module       : Document Model
File         : processing_info.py
Version      : 1.0.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProcessingInfo:
    """
    Stores preprocessing statistics.
    """

    extraction_time: float = 0.0

    cleaning_time: float = 0.0

    section_detection_time: float = 0.0

    metadata_time: float = 0.0

    validation_time: float = 0.0

    total_time: float = 0.0

    removed_reference_characters: int = 0

    removed_appendix_characters: int = 0