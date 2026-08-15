"""
===============================================================================
Project      : AI Research Assistant
File         : history_service.py
Version      : 2.0.0
Author       : Dr. B. Sudhakar

Description:
Business service for managing analysis history.

Responsibilities:
    - Validate analysis records.
    - Coordinate history persistence.
    - Provide business operations over analysis history.
    - Provide dashboard-friendly history queries.

Notes:
    - SQL must not be written in this module.
    - Database operations are delegated to HistoryRepository.
===============================================================================
"""

from __future__ import annotations

from app.models.analysis_record import AnalysisRecord
from app.models.analysis_result import AnalysisResult
from app.models.prepared_paper import PreparedPaper
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
        Initialize history service.

        Parameters
        ----------
        repository:
            Repository implementation.
            If omitted, default repository is created.
        """

        self._repository = (
            repository
            or HistoryRepository()
        )

    # =========================================================================
    # Create
    # =========================================================================

    def save_analysis(
        self,
        record: AnalysisRecord,
    ) -> int:
        """
        Save analysis record.

        Parameters
        ----------
        record:
            Analysis record.

        Returns
        -------
        int
            Database identifier.
        """

        self._validate_record(
            record
        )

        return self._repository.add(
            record
        )

    def save_result(
        self,
        result: AnalysisResult,
        *,
        paper: PreparedPaper | None = None,
        title: str = "",
        filename: str = "",
        input_source: str = "PDF",
        analysis_type: str = "Research Paper Analysis",
        total_pages: int = 0,
        total_characters: int = 0,
    ) -> int:
        """Persist an AnalysisResult as a history AnalysisRecord."""

        record = AnalysisRecord.from_result(
            result,
            paper=paper,
            title=title,
            filename=filename,
            input_source=input_source,
            analysis_type=analysis_type,
            total_pages=total_pages,
            total_characters=total_characters,
        )
        return self.save_analysis(record)

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

        return self._repository.get_by_id(
            record_id
        )


    def get_all_analyses(
        self,
    ) -> list[AnalysisRecord]:
        """
        Retrieve all analyses.

        Returns
        -------
        list[AnalysisRecord]
        """

        return self._repository.get_all()


    def get_recent_analyses(
        self,
        limit: int = 5,
    ) -> list[AnalysisRecord]:
        """
        Retrieve latest analysis records.

        Used by:
            - Dashboard recent activity
            - Dashboard summary widgets

        Parameters
        ----------
        limit:
            Maximum number of records.

        Returns
        -------
        list[AnalysisRecord]
            Recent analysis records.
        """

        if limit <= 0:
            return []


        records = self._repository.get_all()


        return records[:limit]


    def analysis_exists(
        self,
        record_id: int,
    ) -> bool:
        """
        Check whether analysis exists.
        """

        return self._repository.exists(
            record_id
        )


    def get_analysis_count(
        self,
    ) -> int:
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

        return self._repository.delete(
            record_id
        )


    def clear_history(
        self,
    ) -> None:
        """
        Delete all stored analyses.
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
        Validate analysis record.

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