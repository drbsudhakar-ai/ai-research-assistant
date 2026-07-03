"""
===============================================================================
Project      : AI Research Assistant
File         : database.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
SQLite database infrastructure.

Responsibilities:
    - Create database connections.
    - Initialize the database schema.
    - Configure SQLite settings.
    - Provide reusable database access for repositories.

Business logic must not be implemented in this module.
===============================================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

__all__ = [
    "DATABASE_PATH",
    "get_connection",
    "initialize_database",
]

# =============================================================================
# Database Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIRECTORY = PROJECT_ROOT / "data"

DATABASE_PATH = DATA_DIRECTORY / "history.db"

# =============================================================================
# SQL Schema
# =============================================================================

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

# =============================================================================
# Public API
# =============================================================================


def get_connection() -> sqlite3.Connection:
    """
    Create and return a configured SQLite connection.

    Returns
    -------
    sqlite3.Connection
        Configured database connection.
    """

    DATA_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


def initialize_database() -> None:
    """
    Initialize the SQLite database.

    Creates all required tables if they do not already exist.
    """

    with get_connection() as connection:

        connection.execute(
            CREATE_ANALYSIS_TABLE_SQL
        )

        connection.commit()