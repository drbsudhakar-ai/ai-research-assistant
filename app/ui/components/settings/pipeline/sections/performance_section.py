"""
AI Research Assistant
Pipeline Settings - Performance Section

Responsible for rendering pipeline performance configuration.

Controls:
    - Timeout settings
    - Concurrency level
    - Parallel processing
    - Worker limits
    - Extraction optimization
    - Pipeline logging

No business logic.
State is managed by PipelineSettingsState.

Version:
    1.0.0
"""

from __future__ import annotations

import streamlit as st

from ..enums import (
    TimeoutPreset,
    ConcurrencyLevel,
)

from ..metadata import (
    TIMEOUT_METADATA,
    CONCURRENCY_METADATA,
)

from ..state import PipelineSettingsState


class PerformanceSection:
    """
    Pipeline performance configuration section.
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
        Render performance settings.
        """

        st.subheader(
            "🚀 Performance & Resources"
        )

        st.caption(
            "Tune execution speed, resource usage, "
            "and processing optimization."
        )


        self._render_timeout()

        st.divider()

        self._render_concurrency()

        st.divider()

        self._render_parallel_processing()

        st.divider()

        self._render_extraction_options()

        st.divider()

        self._render_logging_options()


    # ========================================================
    # Timeout
    # ========================================================

    def _render_timeout(self) -> None:
        """
        Render timeout configuration.
        """

        st.markdown(
            "### Execution Timeout"
        )


        options = list(
            TimeoutPreset
        )


        selected = st.selectbox(
            label="Pipeline Timeout",
            options=options,
            index=options.index(
                self.state.timeout_preset
            ),
            format_func=self._format_timeout,
        )


        if selected != self.state.timeout_preset:

            self.state.update(
                "timeout_preset",
                selected,
            )


            self.state.update(
                "timeout_seconds",
                int(selected.value),
            )


        timeout = st.number_input(
            label="Timeout Seconds",
            min_value=30,
            max_value=3600,
            value=self.state.timeout_seconds,
            step=30,
            help=(
                "Maximum allowed pipeline execution time."
            ),
        )


        if timeout != self.state.timeout_seconds:

            self.state.update(
                "timeout_seconds",
                timeout,
            )


    # ========================================================
    # Concurrency
    # ========================================================

    def _render_concurrency(self) -> None:
        """
        Render worker configuration.
        """

        st.markdown(
            "### Worker Configuration"
        )


        options = list(
            ConcurrencyLevel
        )


        selected = st.selectbox(
            label="Worker Level",
            options=options,
            index=options.index(
                self.state.concurrency_level
            ),
            format_func=self._format_concurrency,
        )


        if selected != self.state.concurrency_level:

            self.state.update(
                "concurrency_level",
                selected,
            )


            self.state.update(
                "max_workers",
                int(selected.value),
            )


        workers = st.slider(
            label="Maximum Workers",
            min_value=1,
            max_value=16,
            value=self.state.max_workers,
            step=1,
            help=(
                "Maximum parallel processing workers."
            ),
        )


        if workers != self.state.max_workers:

            self.state.update(
                "max_workers",
                workers,
            )


    # ========================================================
    # Parallel Processing
    # ========================================================

    def _render_parallel_processing(self) -> None:
        """
        Render parallel execution option.
        """

        st.markdown(
            "### Parallel Processing"
        )


        enabled = st.toggle(
            label="Enable Parallel Processing",
            value=(
                self.state.enable_parallel_processing
            ),
            help=(
                "Runs independent pipeline tasks "
                "simultaneously."
            ),
        )


        if (
            enabled
            != self.state.enable_parallel_processing
        ):

            self.state.update(
                "enable_parallel_processing",
                enabled,
            )


    # ========================================================
    # Extraction Options
    # ========================================================

    def _render_extraction_options(self) -> None:
        """
        Render extraction optimization options.
        """

        st.markdown(
            "### Document Processing"
        )


        options = [

            (
                "enable_title_extraction",
                "Title Extraction",
                "Automatically detect research paper title.",
            ),

            (
                "enable_text_preprocessing",
                "Text Preprocessing",
                "Clean extracted text before analysis.",
            ),

            (
                "enable_metadata_extraction",
                "Metadata Extraction",
                "Extract paper metadata information.",
            ),
        ]


        for (
            key,
            label,
            description,
        ) in options:

            current = getattr(
                self.state,
                key,
            )


            updated = st.toggle(
                label,
                value=current,
                help=description,
                key=f"performance_{key}",
            )


            if updated != current:

                self.state.update(
                    key,
                    updated,
                )


    # ========================================================
    # Logging
    # ========================================================

    def _render_logging_options(self) -> None:
        """
        Render debugging options.
        """

        st.markdown(
            "### Diagnostics"
        )


        logging_enabled = st.toggle(
            label="Enable Pipeline Logging",
            value=(
                self.state.enable_pipeline_logging
            ),
            help=(
                "Stores pipeline execution information."
            ),
        )


        if (
            logging_enabled
            != self.state.enable_pipeline_logging
        ):

            self.state.update(
                "enable_pipeline_logging",
                logging_enabled,
            )


        verbose = st.toggle(
            label="Verbose Error Messages",
            value=self.state.verbose_errors,
            help=(
                "Shows detailed debugging information."
            ),
        )


        if (
            verbose
            != self.state.verbose_errors
        ):

            self.state.update(
                "verbose_errors",
                verbose,
            )


    # ========================================================
    # Formatters
    # ========================================================

    @staticmethod
    def _format_timeout(
        item: TimeoutPreset,
    ) -> str:
        """
        Format timeout option.
        """

        metadata = (
            TIMEOUT_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


    @staticmethod
    def _format_concurrency(
        item: ConcurrencyLevel,
    ) -> str:
        """
        Format worker option.
        """

        metadata = (
            CONCURRENCY_METADATA[item]
        )

        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


__all__ = [
    "PerformanceSection",
]