"""
===============================================================================
Project      : AI Research Assistant
Module       : Auto Refresh Utility
File         : auto_refresh.py
Version      : 1.0.0
===============================================================================
"""

from __future__ import annotations

import time

import streamlit as st


def auto_refresh(interval: float = 1.0) -> None:
    """
    Trigger Streamlit rerun while long-running analysis is active.
    """

    if not st.session_state.get(
        "analysis_running",
        False,
    ):
        return

    time.sleep(interval)

    st.rerun()