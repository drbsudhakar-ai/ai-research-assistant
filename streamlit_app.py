"""
===============================================================================
Project      : AI Research Assistant
File         : streamlit_app.py
Version      : 1.0.1
Author       : Dr. B. Sudhakar

Description:
Main entry point for the AI Research Assistant application.

Responsibilities:
    - Configure the Streamlit page
    - Initialize application session state
    - Render the sidebar navigation
    - Route to the selected page

Notes:
    - Business logic must not be implemented in this file.
    - This module acts as the application's bootstrapper.
===============================================================================
"""
from __future__ import annotations

import streamlit as st

from app.core.navigation import render_page
from app.core.session import initialize_session
from app.ui.components.sidebar import render_sidebar
from app.storage.database import initialize_database


# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------

def configure_page() -> None:
    """
    Configure Streamlit page settings.

    This function must be called before rendering any Streamlit UI elements.
    """

    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

configure_page()

def main() -> None:
    """
    Application entry point.
    """

    # -------------------------------------------------------------------------
    # Infrastructure
    # -------------------------------------------------------------------------
    initialize_database()

    # -------------------------------------------------------------------------
    # Session
    # -------------------------------------------------------------------------
    initialize_session()

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------
    selected_page = render_sidebar()
    render_page(selected_page)
    
if __name__ == "__main__":
    main()
