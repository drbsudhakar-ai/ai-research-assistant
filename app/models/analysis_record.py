"""
===============================================================================
Project      : AI Research Assistant
File         : analysis_record.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Domain model representing a completed research paper analysis.

Responsibilities:
    - Represent a single analysis record.
    - Provide serialization helpers.
    - Remain independent of UI, database, and AI services.

Notes:
    - This module contains no business logic.
===============================================================================
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any


__all__ = [
    "AnalysisRecord",
]


@dataclass(slots=True)
class AnalysisRecord:
    """
    Represents one research paper analysis.
    """

    id: int | None = None

    title: str = ""
    filename: str = ""

    input_source: str = ""

    analysis_type: str = ""

    # PDF Statistics
    total_pages: int = 0
    total_characters: int = 0

    # AI Result
    analysis: str = ""

    # LLM Information
    provider: str = ""
    model: str = ""

    # Performance
    execution_time: float = 0.0

    # Metadata
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(
            timespec="seconds"
        )
    )

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the analysis record to a dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representation of the record.
        """
        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "AnalysisRecord":
        """
        Create an AnalysisRecord from a dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            Dictionary containing analysis data.

        Returns
        -------
        AnalysisRecord
            Constructed analysis record.
        """
        return cls(**data)