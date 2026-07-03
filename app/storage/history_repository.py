"""
===============================================================================
Project      : AI Research Assistant
File         : history_repository.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Repository responsible for persistence of analysis history.

Responsibilities:
    - Insert analysis records.
    - Retrieve analysis records.
    - Delete analysis records.
    - Count stored analyses.

Notes:
    - This module contains only database access logic.
    - Business logic must not be implemented here.
===============================================================================
"""

from __future__ import annotations

import sqlite3

from app.models.analysis_record import AnalysisRecord
from app.storage.database import get_connection

__all__ = [
    "HistoryRepository",
]


class HistoryRepository:
    """
    Repository for analysis history persistence.
    """

    # =========================================================================
    # Create
    # =========================================================================

    def add(self, record: AnalysisRecord) -> int:
        """
        Save an analysis record.

        Parameters
        ----------
        record : AnalysisRecord
            Analysis record to store.

        Returns
        -------
        int
            Newly generated database identifier.
        """

        sql = """
        INSERT INTO analysis_history (

            title,

            filename,

            input_source,

            analysis_type,

            total_pages,

            total_characters,

            analysis,

            provider,

            model,

            execution_time,

            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with get_connection() as connection:

            cursor = connection.execute(
                sql,
                (
                    record.title,
                    record.filename,
                    record.input_source,
                    record.analysis_type,
                    record.total_pages,
                    record.total_characters,
                    record.analysis,
                    record.provider,
                    record.model,
                    record.execution_time,
                    record.created_at,
                ),
            )

            connection.commit()

            return int(cursor.lastrowid)

    # =========================================================================
    # Read
    # =========================================================================

    def get_all(self) -> list[AnalysisRecord]:
        """
        Retrieve every stored analysis.

        Returns
        -------
        list[AnalysisRecord]
        """

        sql = """
        SELECT *
        FROM analysis_history
        ORDER BY id DESC
        """

        with get_connection() as connection:

            rows = connection.execute(sql).fetchall()

        return [self._row_to_record(row) for row in rows]

    def get_by_id(
        self,
        record_id: int,
    ) -> AnalysisRecord | None:
        """
        Retrieve one analysis by identifier.
        """

        sql = """
        SELECT *
        FROM analysis_history
        WHERE id = ?
        """

        with get_connection() as connection:

            row = connection.execute(
                sql,
                (record_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_record(row)

    def exists(
        self,
        record_id: int,
    ) -> bool:
        """
        Check whether an analysis exists.
        """

        sql = """
        SELECT 1
        FROM analysis_history
        WHERE id = ?
        LIMIT 1
        """

        with get_connection() as connection:

            row = connection.execute(
                sql,
                (record_id,),
            ).fetchone()

        return row is not None

    def count(self) -> int:
        """
        Return total number of stored analyses.
        """

        sql = """
        SELECT COUNT(*) AS total
        FROM analysis_history
        """

        with get_connection() as connection:

            row = connection.execute(sql).fetchone()

        return int(row["total"])

    # =========================================================================
    # Delete
    # =========================================================================

    def delete(
        self,
        record_id: int,
    ) -> bool:
        """
        Delete one analysis.

        Returns
        -------
        bool
            True if a record was removed.
        """

        sql = """
        DELETE FROM analysis_history
        WHERE id = ?
        """

        with get_connection() as connection:

            cursor = connection.execute(
                sql,
                (record_id,),
            )

            connection.commit()

        return cursor.rowcount > 0

    def delete_all(self) -> None:
        """
        Delete every stored analysis.
        """

        sql = "DELETE FROM analysis_history"

        with get_connection() as connection:

            connection.execute(sql)

            connection.commit()

    # =========================================================================
    # Private Helpers
    # =========================================================================

    @staticmethod
    def _row_to_record(
        row: sqlite3.Row,
    ) -> AnalysisRecord:
        """
        Convert a SQLite row into an AnalysisRecord.
        """

        return AnalysisRecord(
            id=row["id"],
            title=row["title"],
            filename=row["filename"],
            input_source=row["input_source"],
            analysis_type=row["analysis_type"],

            # PDF Statistics
            total_pages=row["total_pages"],
            total_characters=row["total_characters"],

            # AI Analysis
            analysis=row["analysis"],

            # LLM Information
            provider=row["provider"],
            model=row["model"],

            # Performance
            execution_time=row["execution_time"],

            # Metadata
            created_at=row["created_at"],
        )