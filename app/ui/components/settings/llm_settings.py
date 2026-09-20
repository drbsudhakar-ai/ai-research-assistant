"""
app/ui/components/settings/llm_settings.py

LLM Settings UI Component

Provides configuration controls for Large Language Model
analysis behaviour in the AI Research Assistant application.

Version:
    1.0.0

Author:
    Dr B Sudhakar

Description:
    - Configure active LLM model
    - Configure generation parameters
    - Configure analysis behaviour
    - Manage token and response preferences

This component handles only UI state.
Actual configuration persistence should be handled by:

    app/config/settings_manager.py

Related configuration modules:

    app/config/provider_config.py
    app/config/model_config.py
    app/config/llm_config.py
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMPONENT_TITLE = "LLM Settings"


DEFAULT_LLM_SETTINGS: Dict[str, Any] = {
    "temperature": 0.3,
    "max_tokens": 4096,
    "context_window": 8192,
    "response_format": "Structured Report",
    "stream_response": True,
}


AVAILABLE_RESPONSE_FORMATS = [
    "Structured Report",
    "Research Summary",
    "Executive Summary",
    "Technical Analysis",
]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def _get_setting(
    key: str,
    default: Any,
) -> Any:
    """
    Retrieve LLM setting from session state.

    Args:
        key:
            Configuration key.

        default:
            Default value.

    Returns:
        Stored value or default.
    """

    return st.session_state.get(
        key,
        default,
    )


def _set_setting(
    key: str,
    value: Any,
) -> None:
    """
    Store LLM setting.

    Args:
        key:
            Configuration key.

        value:
            Configuration value.
    """

    st.session_state[key] = value


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_llm_settings() -> Dict[str, Any]:
    """
    Render LLM configuration panel.

    Returns:
        Dictionary containing updated LLM settings.
    """

    st.subheader(
        COMPONENT_TITLE
    )

    st.caption(
        "Configure AI model behaviour and response generation parameters."
    )

    settings: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Model Behaviour
    # ------------------------------------------------------------------

    st.markdown(
        "### Generation Parameters"
    )

    temperature = st.slider(
        label="Temperature",
        min_value=0.0,
        max_value=1.0,
        value=float(
            _get_setting(
                "temperature",
                DEFAULT_LLM_SETTINGS["temperature"],
            )
        ),
        step=0.05,
        help=(
            "Controls creativity. "
            "Lower values produce more deterministic responses."
        ),
    )

    settings["temperature"] = temperature

    _set_setting(
        "temperature",
        temperature,
    )


    max_tokens = st.number_input(
        label="Maximum Output Tokens",
        min_value=256,
        max_value=32768,
        value=int(
            _get_setting(
                "max_tokens",
                DEFAULT_LLM_SETTINGS["max_tokens"],
            )
        ),
        step=256,
    )

    settings["max_tokens"] = max_tokens

    _set_setting(
        "max_tokens",
        max_tokens,
    )


    context_window = st.number_input(
        label="Context Window Size",
        min_value=1024,
        max_value=131072,
        value=int(
            _get_setting(
                "context_window",
                DEFAULT_LLM_SETTINGS["context_window"],
            )
        ),
        step=1024,
    )

    settings["context_window"] = context_window

    _set_setting(
        "context_window",
        context_window,
    )


    # ------------------------------------------------------------------
    # Output Preferences
    # ------------------------------------------------------------------

    st.markdown(
        "### Output Preferences"
    )


    response_format = st.selectbox(
        label="Default Response Format",
        options=AVAILABLE_RESPONSE_FORMATS,
        index=AVAILABLE_RESPONSE_FORMATS.index(
            _get_setting(
                "response_format",
                DEFAULT_LLM_SETTINGS["response_format"],
            )
        ),
    )

    settings["response_format"] = response_format

    _set_setting(
        "response_format",
        response_format,
    )


    stream_response = st.checkbox(
        label="Enable streaming responses",
        value=bool(
            _get_setting(
                "stream_response",
                DEFAULT_LLM_SETTINGS["stream_response"],
            )
        ),
        help=(
            "Display generated analysis progressively "
            "instead of waiting for completion."
        ),
    )


    settings["stream_response"] = stream_response

    _set_setting(
        "stream_response",
        stream_response,
    )


    # ------------------------------------------------------------------
    # Information Panel
    # ------------------------------------------------------------------

    st.markdown(
        "### Current Configuration"
    )


    st.info(
        f"""
        **Temperature:** {temperature}

        **Maximum Tokens:** {max_tokens}

        **Context Window:** {context_window}

        **Response Format:** {response_format}

        **Streaming:** {"Enabled" if stream_response else "Disabled"}
        """
    )


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    st.divider()

    if st.button(
        "Reset LLM Settings",
        type="secondary",
    ):

        for key, value in DEFAULT_LLM_SETTINGS.items():

            _set_setting(
                key,
                value,
            )

        st.success(
            "LLM settings restored to defaults."
        )

        st.rerun()


    return settings



# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


__all__ = [
    "render_llm_settings",
]