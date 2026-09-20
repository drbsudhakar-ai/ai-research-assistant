"""
app/ui/components/settings/api/components/save_actions.py

Reusable settings action controls.

Provides:
- Save changes
- Discard changes
- Reset defaults
- Validation handling
- User feedback

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


def render_save_actions(
    state: APISettingsState,
) -> None:
    """
    Render settings action buttons.

    Parameters
    ----------
    state:
        API settings state.
    """

    st.subheader(
        "💾 Actions"
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        render_save_button(
            state
        )


    with col2:

        render_discard_button(
            state
        )


    with col3:

        render_reset_button(
            state
        )



# ============================================================================
# Save Button
# ============================================================================


def render_save_button(
    state: APISettingsState,
) -> None:
    """
    Render save button.
    """

    if st.button(
        "💾 Save Changes",
        disabled=(
            not state.has_changes()
        ),
        use_container_width=True,
    ):

        save_configuration(
            state
        )



# ============================================================================
# Discard Button
# ============================================================================


def render_discard_button(
    state: APISettingsState,
) -> None:
    """
    Render discard button.
    """

    if st.button(
        "↩️ Discard",
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



# ============================================================================
# Reset Button
# ============================================================================


def render_reset_button(
    state: APISettingsState,
) -> None:
    """
    Render reset button.
    """

    if st.button(
        "♻️ Reset Defaults",
        use_container_width=True,
    ):

        state.reset_to_defaults()


        st.warning(
            "Defaults restored. "
            "Save to apply."
        )



# ============================================================================
# Save Handler
# ============================================================================


def save_configuration(
    state: APISettingsState,
) -> None:
    """
    Validate and save configuration.
    """

    validation = (
        state.validate()
    )


    if validation.has_errors:

        st.error(
            "Cannot save configuration."
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
            "Settings saved successfully."
        )


        st.rerun()


    else:

        st.error(
            "Unable to save settings."
        )



# ============================================================================
# Change Indicator
# ============================================================================


def render_change_indicator(
    state: APISettingsState,
) -> None:
    """
    Display unsaved change status.
    """

    if state.has_changes():

        st.warning(
            "⚠️ Unsaved changes"
        )

    else:

        st.caption(
            "✅ All changes saved"
        )



# ============================================================================
# Exports
# ============================================================================


__all__ = [
    "render_save_actions",
    "render_change_indicator",
]