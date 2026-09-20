from __future__ import annotations

from pathlib import Path

from app.models.analysis_record import AnalysisRecord
from app.models.research_project import ResearchProject, ResearchSynthesis, utc_now
from app.storage.database import get_connection
from app.storage.history_repository import HistoryRepository


class ResearchProjectRepository:
    def __init__(self, database_path: Path | None = None) -> None:
        self._database_path = database_path

    def create(self, project: ResearchProject) -> int:
        with get_connection(self._database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO research_projects "
                "(name, research_domain, objective, status, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (project.name, project.research_domain, project.objective,
                 project.status, project.created_at, project.updated_at),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def list_all(self) -> list[ResearchProject]:
        with get_connection(self._database_path) as connection:
            rows = connection.execute(
                "SELECT * FROM research_projects ORDER BY updated_at DESC"
            ).fetchall()
        return [ResearchProject(**dict(row)) for row in rows]

    def add_papers(self, project_id: int, analysis_ids: list[int]) -> int:
        added = 0
        with get_connection(self._database_path) as connection:
            for analysis_id in analysis_ids:
                cursor = connection.execute(
                    "INSERT OR IGNORE INTO research_project_papers "
                    "(project_id, analysis_id, added_at) VALUES (?, ?, ?)",
                    (project_id, analysis_id, utc_now()),
                )
                added += cursor.rowcount
            connection.execute(
                "UPDATE research_projects SET updated_at = ? WHERE id = ?",
                (utc_now(), project_id),
            )
            connection.commit()
        return added

    def get_papers(self, project_id: int) -> list[AnalysisRecord]:
        with get_connection(self._database_path) as connection:
            rows = connection.execute(
                "SELECT a.* FROM analysis_history a "
                "JOIN research_project_papers p ON p.analysis_id = a.id "
                "WHERE p.project_id = ? ORDER BY p.added_at DESC, a.id DESC", (project_id,)
            ).fetchall()
        return [HistoryRepository._row_to_record(row) for row in rows]

    def linked_filenames(self, project_id: int) -> set[str]:
        """Return normalized filenames already attached to a project."""
        with get_connection(self._database_path) as connection:
            rows = connection.execute(
                "SELECT a.filename FROM analysis_history a "
                "JOIN research_project_papers p ON p.analysis_id = a.id "
                "WHERE p.project_id = ?", (project_id,)
            ).fetchall()
        return {str(row["filename"]).strip().casefold() for row in rows}

    def save_synthesis(self, result: ResearchSynthesis) -> int:
        with get_connection(self._database_path) as connection:
            cursor = connection.execute(
                "INSERT INTO research_syntheses "
                "(project_id, synthesis, consolidated_gap, future_scope, "
                "provider, model, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (result.project_id, result.synthesis, result.consolidated_gap,
                 result.future_scope, result.provider, result.model, result.created_at),
            )
            connection.execute(
                "UPDATE research_projects SET updated_at = ? WHERE id = ?",
                (result.created_at, result.project_id),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def latest_synthesis(self, project_id: int) -> ResearchSynthesis | None:
        with get_connection(self._database_path) as connection:
            row = connection.execute(
                "SELECT * FROM research_syntheses WHERE project_id = ? "
                "ORDER BY id DESC LIMIT 1", (project_id,)
            ).fetchone()
        return ResearchSynthesis(**dict(row)) if row else None
