"""
===============================================================================
Project      : AI Research Assistant
File         : session.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
Streamlit session state management.
===============================================================================
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import streamlit as st

from app.config.session_config import DEFAULT_SESSION_STATE


__all__ = [
    "initialize_session",
    "get_session_value",
    "set_session_value",
    "reset_session_value",
    "clear_session",
    "has_session_value",
    "remove_session_value",
    "is_session_initialized",
]

# =============================================================================
# Session Initialization
# =============================================================================

def initialize_session() -> None:
    """
    Initialize the Streamlit session state.

    Missing keys are populated using the configured default values while
    preserving any existing session state.
    """

    for key, value in DEFAULT_SESSION_STATE.items():
        st.session_state.setdefault(key, deepcopy(value))

# =============================================================================
# Session Access
# =============================================================================

def get_session_value(key: str) -> Any:
    """Return a session state value."""
    return st.session_state.get(key)


# =============================================================================
# Session Modification
# =============================================================================

def set_session_value(key: str, value: Any) -> None:
    """Set a session state value."""
    st.session_state[key] = value
    
def reset_session_value(key: str) -> None:
    """Reset a session state value to its default."""
    if key in DEFAULT_SESSION_STATE:
        st.session_state[key] = deepcopy(DEFAULT_SESSION_STATE[key])


# =============================================================================
# Session Inspection
# =============================================================================

def has_session_value(key: str) -> bool:
    """Return True if a session key exists."""
    return key in st.session_state

def is_session_initialized() -> bool:
    """
    Check whether the Streamlit session has been initialized.
    """
    return all(
        key in st.session_state
        for key in DEFAULT_SESSION_STATE
    )


# =============================================================================
# Session Cleanup
# =============================================================================


def remove_session_value(key: str) -> None:
    """Remove a session key if it exists."""

    st.session_state.pop(key, None)

def clear_session() -> None:
    """Clear all session state and reinitialize defaults."""
    st.session_state.clear()
    initialize_session()

