"""
===============================================================================
Project      : AI Research Assistant
File         : history_service.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Business service for managing analysis history.

Responsibilities:
    - Validate analysis records.
    - Coordinate history persistence.
    - Provide business operations over analysis history.

Notes:
    - SQL must not be written in this module.
    - Database operations are delegated to HistoryRepository.
===============================================================================
"""

from __future__ import annotations

from app.models.analysis_record import AnalysisRecord
from app.storage.history_repository import HistoryRepository

__all__ = [
    "HistoryService",
]


class HistoryService:
    """
    Service responsible for managing analysis history.
    """

    def __init__(
        self,
        repository: HistoryRepository | None = None,
    ) -> None:
        """
        Initialize the history service.

        Parameters
        ----------
        repository : HistoryRepository | None, optional
            Repository implementation.
            If omitted, a default repository is created.
        """

        self._repository = repository or HistoryRepository()

    # =========================================================================
    # Create
    # =========================================================================

    def save_analysis(
        self,
        record: AnalysisRecord,
    ) -> int:
        """
        Save an analysis record.

        Parameters
        ----------
        record : AnalysisRecord

        Returns
        -------
        int
            Database identifier.

        Raises
        ------
        ValueError
            If required fields are missing.
        """

        self._validate_record(record)

        return self._repository.add(record)

    # =========================================================================
    # Read
    # =========================================================================

    def get_analysis(
        self,
        record_id: int,
    ) -> AnalysisRecord | None:
        """
        Retrieve one analysis.
        """

        return self._repository.get_by_id(record_id)

    def get_all_analyses(
        self,
    ) -> list[AnalysisRecord]:
        """
        Retrieve all analyses.
        """

        return self._repository.get_all()

    def analysis_exists(
        self,
        record_id: int,
    ) -> bool:
        """
        Check whether an analysis exists.
        """

        return self._repository.exists(record_id)

    def get_analysis_count(self) -> int:
        """
        Return total stored analyses.
        """

        return self._repository.count()

    # =========================================================================
    # Delete
    # =========================================================================

    def delete_analysis(
        self,
        record_id: int,
    ) -> bool:
        """
        Delete one analysis.

        Returns
        -------
        bool
            True if deleted.
        """

        return self._repository.delete(record_id)

    def clear_history(self) -> None:
        """
        Delete every stored analysis.
        """

        self._repository.delete_all()

    # =========================================================================
    # Validation
    # =========================================================================

    @staticmethod
    def _validate_record(
        record: AnalysisRecord,
    ) -> None:
        """
        Validate an analysis record.

        Raises
        ------
        ValueError
            If mandatory fields are missing.
        """

        if not record.title.strip():
            raise ValueError(
                "Paper title cannot be empty."
            )

        if not record.analysis.strip():
            raise ValueError(
                "Analysis cannot be empty."
            )

        if not record.model.strip():
            raise ValueError(
                "Model name cannot be empty."
            )

        if record.execution_time < 0:
            raise ValueError(
                "Execution time cannot be negative."
            )