"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/dashboard/system_health.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Dashboard system health component.

    Provides:
        - AI provider status
        - Database status
        - Pipeline readiness
        - Runtime diagnostics

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
    StatusBadge,
    StatusType,
)



from app.ui.theme import (
    ThemeManager,
)



# =============================================================================
# Health Model
# =============================================================================


@dataclass(
    frozen=True,
)
class HealthStatus:
    """
    Represents system health information.

    Attributes:

        component:
            System component name.

        available:
            Component availability.

        message:
            Additional details.

        status:
            Optional status override.
    """

    component: str

    available: bool

    message: Optional[str] = None

    status: Optional[str] = None



# =============================================================================
# System Health Component
# =============================================================================


class SystemHealth:
    """
    Render dashboard system health panel.

    Example:

        SystemHealth.render(
            health_items
        )

    """



    # -------------------------------------------------------------------------
    # Main Renderer
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        items: list[HealthStatus],
    ) -> None:
        """
        Render system health dashboard.

        Args:
            items:
                Health status collection.
        """

        ThemeManager.initialize()


        render_html("""
            <div class="section">

                <div class="section-title">

                    System Health

                </div>


                <div class="section-description">

                    AI services and application readiness.

                </div>

            </div>
            """)



        if not items:

            SystemHealth.empty()

            return



        for item in items:

            SystemHealth._render_item(
                item
            )



    # -------------------------------------------------------------------------
    # Individual Health Item
    # -------------------------------------------------------------------------

    @staticmethod
    def _render_item(
        item: HealthStatus,
    ) -> None:
        """
        Render health card.

        Args:
            item:
                Health information.
        """

        col1, col2 = st.columns(
            [
                3,
                1,
            ]
        )


        with col1:

            message = (

                item.message

                if item.message

                else

                (
                    "Available"
                    if item.available
                    else
                    "Unavailable"
                )

            )


            render_html(f"""
                <div class="card">

                    <div class="card-title">

                        {item.component}

                    </div>


                    <div class="card-content">

                        {message}

                    </div>

                </div>
                """)


        with col2:

            if item.available:

                StatusBadge.render(

                    "Online",

                    StatusType.SUCCESS,

                )

            else:

                StatusBadge.render(

                    "Offline",

                    StatusType.ERROR,

                )



    # -------------------------------------------------------------------------
    # Default System Checks
    # -------------------------------------------------------------------------

    @staticmethod
    def default_checks(
        *,
        llm_available: bool = False,
        database_available: bool = False,
        pipeline_ready: bool = False,
        provider_name: str = "Ollama",
    ) -> list[HealthStatus]:
        """
        Generate standard health checks.

        Args:

            llm_available:
                LLM service status.

            database_available:
                Database status.

            pipeline_ready:
                Pipeline status.

            provider_name:
                Active AI provider.

        Returns:
            list[HealthStatus]
        """

        return [

            HealthStatus(

                component=
                    f"{provider_name} Provider",

                available=
                    llm_available,

                message=
                    (
                        "AI inference service ready."
                        if llm_available
                        else
                        "AI provider unavailable."
                    ),

            ),



            HealthStatus(

                component=
                    "History Database",

                available=
                    database_available,

                message=
                    (
                        "Storage service ready."
                        if database_available
                        else
                        "Database connection failed."
                    ),

            ),



            HealthStatus(

                component=
                    "Analysis Pipeline",

                available=
                    pipeline_ready,

                message=
                    (
                        "Pipeline ready for execution."
                        if pipeline_ready
                        else
                        "Pipeline initialization required."
                    ),

            ),

        ]



    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------

    @staticmethod
    def empty() -> None:
        """
        Render empty health state.
        """

        render_html("""
            <div class="card">

                <div class="card-title">

                    No Health Data

                </div>


                <div class="card-content">

                    System diagnostics are unavailable.

                </div>

            </div>
            """)