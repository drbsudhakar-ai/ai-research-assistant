"""
AI Research Assistant
Pipeline Settings - Stage Toggle Component

Reusable toggle component for pipeline stages.

Used for:
    - PDF Validation
    - Text Preparation
    - AI Paper Analysis
    - History Storage

Responsibilities:
    - Render consistent stage toggle UI
    - Display metadata
    - Handle state updates

No business logic.
No pipeline execution.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import PipelineStageType

from ..metadata import (
    PIPELINE_STAGE_METADATA,
)


class StageToggle:
    """
    Reusable pipeline stage toggle component.
    """


    def __init__(
        self,
        stage: PipelineStageType,
        enabled: bool,
        on_change=None,
    ) -> None:
        """
        Initialize stage toggle.

        Args:
            stage:
                Pipeline stage enum.

            enabled:
                Current enabled state.

            on_change:
                Optional callback receiving
                updated boolean value.
        """

        self.stage = stage
        self.enabled = enabled
        self.on_change = on_change


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> bool:
        """
        Render toggle component.

        Returns:
            Updated enabled state.
        """

        metadata = (
            PIPELINE_STAGE_METADATA[
                self.stage
            ]
        )


        st.markdown(
            f"#### {metadata.icon} "
            f"{metadata.label}"
        )


        updated = st.toggle(
            label=(
                f"Enable {metadata.label}"
            ),
            value=self.enabled,
            key=(
                f"stage_toggle_"
                f"{self.stage.value}"
            ),
            help=metadata.help_text,
        )


        st.caption(
            metadata.description
        )


        if (
            updated != self.enabled
            and self.on_change
        ):
            self.on_change(
                updated
            )


        return updated


__all__ = [
    "StageToggle",
]