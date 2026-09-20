"""
app/ui/components/settings/api/components/api_key_input.py

Reusable secure API key input component.

Features:
- Masked input
- Show/hide key
- Empty key validation
- Save key option
- Environment key support hook

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


def render_api_key_input(
    provider: APIProvider,
    state: APISettingsState,
) -> None:
    """
    Render secure API key input.

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
        "#### 🔑 API Key"
    )


    key_value = (
        config.api_key
    )


    col1, col2 = st.columns(
        [4, 1]
    )


    with col1:

        api_key = render_key_field(
            key_value
        )


    with col2:

        show_key = st.checkbox(
            "Show",
            key=(
                f"show_key_{provider.value}"
            ),
        )



    if show_key:

        api_key = st.text_input(
            "Visible API Key",
            value=key_value,
        )



    if api_key != key_value:

        state.set_api_key(
            provider,
            api_key,
        )



    render_key_status(
        api_key
    )



# ============================================================================
# Input Field
# ============================================================================


def render_key_field(
    value: str,
) -> str:
    """
    Render masked key input.
    """

    return st.text_input(
        "API Key",
        value=value,
        type="password",
        placeholder=(
            "Enter API key"
        ),
        label_visibility="collapsed",
    )



# ============================================================================
# Status Display
# ============================================================================


def render_key_status(
    api_key: str,
) -> None:
    """
    Display key configuration status.
    """

    if not api_key:

        st.warning(
            "No API key configured."
        )

        return



    if len(api_key) < 8:

        st.error(
            "API key appears invalid."
        )

        return



    masked = mask_key(
        api_key
    )


    st.success(
        f"API key configured: {masked}"
    )



# ============================================================================
# Masking Utility
# ============================================================================


def mask_key(
    api_key: str,
) -> str:
    """
    Hide API key characters.
    """

    if len(api_key) <= 8:

        return "********"


    return (
        api_key[:4]
        +
        "****"
        +
        api_key[-4:]
    )



# ============================================================================
# Environment Variable Hook
# ============================================================================


def render_environment_hint() -> None:
    """
    Display environment variable guidance.
    """

    st.caption(
        "You can also configure API keys "
        "using environment variables."
    )



# ============================================================================
# Exports
# ============================================================================


__all__ = [
    "render_api_key_input",
    "mask_key",
]