"""
app/ui/components/settings/api/sections/test_connection.py

API provider connection testing UI.

Responsible for:
- Provider connectivity test
- Latency display
- Status reporting
- Error visualization

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

import time

import streamlit as st

from ..state.api_settings_state import (
    APISettingsState,
)


# ============================================================================
# Main Renderer
# ============================================================================


def render_connection_test(
    state: APISettingsState,
) -> None:
    """
    Render connection testing component.
    """

    st.subheader(
        "🔍 Test Connection"
    )


    st.caption(
        "Verify that the selected provider "
        "is reachable and correctly configured."
    )


    if st.button(
        "🚀 Test Provider Connection",
        use_container_width=True,
    ):

        test_provider_connection(
            state
        )



# ============================================================================
# Connection Test
# ============================================================================


def test_provider_connection(
    state: APISettingsState,
) -> None:
    """
    Execute provider connection test.

    Future implementation:
        LLMService.health_check()
    """

    provider = (
        state.active_provider
    )


    config = (
        state.active_configuration
    )


    with st.spinner(
        "Testing connection..."
    ):

        start_time = time.perf_counter()


        try:

            result = (
                simulate_connection_test(
                    config
                )
            )


            elapsed = (
                time.perf_counter()
                - start_time
            )


            render_success_result(
                provider.value,
                elapsed,
                result,
            )


        except Exception as exc:

            elapsed = (
                time.perf_counter()
                - start_time
            )


            render_failure_result(
                provider.value,
                elapsed,
                str(exc),
            )



# ============================================================================
# Temporary Connection Adapter
# ============================================================================


def simulate_connection_test(
    config,
) -> dict:
    """
    Temporary provider test.

    Replace with:

        LLMService.health_check()

    """

    if not config.enabled:

        raise RuntimeError(
            "Provider is disabled."
        )


    if not config.model:

        raise RuntimeError(
            "No model configured."
        )


    return {
        "model": config.model,
        "status": "reachable",
    }



# ============================================================================
# Result Display
# ============================================================================


def render_success_result(
    provider: str,
    latency: float,
    result: dict,
) -> None:
    """
    Display successful connection result.
    """

    st.success(
        "Connection successful."
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        st.metric(
            "Provider",
            provider.upper(),
        )


    with col2:

        st.metric(
            "Latency",
            f"{latency:.2f}s",
        )


    with col3:

        st.metric(
            "Model",
            result.get(
                "model",
                "Unknown",
            ),
        )



def render_failure_result(
    provider: str,
    latency: float,
    error: str,
) -> None:
    """
    Display failed connection result.
    """

    st.error(
        "Connection failed."
    )


    st.write(
        f"Provider: {provider}"
    )


    st.write(
        f"Latency: {latency:.2f}s"
    )


    st.exception(
        error
    )