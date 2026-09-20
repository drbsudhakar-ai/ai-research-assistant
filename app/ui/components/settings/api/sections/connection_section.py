"""
app/ui/components/settings/api/sections/connection_section.py

API connection configuration UI section.

Responsible for:
- API credentials
- Endpoint configuration
- Timeout settings
- Retry settings

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..state.api_settings_state import (
    APISettingsState,
)


# ============================================================================
# Main Renderer
# ============================================================================


def render_connection_section(
    state: APISettingsState,
) -> None:
    """
    Render connection configuration section.
    """

    st.subheader(
        "🌐 Connection"
    )


    render_api_credentials(
        state
    )


    st.divider()


    render_endpoint_settings(
        state
    )


    st.divider()


    render_timeout_settings(
        state
    )



# ============================================================================
# API Credentials
# ============================================================================


def render_api_credentials(
    state: APISettingsState,
) -> None:
    """
    Render API key configuration.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### 🔑 API Credentials"
    )


    api_key = st.text_input(
        "API Key",
        value=config.api_key,
        type="password",
        placeholder=(
            "Enter provider API key"
        ),
        help=(
            "API key is stored securely "
            "when enabled."
        ),
    )


    if api_key != config.api_key:

        state.set_api_key(
            state.active_provider,
            api_key,
        )



    save_key = st.checkbox(
        "Save API key",
        value=config.save_api_key,
    )


    if save_key != config.save_api_key:

        state.update_active_provider(
            {
                "save_api_key": save_key,
            }
        )



# ============================================================================
# Endpoint Settings
# ============================================================================


def render_endpoint_settings(
    state: APISettingsState,
) -> None:
    """
    Render endpoint configuration.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### 🔗 Endpoint"
    )


    base_url = st.text_input(
        "Base URL",
        value=config.base_url,
        placeholder=(
            "https://api.provider.com"
        ),
    )


    if base_url != config.base_url:

        state.update_active_provider(
            {
                "base_url": base_url,
            }
        )



# ============================================================================
# Timeout Settings
# ============================================================================


def render_timeout_settings(
    state: APISettingsState,
) -> None:
    """
    Render timeout and retry configuration.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### ⏱ Request Settings"
    )


    col1, col2 = st.columns(
        2
    )


    with col1:

        timeout = st.number_input(
            "Timeout (seconds)",
            min_value=5,
            max_value=600,
            value=config.timeout,
            step=5,
        )


    with col2:

        retries = st.number_input(
            "Max Retries",
            min_value=0,
            max_value=10,
            value=config.max_retries,
            step=1,
        )



    retry_delay = st.number_input(
        "Retry Delay (seconds)",
        min_value=0.5,
        max_value=30.0,
        value=float(
            config.retry_delay
        ),
        step=0.5,
    )



    if (
        timeout != config.timeout
        or retries != config.max_retries
        or retry_delay != config.retry_delay
    ):

        state.update_active_provider(
            {
                "timeout": timeout,
                "max_retries": retries,
                "retry_delay": retry_delay,
            }
        )