"""
app/ui/components/settings/api/api_settings.py

Main API Settings page controller.

This module only orchestrates UI sections.

UI Sections:
    sections/

State:
    state/api_settings_state.py

Backend:
    app/settings/api/
    app/config/settings_manager.py

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

import streamlit as st


from app.settings.api import (
    APIProvider,
)


from .state.api_settings_state import (
    initialize_api_settings_state,
)


from .sections import (
    render_provider_section,
    render_connection_section,
    render_model_section,
    render_generation_section,
    render_advanced_section,
    render_connection_test,
)



# ============================================================================
# Metadata
# ============================================================================


PAGE_TITLE = (
    "API Provider Settings"
)


PAGE_ICON = (
    "🔌"
)



# ============================================================================
# Main Renderer
# ============================================================================


def render_api_settings() -> None:
    """
    Render complete API settings page.
    """

    state = (
        initialize_api_settings_state()
    )


    render_header(
        state.active_provider
    )


    render_provider_summary(
        state
    )


    st.divider()


    render_validation_status(
        state
    )


    st.divider()


    render_settings_sections(
        state
    )


    st.divider()


    render_actions(
        state
    )



# ============================================================================
# Header
# ============================================================================


def render_header(
    provider: APIProvider,
) -> None:
    """
    Render page header.
    """

    st.title(
        "🔌 API Provider Settings"
    )


    st.caption(
        f"Active Provider: "
        f"{provider.value.upper()}"
    )


# ============================================================================
# Provider Summary
# ============================================================================


def render_provider_summary(
    state,
) -> None:
    """
    Render active provider summary card.
    """

    config = (
        state.active_configuration
    )


    st.subheader(
        "📊 Provider Overview"
    )


    col1, col2, col3, col4 = st.columns(
        4
    )


    with col1:

        st.metric(
            "Provider",
            state.active_provider.value.upper(),
        )


    with col2:

        st.metric(
            "Model",
            config.model,
        )


    with col3:

        status = (
            "Active"
            if config.enabled
            else "Disabled"
        )


        st.metric(
            "Status",
            status,
        )


    with col4:

        change_status = (
            "Pending"
            if state.has_changes()
            else "Saved"
        )


        st.metric(
            "Configuration",
            change_status,
        )



# ============================================================================
# Section Orchestration
# ============================================================================


def render_settings_sections(
    state,
) -> None:
    """
    Render all modular API settings sections.
    """


    render_provider_section(
        state
    )


    st.divider()


    render_connection_section(
        state
    )


    st.divider()


    render_model_section(
        state
    )


    st.divider()


    render_generation_section(
        state
    )


    st.divider()


    render_advanced_section(
        state
    )


    st.divider()


    render_connection_test(
        state
    )



# ============================================================================
# Validation Display
# ============================================================================


def render_validation_status(
    state,
) -> None:
    """
    Display configuration validation status.
    """

    result = (
        state.validate()
    )


    if result.has_errors:

        st.error(
            "❌ Configuration errors detected."
        )


        for error in result.errors:

            st.write(
                f"- {error}"
            )


    elif result.warnings:

        st.warning(
            "⚠️ Configuration warnings."
        )


        for warning in result.warnings:

            st.write(
                f"- {warning}"
            )


    else:

        st.success(
            "✅ Configuration is valid."
        )

# ============================================================================
# Action Controls
# ============================================================================


def render_actions(
    state,
) -> None:
    """
    Render settings action controls.
    """

    st.subheader(
        "💾 Actions"
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        if st.button(
            "💾 Save Changes",
            disabled=(
                not state.has_changes()
            ),
            use_container_width=True,
        ):

            save_settings(
                state
            )



    with col2:

        if st.button(
            "↩️ Discard Changes",
            disabled=(
                not state.has_changes()
            ),
            use_container_width=True,
        ):

            state.discard()


            st.info(
                "Changes discarded."
            )


            st.rerun()



    with col3:

        if st.button(
            "♻️ Reset Defaults",
            use_container_width=True,
        ):

            state.reset_to_defaults()


            st.warning(
                "Defaults restored. "
                "Save to apply changes."
            )



# ============================================================================
# Save Handler
# ============================================================================


def save_settings(
    state,
) -> None:
    """
    Validate and save settings.
    """

    validation = (
        state.validate()
    )


    if validation.has_errors:

        st.error(
            "Cannot save invalid settings."
        )


        for error in validation.errors:

            st.write(
                f"❌ {error}"
            )


        return



    success = (
        state.save()
    )


    if success:

        st.success(
            "API settings saved successfully."
        )


        st.rerun()


    else:

        st.error(
            "Failed to save API settings."
        )



# ============================================================================
# Helper
# ============================================================================


def render_unsaved_indicator(
    state,
) -> None:
    """
    Display unsaved change indicator.
    """

    if state.has_changes():

        st.warning(
            "You have unsaved changes."
        )

    else:

        st.caption(
            "All changes saved."
        )



# ============================================================================
# Module Exports
# ============================================================================


__all__ = [
    "render_api_settings",
]