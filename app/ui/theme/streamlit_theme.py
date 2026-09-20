"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme System
File         : app/ui/theme/streamlit_theme.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Streamlit CSS theme integration layer.

    Responsibilities:
        - Generate application-wide CSS.
        - Apply theme variables.
        - Style Streamlit native components.
        - Provide consistent visual appearance.

    Non-Responsibilities:
        - Page-specific styling.
        - Business logic.
        - Component rendering.

Dependencies:
    Internal:
        - app.ui.theme.color_palette
        - app.ui.theme.components
        - app.ui.theme.design_tokens
        - app.ui.theme.spacing
        - app.ui.theme.typography

    External:
        - streamlit
        - Python >= 3.11

Usage:
    from app.ui.theme.streamlit_theme import apply_streamlit_theme

    apply_streamlit_theme()

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
import streamlit as st


from app.ui.theme.components import COMPONENTS
from app.ui.theme.design_tokens import TOKENS
from app.ui.theme.spacing import SPACING
from app.ui.theme.typography import TYPOGRAPHY


def generate_theme_css() -> str:
    """
    Generate global Streamlit CSS.

    Returns:
        str:
            CSS stylesheet string.
    """

    return f"""
    <style>

    /* ==========================================================
       Global Application Theme
       ========================================================== */

    html,
    body,
    [class*="css"] {{
        font-family: {TYPOGRAPHY.FONT_FAMILY.PRIMARY};
    }}


    .stApp {{

        background-color:
            {TOKENS.COLORS.BACKGROUND};

        color:
            {TOKENS.COLORS.TEXT_PRIMARY};

    }}


    /* ==========================================================
       Main Content Container
       ========================================================== */

    .block-container {{

        padding-top:
            {SPACING.LAYOUT.PAGE_PADDING_TOP};

        padding-bottom:
            {SPACING.LAYOUT.PAGE_PADDING_BOTTOM};

        padding-left:
            {SPACING.LAYOUT.PAGE_PADDING_HORIZONTAL};

        padding-right:
            {SPACING.LAYOUT.PAGE_PADDING_HORIZONTAL};

        max-width:
            {TOKENS.COMPONENTS.PAGE_MAX_WIDTH};

    }}


    /* ==========================================================
       Headings
       ========================================================== */

    h1 {{

        font-size:
            {TYPOGRAPHY.FONT_SIZE.DISPLAY};

        font-weight:
            {TYPOGRAPHY.FONT_WEIGHT.BOLD};

        color:
            {TOKENS.TOKENS.COLORS.TEXT_PRIMARY};

    }}


    h2 {{

        font-size:
            {TYPOGRAPHY.FONT_SIZE.XXL};

        font-weight:
            {TYPOGRAPHY.FONT_WEIGHT.SEMIBOLD};

        color:
            {TOKENS.TOKENS.COLORS.TEXT_PRIMARY};

    }}


    h3 {{

        font-size:
            {TYPOGRAPHY.FONT_SIZE.XL};

        font-weight:
            {TYPOGRAPHY.FONT_WEIGHT.SEMIBOLD};

        color:
            {TOKENS.TOKENS.COLORS.TEXT_PRIMARY};

    }}


    p {{

        font-size:
            {TYPOGRAPHY.FONT_SIZE.BODY};

        line-height:
            {TYPOGRAPHY.LINE_HEIGHT.RELAXED};

    }}


    /* ==========================================================
       Streamlit Buttons
       ========================================================== */

    .stButton > button {{

        height:
            {COMPONENTS.BUTTON.HEIGHT};

        border-radius:
            {COMPONENTS.BUTTON.BORDER_RADIUS};

        font-size:
            {COMPONENTS.BUTTON.FONT_SIZE};

        font-weight:
            {COMPONENTS.BUTTON.FONT_WEIGHT};

        padding:
            {COMPONENTS.BUTTON.PADDING_VERTICAL}
            {COMPONENTS.BUTTON.PADDING_HORIZONTAL};

        border:
            {TOKENS.BORDERS.BORDER_WIDTH}
            solid
            {TOKENS.TOKENS.COLORS.BORDER};

    }}


    .stButton > button:hover {{

        border-color:
            {TOKENS.TOKENS.COLORS.PRIMARY};

        color:
            {TOKENS.TOKENS.COLORS.PRIMARY};

    }}


    /* ==========================================================
       Cards
       ========================================================== */

    .ara-card {{

        background:
            {COMPONENTS.CARD.BACKGROUND};

        border:
            {TOKENS.BORDERS.BORDER_WIDTH}
            solid
            {COMPONENTS.CARD.BORDER};

        border-radius:
            {COMPONENTS.CARD.BORDER_RADIUS};

        padding:
            {COMPONENTS.CARD.PADDING};

        box-shadow:
            {COMPONENTS.CARD.SHADOW};

    }}


    /* ==========================================================
       Metrics
       ========================================================== */

    .ara-metric-value {{

        font-size:
            {COMPONENTS.METRIC_CARD.VALUE_SIZE};

        font-weight:
            {COMPONENTS.METRIC_CARD.VALUE_WEIGHT};

        color:
            {TOKENS.TOKENS.COLORS.PRIMARY};

    }}


    .ara-metric-label {{

        font-size:
            {COMPONENTS.METRIC_CARD.LABEL_SIZE};

        color:
            {TOKENS.TOKENS.COLORS.TEXT_SECONDARY};

    }}


    /* ==========================================================
       Upload Area
       ========================================================== */

    .ara-upload {{

        background:
            {COMPONENTS.UPLOAD_AREA.BACKGROUND};

        border:
            {TOKENS.BORDERS.BORDER_WIDTH}
            dashed
            {COMPONENTS.UPLOAD_AREA.BORDER};

        border-radius:
            {COMPONENTS.UPLOAD_AREA.BORDER_RADIUS};

        padding:
            {COMPONENTS.UPLOAD_AREA.PADDING};

    }}


    /* ==========================================================
       Analysis Result Panel
       ========================================================== */

    .ara-result-panel {{

        background:
            {COMPONENTS.RESULT_PANEL.BACKGROUND};

        border:
            {TOKENS.BORDERS.BORDER_WIDTH}
            solid
            {COMPONENTS.RESULT_PANEL.BORDER};

        border-radius:
            {COMPONENTS.RESULT_PANEL.BORDER_RADIUS};

        padding:
            {COMPONENTS.RESULT_PANEL.PADDING};

    }}


    /* ==========================================================
       Sidebar
       ========================================================== */

    section[data-testid="stSidebar"] {{

        background:
            {TOKENS.TOKENS.COLORS.SURFACE};

    }}


    /* ==========================================================
       Hide Streamlit Branding
       ========================================================== */

    #MainMenu {{

        visibility:
            hidden;

    }}


    footer {{

        visibility:
            hidden;

    }}


    header {{

        visibility:
            hidden;

    }}


    </style>
    """


def apply_streamlit_theme() -> None:
    """
    Apply application theme CSS to Streamlit.

    Should be called once during application startup.
    """

    render_html(generate_theme_css())