"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/dashboard/recent_activity.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Dashboard recent analysis activity component.

    Provides:
        - Recent research papers
        - Analysis status display
        - Provider/model information
        - History activity timeline

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
class ActivityItem:
    """
    Represents a recent analysis record.

    Attributes:

        title:
            Research paper title.

        status:
            Analysis status.

        created_at:
            Creation timestamp.

        provider:
            AI provider name.

        model:
            Model name.
    """

    title: str

    status: str

    created_at: str

    provider: Optional[str] = None

    model: Optional[str] = None



# =============================================================================
# Recent Activity Component
# =============================================================================


class RecentActivity:
    """
    Dashboard recent activity renderer.

    Example:

        RecentActivity.render(items)

    """



    # -------------------------------------------------------------------------
    # Main Renderer
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        items: list[ActivityItem],
        limit: int = 5,
    ) -> None:
        """
        Render recent analysis activity.

        Args:
            items:
                Activity records.

            limit:
                Maximum displayed items.
        """

        ThemeManager.initialize()


        render_html("""
            <div class="section">

                <div class="section-title">
                    Recent Analyses
                </div>

                <div class="section-description">

                    Latest processed research papers
                    and analysis status.

                </div>

            </div>
            """)



        if not items:

            RecentActivity.empty()

            return



        for item in items[:limit]:

            RecentActivity._render_item(
                item
            )



    # -------------------------------------------------------------------------
    # Single Activity Item
    # -------------------------------------------------------------------------

    @staticmethod
    def _render_item(
        item: ActivityItem,
    ) -> None:
        """
        Render single activity entry.

        Args:
            item:
                Activity information.
        """

        render_html(f"""
            <div class="card">

                <div class="card-header">

                    <div class="card-title">

                        📄 {item.title}

                    </div>

                </div>


                <div class="card-content">

                    <b>Date:</b>
                    {item.created_at}

                    <br>

                    <b>Provider:</b>
                    {item.provider or "N/A"}

                    <br>

                    <b>Model:</b>
                    {item.model or "N/A"}

                </div>

            </div>
            """)


        StatusBadge.pipeline(
            item.status
        )


        st.write("")



    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------

    @staticmethod
    def empty() -> None:
        """
        Render empty activity state.
        """

        render_html("""
            <div class="card">

                <div class="card-title">

                    No Recent Analyses

                </div>


                <div class="card-content">

                    Your processed research papers
                    will appear here.

                </div>


            </div>
            """)



    # -------------------------------------------------------------------------
    # History Conversion Helper
    # -------------------------------------------------------------------------

    @staticmethod
    def from_records(
        records: list,
    ) -> list[ActivityItem]:
        """
        Convert history records into UI models.

        Compatible with:
            AnalysisRecord objects.

        Args:
            records:
                History records.

        Returns:
            list[ActivityItem]
        """

        activities = []


        for record in records:


            activities.append(

                ActivityItem(

                    title=getattr(

                        record,

                        "title",

                        "Untitled Paper",

                    ),


                    status=getattr(

                        record,

                        "status",

                        "completed",

                    ),


                    created_at=str(

                        getattr(

                            record,

                            "created_at",

                            "",

                        )

                    ),


                    provider=getattr(

                        record,

                        "provider",

                        None,

                    ),


                    model=getattr(

                        record,

                        "model",

                        None,

                    ),

                )

            )


        return activities
