"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/dashboard/analysis_summary.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Dashboard analysis summary component.

    Provides:
        - Research analysis statistics
        - Execution overview
        - Pipeline health indicators
        - Recent analysis summary

Dependencies:
        - Streamlit
        - Shared UI Components
        - Theme System

===============================================================================
"""


from __future__ import annotations

from app.ui.html_renderer import render_html

from dataclasses import dataclass
from typing import Optional


import streamlit as st



from app.ui.components.shared import (
    StatCard,
    StatValue,
    StatusBadge,
    StatusType,
)



from app.ui.theme import (
    ThemeManager,
)



# =============================================================================
# Data Model
# =============================================================================


@dataclass(
    frozen=True,
)
class AnalysisSummaryData:
    """
    Dashboard analysis metrics.

    Attributes:
        total:
            Total analyses performed.

        completed:
            Successfully completed analyses.

        failed:
            Failed analyses.

        avg_time:
            Average processing time.

        last_status:
            Latest pipeline status.
    """

    total: int

    completed: int

    failed: int

    avg_time: float

    last_status: str = "unknown"



# =============================================================================
# Analysis Summary Component
# =============================================================================


class AnalysisSummary:
    """
    Render dashboard analysis summary.

    Example:

        AnalysisSummary.render(
            AnalysisSummaryData(
                total=120,
                completed=115,
                failed=5,
                avg_time=32.5,
                last_status="completed",
            )
        )

    """



    # -------------------------------------------------------------------------
    # Main Renderer
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        data: AnalysisSummaryData,
    ) -> None:
        """
        Render analysis dashboard summary.

        Args:
            data:
                Analysis summary metrics.
        """

        ThemeManager.initialize()


        render_html("""
            <div class="section">

                <div class="section-title">
                    Analysis Overview
                </div>

                <div class="section-description">
                    Research paper processing statistics
                    and pipeline performance.
                </div>

            </div>
            """)


        StatCard.render_group(

            [

                StatValue(

                    label="Total Analyses",

                    value=str(
                        data.total
                    ),

                    description=
                        "Research papers processed",

                    trend="positive",

                    icon="📄",

                ),



                StatValue(

                    label="Completed",

                    value=str(
                        data.completed
                    ),

                    description=
                        "Successful runs",

                    trend="positive",

                    icon="✅",

                ),



                StatValue(

                    label="Failed",

                    value=str(
                        data.failed
                    ),

                    description=
                        "Requires attention",

                    trend=(
                        "negative"
                        if data.failed > 0
                        else "neutral"
                    ),

                    icon="⚠️",

                ),



                StatValue(

                    label="Avg Runtime",

                    value=
                        f"{data.avg_time:.2f}s",

                    description=
                        "Processing duration",

                    trend="neutral",

                    icon="⏱️",

                ),

            ]

        )


        st.divider()


        AnalysisSummary.render_pipeline_status(
            data.last_status
        )



    # -------------------------------------------------------------------------
    # Pipeline Status
    # -------------------------------------------------------------------------

    @staticmethod
    def render_pipeline_status(
        status: str,
    ) -> None:
        """
        Render latest pipeline state.

        Args:
            status:
                Pipeline execution status.
        """

        normalized = status.replace("_", " ").strip().title() or "Unknown"
        render_html(f"""
            <div class="ara-status-panel">
                <div>
                    <div class="ara-status-title">Latest Pipeline Status</div>
                    <div class="ara-status-copy">Most recent research-analysis execution state.</div>
                </div>
                <div class="ara-status-pill">● {normalized}</div>
            </div>
        """)



    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------

    @staticmethod
    def empty() -> None:
        """
        Render empty dashboard state.
        """

        render_html("""
            <div class="card">

                <div class="card-title">
                    No Analysis Available
                </div>


                <div class="card-content">

                    Upload a research paper to
                    start your first AI analysis.

                </div>

            </div>
            """)



    # -------------------------------------------------------------------------
    # From History Records
    # -------------------------------------------------------------------------

    @staticmethod
    def from_records(
        records: list,
    ) -> AnalysisSummaryData:
        """
        Build summary from history records.

        Compatible with:
            HistoryRepository results.

        Args:
            records:
                Analysis history records.

        Returns:
            AnalysisSummaryData
        """

        if not records:

            return AnalysisSummaryData(

                total=0,

                completed=0,

                failed=0,

                avg_time=0.0,

                last_status="unknown",

            )



        completed = 0

        failed = 0

        execution_times = []



        for record in records:


            status = getattr(
                record,
                "status",
                "completed",
            ).lower()



            if status in (
                "completed",
                "success",
            ):

                completed += 1


            elif status in (
                "failed",
                "error",
            ):

                failed += 1



            runtime = getattr(
                record,
                "execution_time",
                None,
            )


            if runtime:

                execution_times.append(
                    runtime
                )



        avg_time = (

            sum(execution_times)
            /
            len(execution_times)

            if execution_times

            else 0.0

        )



        latest_status = getattr(

            records[0],

            "status",

            "unknown",

        )



        return AnalysisSummaryData(

            total=len(records),

            completed=completed,

            failed=failed,

            avg_time=avg_time,

            last_status=latest_status,

        )
