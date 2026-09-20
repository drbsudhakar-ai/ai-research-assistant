"""
===============================================================================
Project      : AI Research Assistant
Module       : Auto Refresh UI Component
File         : auto_refresh.py
Version      : 5.0.0
===============================================================================
"""

from __future__ import annotations


import streamlit as st


from streamlit_autorefresh import (
    st_autorefresh,
)



def enable_analysis_refresh(
    running: bool,
    interval: int = 1000,
) -> None:
    """
    Enable refresh while analysis is running.

    Args:

        running:
            Current analysis status.

        interval:
            Milliseconds between reruns.
    """


    if running:


        st_autorefresh(

            interval=interval,

            key="analysis_refresh",

        )