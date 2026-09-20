"""
===============================================================================
Project      : AI Research Assistant
File         : database.py
Version      : 1.1.0
Author       : Dr. B. Sudhakar

Description:
SQLite database infrastructure.

The database path comes from ApplicationConfig. DATABASE_PATH remains the
default location for compatibility with existing imports.
===============================================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

__all__ = [
    "DATABASE_PATH",
    "get_connection",
    "get_database_path",
    "initialize_database",
]

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIRECTORY = PROJECT_ROOT / "data"

DATABASE_PATH = DATA_DIRECTORY / "history.db"

CREATE_ANALYSIS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS analysis_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    filename TEXT NOT NULL,

    input_source TEXT NOT NULL,

    analysis_type TEXT NOT NULL,

    total_pages INTEGER NOT NULL,

    total_characters INTEGER NOT NULL,

    analysis TEXT NOT NULL,

    research_gap TEXT NOT NULL DEFAULT '',

    future_scope TEXT NOT NULL DEFAULT '',

    provider TEXT NOT NULL,

    model TEXT NOT NULL,

    execution_time REAL NOT NULL,

    created_at TEXT NOT NULL
);
"""

CREATE_RESEARCH_PROJECT_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS research_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    research_domain TEXT NOT NULL DEFAULT '',
    objective TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS research_project_papers (
    project_id INTEGER NOT NULL,
    analysis_id INTEGER NOT NULL,
    added_at TEXT NOT NULL,
    PRIMARY KEY (project_id, analysis_id),
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (analysis_id) REFERENCES analysis_history(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS research_syntheses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    synthesis TEXT NOT NULL,
    consolidated_gap TEXT NOT NULL DEFAULT '',
    future_scope TEXT NOT NULL DEFAULT '',
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS research_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    synthesis_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    proposal_type TEXT NOT NULL DEFAULT 'Research Project',
    content TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (project_id, version),
    FOREIGN KEY (project_id) REFERENCES research_projects(id) ON DELETE CASCADE,
    FOREIGN KEY (synthesis_id) REFERENCES research_syntheses(id) ON DELETE CASCADE
);
"""


def get_database_path() -> Path:
    """Return the configured SQLite path."""

    from app.config.loader import get_application_config

    return get_application_config().database.path


def get_connection(database_path: Path | None = None) -> sqlite3.Connection:
    """
    Create and return a configured SQLite connection.
    """

    path = Path(database_path) if database_path is not None else get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize_database(database_path: Path | None = None) -> None:
    """Create required tables if they do not already exist."""

    with get_connection(database_path) as connection:
        connection.execute(CREATE_ANALYSIS_TABLE_SQL)
        connection.executescript(CREATE_RESEARCH_PROJECT_TABLES_SQL)
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(analysis_history)")
        }
        if "research_gap" not in columns:
            connection.execute(
                "ALTER TABLE analysis_history "
                "ADD COLUMN research_gap TEXT NOT NULL DEFAULT ''"
            )
        if "future_scope" not in columns:
            connection.execute(
                "ALTER TABLE analysis_history "
                "ADD COLUMN future_scope TEXT NOT NULL DEFAULT ''"
            )

        # Backfill reusable insights for reports created before these fields
        # existed. New analyses receive the values directly from AnalysisResult.
        from app.utils.research_insights import extract_research_insights

        legacy_rows = connection.execute(
            "SELECT id, analysis FROM analysis_history "
            "WHERE research_gap = '' OR future_scope = ''"
        ).fetchall()
        for row in legacy_rows:
            research_gap, future_scope = extract_research_insights(row["analysis"])
            connection.execute(
                "UPDATE analysis_history SET research_gap = ?, future_scope = ? "
                "WHERE id = ?",
                (research_gap, future_scope, row["id"]),
            )
        connection.commit()
