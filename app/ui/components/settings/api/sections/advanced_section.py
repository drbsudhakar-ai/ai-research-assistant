"""
app/ui/components/settings/api/sections/advanced_section.py

Advanced API configuration UI section.

Responsible for:
- Retry configuration
- SSL settings
- Request limits
- Debug options

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


def render_advanced_section(
    state: APISettingsState,
) -> None:
    """
    Render advanced API settings.
    """

    st.subheader(
        "🔧 Advanced Settings"
    )


    render_retry_settings(
        state
    )


    st.divider()


    render_security_settings(
        state
    )


    st.divider()


    render_performance_settings(
        state
    )


    st.divider()


    render_debug_settings(
        state
    )



# ============================================================================
# Retry Settings
# ============================================================================


def render_retry_settings(
    state: APISettingsState,
) -> None:
    """
    Render retry policy controls.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### 🔄 Retry Policy"
    )


    max_retries = st.number_input(
        "Maximum Retries",
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
        max_retries
        != config.max_retries
        or retry_delay
        != config.retry_delay
    ):

        state.update_active_provider(
            {
                "max_retries": max_retries,
                "retry_delay": retry_delay,
            }
        )



# ============================================================================
# Security Settings
# ============================================================================


def render_security_settings(
    state: APISettingsState,
) -> None:
    """
    Render security related settings.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### 🔐 Security"
    )


    verify_ssl = st.checkbox(
        "Verify SSL Certificates",
        value=config.verify_ssl,
    )


    save_key = st.checkbox(
        "Allow API Key Storage",
        value=config.save_api_key,
    )


    if (
        verify_ssl
        != config.verify_ssl
        or save_key
        != config.save_api_key
    ):

        state.update_active_provider(
            {
                "verify_ssl": verify_ssl,
                "save_api_key": save_key,
            }
        )



# ============================================================================
# Performance Settings
# ============================================================================


def render_performance_settings(
    state: APISettingsState,
) -> None:
    """
    Render performance controls.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### 🚀 Performance"
    )


    auto_discover = st.checkbox(
        "Auto Discover Models",
        value=(
            config.auto_discover_models
        ),
    )


    requests_per_minute = st.number_input(
        "Requests Per Minute",
        min_value=1,
        max_value=10000,
        value=(
            config.requests_per_minute
        ),
        step=10,
    )


    if (
        auto_discover
        != config.auto_discover_models
        or requests_per_minute
        != config.requests_per_minute
    ):

        state.update_active_provider(
            {
                "auto_discover_models":
                    auto_discover,

                "requests_per_minute":
                    requests_per_minute,
            }
        )



# ============================================================================
# Debug Settings
# ============================================================================


def render_debug_settings(
    state: APISettingsState,
) -> None:
    """
    Render debugging controls.

    Global settings are handled separately.
    """

    st.markdown(
        "#### 🐞 Debugging"
    )


    enable_debug = st.checkbox(
        "Enable API Debug Logging",
        value=(
            state.settings
            .global_settings
            .enable_logging
        ),
    )


    if (
        enable_debug
        != state.settings
        .global_settings
        .enable_logging
    ):

        state.update_global(
            {
                "enable_logging":
                    enable_debug,
            }
        )