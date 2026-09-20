"""
AI Research Assistant
Pipeline Settings - Processing Section

Responsible for rendering pipeline processing behaviour.

Controls:
    - Execution mode
    - Analysis mode
    - LLM processing mode
    - Retry policy
    - Progress display
    - Cancellation behaviour

No business logic.
State is managed by PipelineSettingsState.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import (
    PipelineExecutionMode,
    AnalysisMode,
    ProgressDisplayMode,
    RetryPolicy,
    LLMProcessingMode,
    CancellationMode,
)

from ..metadata import (
    PIPELINE_EXECUTION_METADATA,
    ANALYSIS_MODE_METADATA,
    PROGRESS_DISPLAY_METADATA,
    RETRY_POLICY_METADATA,
    LLM_PROCESSING_METADATA,
    CANCELLATION_METADATA,
)

from ..state import PipelineSettingsState


class ProcessingSection:
    """
    Pipeline processing configuration section.
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
        Render processing settings.
        """

        st.subheader(
            "⚙️ Processing Behaviour"
        )

        st.caption(
            "Configure execution strategy, "
            "AI processing, and runtime behaviour."
        )


        self._render_execution_mode()

        st.divider()

        self._render_analysis_mode()

        st.divider()

        self._render_llm_mode()

        st.divider()

        self._render_retry_policy()

        st.divider()

        self._render_progress_mode()

        st.divider()

        self._render_cancellation()


    # ========================================================
    # Execution Mode
    # ========================================================

    def _render_execution_mode(self) -> None:
        """
        Render pipeline execution mode.
        """

        st.markdown(
            "### Pipeline Execution"
        )


        options = list(
            PipelineExecutionMode
        )


        selected = st.radio(
            label="Execution Strategy",
            options=options,
            index=options.index(
                self.state.execution_mode
            ),
            format_func=self._format_execution,
            horizontal=True,
        )


        if selected != self.state.execution_mode:

            self.state.update(
                "execution_mode",
                selected,
            )


    # ========================================================
    # Analysis Mode
    # ========================================================

    def _render_analysis_mode(self) -> None:
        """
        Render analysis depth selector.
        """

        st.markdown(
            "### Analysis Mode"
        )


        options = list(
            AnalysisMode
        )


        selected = st.selectbox(
            label="Processing Depth",
            options=options,
            index=options.index(
                self.state.analysis_mode
            ),
            format_func=self._format_analysis,
        )


        if selected != self.state.analysis_mode:

            self.state.update(
                "analysis_mode",
                selected,
            )


    # ========================================================
    # LLM Mode
    # ========================================================

    def _render_llm_mode(self) -> None:
        """
        Render LLM processing mode.
        """

        st.markdown(
            "### AI Provider Strategy"
        )


        options = list(
            LLMProcessingMode
        )


        selected = st.radio(
            label="LLM Processing",
            options=options,
            index=options.index(
                self.state.llm_processing_mode
            ),
            format_func=self._format_llm,
            horizontal=True,
        )


        if selected != self.state.llm_processing_mode:

            self.state.update(
                "llm_processing_mode",
                selected,
            )


    # ========================================================
    # Retry Policy
    # ========================================================

    def _render_retry_policy(self) -> None:
        """
        Render retry configuration.
        """

        st.markdown(
            "### Error Recovery"
        )


        options = list(
            RetryPolicy
        )


        selected = st.selectbox(
            label="Retry Policy",
            options=options,
            index=options.index(
                self.state.retry_policy
            ),
            format_func=self._format_retry,
        )


        if selected != self.state.retry_policy:

            self.state.update(
                "retry_policy",
                selected,
            )


        retry_count = st.number_input(
            label="Maximum Retry Count",
            min_value=0,
            max_value=10,
            value=self.state.retry_count,
            step=1,
        )


        if retry_count != self.state.retry_count:

            self.state.update(
                "retry_count",
                retry_count,
            )


    # ========================================================
    # Progress
    # ========================================================

    def _render_progress_mode(self) -> None:
        """
        Render progress display settings.
        """

        st.markdown(
            "### Progress Display"
        )


        options = list(
            ProgressDisplayMode
        )


        selected = st.selectbox(
            label="Progress View",
            options=options,
            index=options.index(
                self.state.progress_display_mode
            ),
            format_func=self._format_progress,
        )


        if selected != self.state.progress_display_mode:

            self.state.update(
                "progress_display_mode",
                selected,
            )


    # ========================================================
    # Cancellation
    # ========================================================

    def _render_cancellation(self) -> None:
        """
        Render cancellation option.
        """

        st.markdown(
            "### Cancellation"
        )


        options = list(
            CancellationMode
        )


        selected = st.radio(
            label="Pipeline Stop Control",
            options=options,
            index=options.index(
                self.state.cancellation_mode
            ),
            format_func=self._format_cancellation,
            horizontal=True,
        )


        if selected != self.state.cancellation_mode:

            self.state.update(
                "cancellation_mode",
                selected,
            )


    # ========================================================
    # Formatters
    # ========================================================

    @staticmethod
    def _format_execution(
        item: PipelineExecutionMode,
    ) -> str:

        metadata = (
            PIPELINE_EXECUTION_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _format_analysis(
        item: AnalysisMode,
    ) -> str:

        metadata = (
            ANALYSIS_MODE_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _format_llm(
        item: LLMProcessingMode,
    ) -> str:

        metadata = (
            LLM_PROCESSING_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _format_retry(
        item: RetryPolicy,
    ) -> str:

        metadata = (
            RETRY_POLICY_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _format_progress(
        item: ProgressDisplayMode,
    ) -> str:

        metadata = (
            PROGRESS_DISPLAY_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _format_cancellation(
        item: CancellationMode,
    ) -> str:

        metadata = (
            CANCELLATION_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


__all__ = [
    "ProcessingSection",
]