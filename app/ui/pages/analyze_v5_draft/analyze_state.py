"""
===============================================================================
Project      : AI Research Assistant
Module       : Analyze Page State Management
File         : analyze_state.py

Description:
    Centralized Streamlit session state management for the Analyze Paper page.

Responsibilities:
    - Initialize analyze page session variables
    - Provide safe state access helpers
    - Maintain state consistency across Streamlit reruns

Version:
    5.0.0
===============================================================================
"""

from __future__ import annotations

from typing import Any

import streamlit as st


# =============================================================================
# Session State Keys
# =============================================================================

PDF_FILE_KEY = "analyze_pdf_file"
PDF_PATH_KEY = "analyze_pdf_path"

PDF_RESULT_KEY = "pdf_result"
PREPARED_PAPER_KEY = "prepared_paper"

ANALYSIS_RUNNING_KEY = "analysis_running"
ANALYSIS_COMPLETED_KEY = "analysis_completed"

ANALYSIS_RESULT_KEY = "analysis_result"
ANALYSIS_ERROR_KEY = "analysis_error"

PROGRESS_MANAGER_KEY = "progress_manager"

WORKER_THREAD_KEY = "analysis_worker_thread"


# =============================================================================
# Default State Factory
# =============================================================================


def _default_state() -> dict[str, Any]:
    """
    Create default analyze page state.

    Returns:
        Dictionary containing default values.
    """

    return {

        PDF_FILE_KEY: None,

        PDF_PATH_KEY: None,


        PDF_RESULT_KEY: None,

        PREPARED_PAPER_KEY: None,


        ANALYSIS_RUNNING_KEY: False,

        ANALYSIS_COMPLETED_KEY: False,


        ANALYSIS_RESULT_KEY: None,

        ANALYSIS_ERROR_KEY: None,


        PROGRESS_MANAGER_KEY: None,

        WORKER_THREAD_KEY: None,
    }


# =============================================================================
# Initialization
# =============================================================================


def initialize_state() -> None:
    """
    Initialize Analyze page session state.

    Streamlit reruns the script frequently, therefore every
    variable must be initialized safely.
    """

    defaults = _default_state()

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value



# =============================================================================
# State Reset
# =============================================================================


def reset_analysis_state() -> None:
    """
    Reset analyze page state after completion or new upload.
    """

    defaults = _default_state()

    for key, value in defaults.items():

        st.session_state[key] = value



# =============================================================================
# Generic Helpers
# =============================================================================


def get_state(
    key: str,
    default: Any = None,
) -> Any:
    """
    Safely read session state.

    Args:
        key:
            Session state key.

        default:
            Returned when key does not exist.

    Returns:
        Stored value.
    """

    return st.session_state.get(
        key,
        default,
    )



def set_state(
    key: str,
    value: Any,
) -> None:
    """
    Update session state.

    Args:
        key:
            Session state key.

        value:
            New value.
    """

    st.session_state[key] = value



def remove_state(
    key: str,
) -> None:
    """
    Remove state variable if available.
    """

    if key in st.session_state:

        del st.session_state[key]



# =============================================================================
# Analysis Status Helpers
# =============================================================================


def is_analysis_running() -> bool:
    """
    Check whether analysis worker is active.
    """

    return bool(
        st.session_state.get(
            ANALYSIS_RUNNING_KEY,
            False,
        )
    )



def mark_analysis_started() -> None:
    """
    Mark analysis as running.
    """

    st.session_state[ANALYSIS_RUNNING_KEY] = True

    st.session_state[ANALYSIS_COMPLETED_KEY] = False

    st.session_state[ANALYSIS_ERROR_KEY] = None



def mark_analysis_completed(
    result: Any,
) -> None:
    """
    Store successful analysis result.
    """

    st.session_state[ANALYSIS_RESULT_KEY] = result

    st.session_state[ANALYSIS_RUNNING_KEY] = False

    st.session_state[ANALYSIS_COMPLETED_KEY] = True



def mark_analysis_failed(
    error: Exception | str,
) -> None:
    """
    Store failed analysis state.
    """

    st.session_state[ANALYSIS_ERROR_KEY] = str(error)

    st.session_state[ANALYSIS_RUNNING_KEY] = False

    st.session_state[ANALYSIS_COMPLETED_KEY] = False