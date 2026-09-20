"""
app/ui/components/settings/api/sections/provider_section.py

Provider selection UI section.

Responsible for:
- Provider list rendering
- Active provider selection
- Enable/disable provider
- Provider status display

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

import streamlit as st

from app.settings.api import (
    APIProvider,
    get_provider_metadata,
)

from ..state.api_settings_state import (
    APISettingsState,
)


# ============================================================================
# Main Renderer
# ============================================================================


def render_provider_section(
    state: APISettingsState,
) -> None:
    """
    Render provider configuration section.
    """

    st.subheader(
        "🤖 AI Provider"
    )


    render_provider_selector(
        state
    )


    st.divider()


    render_provider_details(
        state
    )



# ============================================================================
# Provider Selector
# ============================================================================


def render_provider_selector(
    state: APISettingsState,
) -> None:
    """
    Render provider selection dropdown.
    """

    providers = list(
        state.settings.providers.keys()
    )


    selected_provider = st.selectbox(
        "Active Provider",
        providers,
        index=providers.index(
            state.active_provider
        ),
        format_func=lambda provider:
            provider.value.upper(),
    )


    if (
        selected_provider
        != state.active_provider
    ):

        state.set_active_provider(
            selected_provider
        )



# ============================================================================
# Provider Details
# ============================================================================


def render_provider_details(
    state: APISettingsState,
) -> None:
    """
    Display selected provider details.
    """

    provider = (
        state.active_provider
    )


    config = (
        state.active_configuration
    )


    metadata = (
        get_provider_metadata(
            provider
        )
    )


    st.markdown(
        f"### {metadata.display_name}"
    )


    if metadata.description:

        st.caption(
            metadata.description
        )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        enabled = st.toggle(
            "Enabled",
            value=config.enabled,
        )


        if enabled != config.enabled:

            if enabled:

                state.enable_provider(
                    provider
                )

            else:

                state.disable_provider(
                    provider
                )



    with col2:

        st.metric(
            "Model",
            config.model,
        )


    with col3:

        status = (
            "Ready"
            if config.enabled
            else "Disabled"
        )

        st.metric(
            "Status",
            status,
        )



# ============================================================================
# Provider Card
# ============================================================================


def render_provider_card(
    provider: APIProvider,
    state: APISettingsState,
) -> None:
    """
    Render compact provider card.

    Used later for dashboard-style layouts.
    """

    config = (
        state.get_provider(provider)
    )


    with st.container():

        st.markdown(
            f"#### {provider.value}"
        )


        st.write(
            config.model
        )


        st.write(
            "Enabled"
            if config.enabled
            else "Disabled"
        )