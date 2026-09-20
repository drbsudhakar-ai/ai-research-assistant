"""
Export Option Card Component

Reusable Streamlit UI card component for displaying
export configuration options.

Responsibilities:
- Render grouped export options
- Provide consistent visual structure
- Display title, description, and controls

Does NOT contain:
- Export logic
- Validation logic
- Settings persistence
- Configuration state management

Version:
    1.0.0
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from collections.abc import Callable

import streamlit as st


# ---------------------------------------------------------------------------
# Component
# ---------------------------------------------------------------------------


def render_export_option_card(
    title: str,
    description: str,
    render_control: Callable[[], None],
    *,
    expanded: bool = True,
) -> None:
    """
    Render an export settings option card.

    Args:
        title:
            Card heading.

        description:
            Supporting information.

        render_control:
            Callback responsible for rendering
            the actual input control.

        expanded:
            Whether card content is expanded by default.

    Returns:
        None
    """

    with st.container():

        render_html(f"""
            <div class="settings-card">

                <h4>
                    {title}
                </h4>

                <p>
                    {description}
                </p>

            </div>
            """)

        with st.expander(
            "Configure",
            expanded=expanded,
        ):
            render_control()


# ---------------------------------------------------------------------------
# Alternative Compact Renderer
# ---------------------------------------------------------------------------


def render_export_toggle_card(
    title: str,
    description: str,
    value: bool,
    key: str,
) -> bool:
    """
    Render a simple boolean export option card.

    Useful for:
    - Include metadata
    - Include summary
    - Include citations

    Args:
        title:
            Option title.

        description:
            Option explanation.

        value:
            Current boolean state.

        key:
            Streamlit widget key.

    Returns:
        Updated boolean value.
    """

    with st.container():

        render_html(f"""
            <div class="settings-card">

                <h4>
                    {title}
                </h4>

                <p>
                    {description}
                </p>

            </div>
            """)

        return st.toggle(
            label=title,
            value=value,
            key=key,
        )