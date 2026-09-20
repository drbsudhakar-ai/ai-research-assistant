"""
app/ui/components/settings/api/components/settings_metric.py

Reusable settings metric UI component.

Provides:
- Configuration metrics
- Provider statistics
- Performance indicators
- Status summaries

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations

from typing import Optional

import streamlit as st



# ============================================================================
# Basic Metric
# ============================================================================


def render_settings_metric(
    label: str,
    value: str | int | float,
    delta: Optional[str] = None,
    help_text: Optional[str] = None,
) -> None:
    """
    Render reusable metric widget.

    Parameters
    ----------
    label:
        Metric title.

    value:
        Main metric value.

    delta:
        Optional change indicator.

    help_text:
        Optional tooltip.
    """

    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text,
    )



# ============================================================================
# Provider Metrics
# ============================================================================


def render_provider_metrics(
    state,
) -> None:
    """
    Render provider summary metrics.
    """

    config = (
        state.active_configuration
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        render_settings_metric(
            label="Provider",
            value=(
                state.active_provider
                .value
                .upper()
            ),
        )


    with col2:

        render_settings_metric(
            label="Model",
            value=(
                config.model
                or "Not configured"
            ),
        )


    with col3:

        render_settings_metric(
            label="Status",
            value=(
                "Enabled"
                if config.enabled
                else "Disabled"
            ),
        )



# ============================================================================
# Connection Metrics
# ============================================================================


def render_connection_metrics(
    latency: float | None = None,
    requests: int | None = None,
) -> None:
    """
    Render connection statistics.
    """

    columns = st.columns(
        2
    )


    with columns[0]:

        render_settings_metric(
            label="Latency",
            value=(
                f"{latency:.2f}s"
                if latency is not None
                else "-"
            ),
        )


    with columns[1]:

        render_settings_metric(
            label="Requests",
            value=(
                requests
                if requests is not None
                else "-"
            ),
        )



# ============================================================================
# Generation Metrics
# ============================================================================


def render_generation_metrics(
    config,
) -> None:
    """
    Render LLM generation metrics.
    """

    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        render_settings_metric(
            label="Temperature",
            value=(
                f"{config.temperature:.2f}"
            ),
        )


    with col2:

        render_settings_metric(
            label="Top-P",
            value=(
                f"{config.top_p:.2f}"
            ),
        )


    with col3:

        render_settings_metric(
            label="Max Tokens",
            value=(
                config.max_tokens
            ),
        )



# ============================================================================
# Configuration State
# ============================================================================


def render_configuration_status(
    state,
) -> None:
    """
    Display configuration state.
    """

    if state.has_changes():

        render_settings_metric(
            label="Configuration",
            value="Unsaved",
            delta="Pending",
        )

    else:

        render_settings_metric(
            label="Configuration",
            value="Saved",
        )



# ============================================================================
# Exports
# ============================================================================


__all__ = [
    "render_settings_metric",
    "render_provider_metrics",
    "render_connection_metrics",
    "render_generation_metrics",
    "render_configuration_status",
]