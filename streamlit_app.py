"""
Main entry point for the AI Research Assistant application.
"""

from __future__ import annotations

import streamlit as st

from app.config.branding import get_brand_config
from app.config.loader import (
    configure_logging,
    ensure_runtime_directories,
    get_application_config,
)
from app.core.navigation import render_page
from app.core.session import initialize_session
from app.storage.database import initialize_database
from app.ui.components.sidebar import render_sidebar
from app.ui.layout.footer import render_footer
from app.ui.theme import ThemeManager


def configure_page() -> None:
    brand = get_brand_config()
    st.set_page_config(
        page_title=brand.page_title,
        page_icon=brand.icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def initialize_application() -> None:
    config = get_application_config()
    configure_logging(config)
    ensure_runtime_directories(config)
    initialize_database()
    initialize_session()
    ThemeManager.initialize()
    ThemeManager.inject()


def main() -> None:
    try:
        initialize_application()
        selected_page = render_sidebar()
        render_page(selected_page)
        render_footer()
    except Exception:  # noqa: BLE001 - keep startup errors off the UI
        st.error(
            "The application could not start. "
            "Please retry or check the application logs."
        )


configure_page()

if __name__ == "__main__":
    main()
