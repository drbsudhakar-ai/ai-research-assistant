"""
app/ui/components/settings/api/components/provider_card.py

Reusable provider card UI component.

Displays:
- Provider name
- Provider status
- Active model
- Endpoint
- Configuration state

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
# Provider Card Renderer
# ============================================================================


def render_provider_card(
    provider: APIProvider,
    state: APISettingsState,
    compact: bool = False,
) -> None:
    """
    Render provider information card.

    Parameters
    ----------
    provider:
        Provider enum.

    state:
        API settings UI state.

    compact:
        Render compact version.
    """

    config = (
        state.get_provider(
            provider
        )
    )


    is_active = (
        provider
        == state.active_provider
    )


    with st.container(
        border=True,
    ):

        render_header(
            provider,
            is_active,
        )


        if compact:

            render_compact_body(
                config
            )

        else:

            render_full_body(
                config
            )



# ============================================================================
# Card Header
# ============================================================================


def render_header(
    provider: APIProvider,
    active: bool,
) -> None:
    """
    Render card title.
    """

    title = (
        "🟢 "
        if active
        else ""
    )


    st.markdown(
        f"### {title}{provider.value.upper()}"
    )



# ============================================================================
# Full Card Body
# ============================================================================


def render_full_body(
    config,
) -> None:
    """
    Render detailed provider information.
    """

    col1, col2 = st.columns(
        2
    )


    with col1:

        st.write(
            "Model"
        )

        st.info(
            config.model
            if config.model
            else "Not configured"
        )


    with col2:

        st.write(
            "Status"
        )


        if config.enabled:

            st.success(
                "Enabled"
            )

        else:

            st.warning(
                "Disabled"
            )


    st.write(
        "Endpoint"
    )


    st.code(
        config.base_url
        or "Local provider",
    )



# ============================================================================
# Compact Card Body
# ============================================================================


def render_compact_body(
    config,
) -> None:
    """
    Render compact provider summary.
    """

    st.write(
        config.model
        or "No model"
    )


    status = (
        "Ready"
        if config.enabled
        else "Disabled"
    )


    st.caption(
        status
    )



# ============================================================================
# Provider Grid
# ============================================================================


def render_provider_grid(
    state: APISettingsState,
) -> None:
    """
    Render all providers as cards.
    """

    providers = list(
        state.settings.providers.keys()
    )


    columns = st.columns(
        3
    )


    for index, provider in enumerate(
        providers
    ):

        with columns[index % 3]:

            render_provider_card(
                provider,
                state,
                compact=True,
            )