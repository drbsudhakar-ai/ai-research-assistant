"""
===============================================================================
Project      : AI Research Assistant
File         : session_config.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Default Streamlit session state configuration.

Responsibilities:
    - Define all default session state variables.
    - Provide a single source of truth for session initialization.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from app.config.navigation_config import DEFAULT_PAGE

# =============================================================================
# Default Session State
# =============================================================================

DEFAULT_SESSION_STATE: dict[str, Any] = {

    # -------------------------------------------------------------------------
    # Navigation
    # -------------------------------------------------------------------------
    "current_page": DEFAULT_PAGE,

    # -------------------------------------------------------------------------
    # Paper Analysis
    # -------------------------------------------------------------------------
    "uploaded_file": None,
    "paper_text": "",
    "paper_metadata": {},
    "analysis_result": None,
    "analysis_history": [],

    # -------------------------------------------------------------------------
    # AI / LLM
    # -------------------------------------------------------------------------
    "selected_model": None,

    # -------------------------------------------------------------------------
    # User Interface
    # -------------------------------------------------------------------------
    "theme": "Light",
    "is_processing": False,

    # -------------------------------------------------------------------------
    # Error Handling
    # -------------------------------------------------------------------------
    "error_message": None,
}
