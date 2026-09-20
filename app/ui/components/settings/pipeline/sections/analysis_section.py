"""
AI Research Assistant
Pipeline Settings - Analysis Section

Responsible for rendering research pipeline stage configuration.

Controls:
    - PDF validation stage
    - Text preparation stage
    - AI analysis stage
    - History storage stage
    - Research quality analysis options

Maps to:

    ValidatePdfStep
    PreparePaperStep
    AnalyzePaperStep
    SaveHistoryStep

No business logic.
State is managed by PipelineSettingsState.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import PipelineStageType

from ..metadata import (
    PIPELINE_STAGE_METADATA,
)

from ..state import PipelineSettingsState


class AnalysisSection:
    """
    Research analysis pipeline configuration section.
    """


    def __init__(
        self,
        state: PipelineSettingsState,
    ) -> None:
        """
        Initialize section.

        Args:
            state:
                Pipeline settings state.
        """

        self.state = state


    # ========================================================
    # Render
    # ========================================================

    def render(self) -> None:
        """
        Render analysis settings section.
        """

        st.subheader(
            "🔬 Research Analysis Pipeline"
        )

        st.caption(
            "Configure the stages executed during paper analysis."
        )


        self._render_pipeline_stages()

        st.divider()

        self._render_research_quality()


    # ========================================================
    # Pipeline Stages
    # ========================================================

    def _render_pipeline_stages(self) -> None:
        """
        Render pipeline stage toggles.
        """

        st.markdown(
            "### Pipeline Stages"
        )


        for stage in PipelineStageType:

            metadata = (
                PIPELINE_STAGE_METADATA[stage]
            )


            current_value = (
                self.state.enabled_stages.get(
                    stage,
                    False,
                )
            )


            enabled = st.toggle(
                label=(
                    f"{metadata.icon} "
                    f"{metadata.label}"
                ),
                value=current_value,
                help=metadata.help_text,
                key=f"pipeline_stage_{stage.value}",
            )


            if enabled != current_value:

                updated_stages = (
                    self.state.enabled_stages.copy()
                )

                updated_stages[stage] = enabled


                self.state.update(
                    "enabled_stages",
                    updated_stages,
                )


            st.caption(
                metadata.description
            )


    # ========================================================
    # Research Quality
    # ========================================================

    def _render_research_quality(self) -> None:
        """
        Render research quality analysis options.
        """

        st.markdown(
            "### Research Quality Analysis"
        )

        st.caption(
            "Select academic analysis sections "
            "included in generated reports."
        )


        options = [

            (
                "include_research_gap",
                "Research Gap Identification",
                "Find missing problems and research opportunities.",
                "🎯",
            ),

            (
                "include_methodology_analysis",
                "Methodology Analysis",
                "Analyze research design and methodology.",
                "🧪",
            ),

            (
                "include_limitations",
                "Limitations Analysis",
                "Identify weaknesses and constraints.",
                "⚠️",
            ),

            (
                "include_future_work",
                "Future Work Suggestions",
                "Extract possible future research directions.",
                "🚀",
            ),

            (
                "include_citation_analysis",
                "Citation Analysis",
                "Analyze citation relevance and impact.",
                "📚",
            ),
        ]


        for (
            key,
            label,
            description,
            icon,
        ) in options:


            current_value = getattr(
                self.state,
                key,
            )


            enabled = st.toggle(
                label=(
                    f"{icon} {label}"
                ),
                value=current_value,
                help=description,
                key=f"research_{key}",
            )


            if enabled != current_value:

                self.state.update(
                    key,
                    enabled,
                )


__all__ = [
    "AnalysisSection",
]