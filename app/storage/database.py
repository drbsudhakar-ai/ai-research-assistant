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

    provider TEXT NOT NULL,

    model TEXT NOT NULL,

    execution_time REAL NOT NULL,

    created_at TEXT NOT NULL
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
        connection.commit()
