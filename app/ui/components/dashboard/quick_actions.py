"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/dashboard/quick_actions.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Dashboard quick actions component.

    Provides:
        - Navigation shortcuts
        - Common research workflow actions
        - Dashboard command center

Dependencies:
        - Streamlit
        - Theme System

===============================================================================
"""


from __future__ import annotations

from app.ui.html_renderer import render_html

from dataclasses import dataclass
from typing import Callable, Optional


import streamlit as st



from app.ui.theme import (
    ThemeManager,
)



# =============================================================================
# Action Model
# =============================================================================


@dataclass(
    frozen=True,
)
class QuickAction:
    """
    Represents a dashboard action.

    Attributes:

        title:
            Action display title.

        description:
            Supporting text.

        icon:
            Visual icon.

        callback:
            Function executed on click.
    """

    title: str

    description: str

    icon: str

    callback: Optional[Callable[[], None]] = None



# =============================================================================
# Quick Actions Component
# =============================================================================


class QuickActions:
    """
    Render dashboard quick action cards.

    Example:

        QuickActions.render(
            actions
        )

    """



    # -------------------------------------------------------------------------
    # Main Renderer
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        actions: list[QuickAction],
    ) -> None:
        """
        Render quick action cards.

        Args:
            actions:
                Available actions.
        """

        ThemeManager.initialize()


        render_html("""
            <div class="section">

                <div class="section-title">

                    Quick Actions

                </div>


                <div class="section-description">

                    Frequently used research workflows.

                </div>

            </div>
            """)



        if not actions:

            QuickActions.empty()

            return



        columns = st.columns(
            min(
                len(actions),
                4,
            )
        )


        for index, action in enumerate(actions):

            with columns[index % len(columns)]:

                QuickActions._render_action(
                    action
                )



    # -------------------------------------------------------------------------
    # Action Card Renderer
    # -------------------------------------------------------------------------

    @staticmethod
    def _render_action(
        action: QuickAction,
    ) -> None:
        """
        Render single action.

        Args:
            action:
                Action definition.
        """

        render_html(f"""
            <div class="card">

                <div class="card-title">

                    {action.icon}

                    {action.title}

                </div>


                <div class="card-content">

                    {action.description}

                </div>

            </div>
            """)


        if action.callback:


            if st.button(

                f"Open {action.title}",

                key=f"quick_{action.title}",

            ):

                action.callback()



    # -------------------------------------------------------------------------
    # Default Dashboard Actions
    # -------------------------------------------------------------------------

    @staticmethod
    def default_actions(
        *,
        analyze_callback: Optional[Callable] = None,
        history_callback: Optional[Callable] = None,
        settings_callback: Optional[Callable] = None,
        export_callback: Optional[Callable] = None,
    ) -> list[QuickAction]:
        """
        Create standard dashboard actions.

        Args:

            analyze_callback:
                Navigate to analysis page.

            history_callback:
                Navigate to history.

            settings_callback:
                Open settings.

            export_callback:
                Export reports.

        Returns:
            list[QuickAction]
        """

        return [

            QuickAction(

                title="Analyze Paper",

                description=
                    "Upload and analyze a research paper using AI.",

                icon="📄",

                callback=analyze_callback,

            ),



            QuickAction(

                title="History",

                description=
                    "Review previous research analyses.",

                icon="🗂️",

                callback=history_callback,

            ),



            QuickAction(

                title="AI Settings",

                description=
                    "Configure providers and models.",

                icon="🤖",

                callback=settings_callback,

            ),



            QuickAction(

                title="Export Reports",

                description=
                    "Generate research-ready reports.",

                icon="📤",

                callback=export_callback,

            ),

        ]



    # -------------------------------------------------------------------------
    # Empty State
    # -------------------------------------------------------------------------

    @staticmethod
    def empty() -> None:
        """
        Render empty action state.
        """

        render_html("""
            <div class="card">

                <div class="card-title">

                    No Actions Available

                </div>


                <div class="card-content">

                    Dashboard actions will appear here.

                </div>

            </div>
            """)