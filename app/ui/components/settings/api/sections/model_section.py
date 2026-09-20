"""
app/ui/components/settings/api/sections/model_section.py

Model configuration UI section.

Responsible for:
- Model selection
- Model discovery settings
- Context configuration
- Model metadata display

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


def render_model_section(
    state: APISettingsState,
) -> None:
    """
    Render model configuration section.
    """

    st.subheader(
        "🧠 Model Configuration"
    )


    render_model_selector(
        state
    )


    st.divider()


    render_model_options(
        state
    )



# ============================================================================
# Model Selector
# ============================================================================


def render_model_selector(
    state: APISettingsState,
) -> None:
    """
    Render model selection controls.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### Available Model"
    )


    model = st.text_input(
        "Model Name",
        value=config.model,
        placeholder=(
            "Enter model identifier"
        ),
        help=(
            "Example: qwen3:4b, "
            "gpt-4.1-mini, gemini-pro"
        ),
    )


    if model != config.model:

        state.update_active_provider(
            {
                "model": model,
            }
        )



# ============================================================================
# Model Discovery
# ============================================================================


def render_model_discovery(
    state: APISettingsState,
) -> None:
    """
    Render automatic model discovery option.
    """

    config = (
        state.active_configuration
    )


    discover = st.checkbox(
        "Auto discover available models",
        value=(
            config.auto_discover_models
        ),
    )


    if (
        discover
        != config.auto_discover_models
    ):

        state.update_active_provider(
            {
                "auto_discover_models": discover,
            }
        )



# ============================================================================
# Model Options
# ============================================================================


def render_model_options(
    state: APISettingsState,
) -> None:
    """
    Render additional model options.
    """

    config = (
        state.active_configuration
    )


    st.markdown(
        "#### Model Options"
    )


    render_model_discovery(
        state
    )


    context_info = st.text_input(
        "Context Information",
        value=(
            str(
                getattr(
                    config,
                    "context_length",
                    "",
                )
            )
        ),
        placeholder=(
            "Optional context size"
        ),
        help=(
            "Maximum context window "
            "supported by model"
        ),
    )


    if context_info:

        try:

            context_length = int(
                context_info
            )


            if hasattr(
                config,
                "context_length",
            ):

                if (
                    context_length
                    != config.context_length
                ):

                    state.update_active_provider(
                        {
                            "context_length":
                            context_length
                        }
                    )


        except ValueError:

            st.warning(
                "Context length must be numeric."
            )



# ============================================================================
# Model Summary
# ============================================================================


def render_model_summary(
    state: APISettingsState,
) -> None:
    """
    Display selected model summary.
    """

    config = (
        state.active_configuration
    )


    col1, col2 = st.columns(
        2
    )


    with col1:

        st.metric(
            "Current Model",
            config.model,
        )


    with col2:

        st.metric(
            "Streaming",
            (
                "Enabled"
                if config.streaming
                else "Disabled"
            ),
        )