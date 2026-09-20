"""
AI Research Assistant
Pipeline Settings - Concurrency Selector Component

Reusable worker/concurrency configuration component.

Responsibilities:
    - Select worker level
    - Configure maximum workers
    - Synchronize concurrency preset and worker count

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
    ConcurrencyLevel,
)

from ..metadata import (
    CONCURRENCY_METADATA,
)


class ConcurrencySelector:
    """
    Pipeline concurrency selector component.
    """


    def __init__(
        self,
        level: ConcurrencyLevel,
        workers: int,
        on_change=None,
        key: str = "pipeline_concurrency",
    ) -> None:
        """
        Initialize concurrency selector.

        Args:
            level:
                Current concurrency level.

            workers:
                Current worker count.

            on_change:
                Callback receiving:
                    (level, workers)

            key:
                Streamlit widget key.
        """

        self.level = level

        self.workers = workers

        self.on_change = on_change

        self.key = key


    # ========================================================
    # Render
    # ========================================================

    def render(
        self,
    ) -> tuple[ConcurrencyLevel, int]:
        """
        Render concurrency selector.

        Returns:
            (
                concurrency level,
                worker count
            )
        """

        st.markdown(
            "#### ⚡ Worker Configuration"
        )


        levels = list(
            ConcurrencyLevel
        )


        selected_level = st.selectbox(
            label="Concurrency Level",
            options=levels,
            index=levels.index(
                self.level
            ),
            format_func=self._format_level,
            key=f"{self.key}_level",
        )


        default_workers = int(
            selected_level.value
        )


        selected_workers = st.slider(
            label="Maximum Workers",
            min_value=1,
            max_value=16,
            step=1,
            value=(
                self.workers
                if selected_level == self.level
                else default_workers
            ),
            help=(
                "Number of parallel workers "
                "available for processing."
            ),
            key=f"{self.key}_workers",
        )


        if self.on_change:

            if (
                selected_level != self.level
                or selected_workers != self.workers
            ):

                self.on_change(
                    selected_level,
                    selected_workers,
                )


        return (
            selected_level,
            selected_workers,
        )


    # ========================================================
    # Formatter
    # ========================================================

    @staticmethod
    def _format_level(
        level: ConcurrencyLevel,
    ) -> str:
        """
        Format concurrency option.
        """

        metadata = (
            CONCURRENCY_METADATA[
                level
            ]
        )


        return (
            f"{metadata.icon} "
            f"{metadata.label}"
        )


__all__ = [
    "ConcurrencySelector",
]