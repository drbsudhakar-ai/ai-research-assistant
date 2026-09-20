"""
AI Research Assistant
Pipeline Settings - Timeout Selector Component

Reusable timeout configuration component.

Responsibilities:
    - Select timeout presets
    - Allow custom timeout values
    - Synchronize timeout preset and seconds

Used by:
    PerformanceSection

No business logic.
No pipeline execution.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import (
    TimeoutPreset,
)

from ..metadata import (
    TIMEOUT_METADATA,
)


class TimeoutSelector:
    """
    Pipeline timeout selector component.
    """


    def __init__(
        self,
        preset: TimeoutPreset,
        seconds: int,
        on_change=None,
        key: str = "pipeline_timeout",
    ) -> None:
        """
        Initialize timeout selector.

        Args:
            preset:
                Current timeout preset.

            seconds:
                Current timeout seconds.

            on_change:
                Callback receiving:
                    (preset, seconds)

            key:
                Streamlit widget key.
        """

        self.preset = preset

        self.seconds = seconds

        self.on_change = on_change

        self.key = key


    # ========================================================
    # Render
    # ========================================================

    def render(
        self,
    ) -> tuple[TimeoutPreset, int]:
        """
        Render timeout selector.

        Returns:
            (
                timeout preset,
                timeout seconds
            )
        """

        st.markdown(
            "#### ⏱️ Execution Timeout"
        )


        presets = list(
            TimeoutPreset
        )


        selected_preset = st.selectbox(
            label="Timeout Preset",
            options=presets,
            index=presets.index(
                self.preset
            ),
            format_func=self._format_preset,
            key=f"{self.key}_preset",
        )


        default_seconds = int(
            selected_preset.value
        )


        selected_seconds = st.number_input(
            label="Timeout Seconds",
            min_value=30,
            max_value=3600,
            step=30,
            value=(
                self.seconds
                if selected_preset == self.preset
                else default_seconds
            ),
            help=(
                "Maximum time allowed "
                "for pipeline execution."
            ),
            key=f"{self.key}_seconds",
        )


        selected_seconds = int(
            selected_seconds
        )


        if self.on_change:

            if (
                selected_preset != self.preset
                or selected_seconds != self.seconds
            ):

                self.on_change(
                    selected_preset,
                    selected_seconds,
                )


        return (
            selected_preset,
            selected_seconds,
        )


    # ========================================================
    # Formatter
    # ========================================================

    @staticmethod
    def _format_preset(
        preset: TimeoutPreset,
    ) -> str:
        """
        Format timeout preset.
        """

        metadata = (
            TIMEOUT_METADATA[
                preset
            ]
        )


        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


__all__ = [
    "TimeoutSelector",
]