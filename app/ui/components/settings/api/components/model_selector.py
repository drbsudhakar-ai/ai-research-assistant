"""
app/ui/components/settings/api/components/model_selector.py

Reusable LLM model selector component.

Features:
- Model dropdown
- Manual model entry
- Auto discovery hook
- Current model display
- Provider independent design

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

import streamlit as st


from app.settings.api import (
    APIProvider,
)


from ..state.api_settings_state import (
    APISettingsState,
)



# ============================================================================
# Main Renderer
# ============================================================================


def render_model_selector(
    provider: APIProvider,
    state: APISettingsState,
) -> None:
    """
    Render model selector.

    Parameters
    ----------
    provider:
        Current provider.

    state:
        API settings state.
    """

    config = (
        state.get_provider(
            provider
        )
    )


    st.markdown(
        "#### 🧠 Model Selection"
    )


    available_models = (
        get_available_models(
            provider,
            state,
        )
    )


    render_model_dropdown(
        provider,
        config.model,
        available_models,
        state,
    )


    render_manual_model_input(
        provider,
        config.model,
        state,
    )



# ============================================================================
# Dropdown
# ============================================================================


def render_model_dropdown(
    provider: APIProvider,
    current_model: str,
    models: list[str],
    state: APISettingsState,
) -> None:
    """
    Render available model dropdown.
    """

    if not models:

        st.info(
            "No discovered models available."
        )

        return



    selected_model = st.selectbox(
        "Available Models",
        models,
        index=(
            models.index(
                current_model
            )
            if current_model in models
            else 0
        ),
        key=(
            f"model_select_{provider.value}"
        ),
    )


    if selected_model != current_model:

        state.update_active_provider(
            {
                "model":
                    selected_model,
            }
        )



# ============================================================================
# Manual Entry
# ============================================================================


def render_manual_model_input(
    provider: APIProvider,
    current_model: str,
    state: APISettingsState,
) -> None:
    """
    Render manual model input.
    """

    manual_model = st.text_input(
        "Custom Model Name",
        value=current_model,
        placeholder=(
            "Enter model identifier"
        ),
        key=(
            f"manual_model_{provider.value}"
        ),
    )


    if manual_model != current_model:

        state.update_active_provider(
            {
                "model":
                    manual_model,
            }
        )



# ============================================================================
# Model Discovery
# ============================================================================


def get_available_models(
    provider: APIProvider,
    state: APISettingsState,
) -> list[str]:
    """
    Return available models.

    Future integration:

        ModelRegistry
        Provider discovery API
        Ollama model list

    """

    config = (
        state.get_provider(
            provider
        )
    )


    discovered = getattr(
        config,
        "available_models",
        [],
    )


    if discovered:

        return discovered



    # Default empty list.
    # Provider discovery will populate later.

    return []



# ============================================================================
# Refresh Control
# ============================================================================


def render_refresh_models_button(
    provider: APIProvider,
    state: APISettingsState,
) -> None:
    """
    Refresh discovered models.

    Future:
        call provider model discovery service
    """

    if st.button(
        "🔄 Refresh Models",
        key=(
            f"refresh_models_{provider.value}"
        ),
    ):

        st.info(
            "Model discovery will run here."
        )



# ============================================================================
# Summary
# ============================================================================


def render_model_summary(
    provider: APIProvider,
    state: APISettingsState,
) -> None:
    """
    Display current model information.
    """

    config = (
        state.get_provider(
            provider
        )
    )


    st.metric(
        "Selected Model",
        config.model
        or "None",
    )



# ============================================================================
# Exports
# ============================================================================


__all__ = [
    "render_model_selector",
    "render_model_summary",
]