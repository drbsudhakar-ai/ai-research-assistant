"""
app/ui/components/settings/api/sections/generation_section.py

LLM generation parameter UI section.

Responsible for:
- Temperature
- Top-P sampling
- Token limits
- Streaming options

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


def render_generation_section(
    state: APISettingsState,
) -> None:
    """
    Render generation settings section.
    """

    st.subheader(
        "⚙️ Generation Settings"
    )


    render_sampling_controls(
        state
    )


    st.divider()


    render_output_controls(
        state
    )


    st.divider()


    render_generation_summary(
        state
    )



# ============================================================================
# Sampling Controls
# ============================================================================


def render_sampling_controls(
    state: APISettingsState,
) -> None:
    """
    Render sampling parameters.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### Sampling Parameters"
    )


    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=float(
            config.temperature
        ),
        step=0.05,
        help=(
            "Higher values create more "
            "creative responses. "
            "Lower values improve "
            "deterministic research analysis."
        ),
    )


    top_p = st.slider(
        "Top-P",
        min_value=0.0,
        max_value=1.0,
        value=float(
            config.top_p
        ),
        step=0.05,
        help=(
            "Controls nucleus sampling."
        ),
    )


    if (
        temperature
        != config.temperature
        or top_p
        != config.top_p
    ):

        state.update_active_provider(
            {
                "temperature": temperature,
                "top_p": top_p,
            }
        )



# ============================================================================
# Output Controls
# ============================================================================


def render_output_controls(
    state: APISettingsState,
) -> None:
    """
    Render output generation settings.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### Output Configuration"
    )


    max_tokens = st.number_input(
        "Maximum Output Tokens",
        min_value=128,
        max_value=1_000_000,
        value=int(
            config.max_tokens
        ),
        step=128,
        help=(
            "Maximum generated response length."
        ),
    )


    streaming = st.toggle(
        "Enable Streaming Response",
        value=config.streaming,
        help=(
            "Display generated text "
            "progressively."
        ),
    )


    if (
        max_tokens
        != config.max_tokens
        or streaming
        != config.streaming
    ):

        state.update_active_provider(
            {
                "max_tokens": max_tokens,
                "streaming": streaming,
            }
        )



# ============================================================================
# Research Presets
# ============================================================================


def render_research_presets(
    state: APISettingsState,
) -> None:
    """
    Provide presets optimized for research analysis.
    """

    st.markdown(
        "#### Research Presets"
    )


    preset = st.selectbox(
        "Analysis Style",
        [
            "Balanced",
            "Precise",
            "Creative",
        ],
    )


    if st.button(
        "Apply Preset",
        use_container_width=True,
    ):

        if preset == "Precise":

            state.update_active_provider(
                {
                    "temperature": 0.1,
                    "top_p": 0.8,
                }
            )


        elif preset == "Creative":

            state.update_active_provider(
                {
                    "temperature": 0.8,
                    "top_p": 0.95,
                }
            )


        else:

            state.update_active_provider(
                {
                    "temperature": 0.3,
                    "top_p": 0.9,
                }
            )



# ============================================================================
# Summary
# ============================================================================


def render_generation_summary(
    state: APISettingsState,
) -> None:
    """
    Display current generation configuration.
    """

    config = (
        state.active_configuration
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        st.metric(
            "Temperature",
            f"{config.temperature:.2f}",
        )


    with col2:

        st.metric(
            "Top-P",
            f"{config.top_p:.2f}",
        )


    with col3:

        st.metric(
            "Max Tokens",
            config.max_tokens,
        )