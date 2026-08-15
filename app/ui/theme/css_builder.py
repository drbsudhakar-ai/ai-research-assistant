"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/theme/css_builder.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Central CSS generation engine for the AI Research Assistant UI.

    This module is responsible for generating application-wide CSS using
    the design system. It converts design tokens into reusable CSS variables
    and provides consistent styling for all Streamlit pages.

Responsibilities
----------------
• Generate CSS custom properties.
• Build global application styles.
• Build typography styles.
• Build layout styles.
• Generate responsive CSS.
• Support light and dark themes.
• Inject CSS into Streamlit.
• Cache generated CSS.

Non Responsibilities
--------------------
• Theme switching logic.
• UI component rendering.
• Business logic.
• Streamlit page creation.

Dependencies
------------
Internal
    app.ui.theme.colors

External
    streamlit

===============================================================================
"""

from __future__ import annotations

from app.ui.html_renderer import render_html
from dataclasses import dataclass

from typing import Final

import streamlit as st

from app.ui.theme.colors import (
    ColorPalette,
    Colors,
)

__all__ = [
    "CSSBuilder",
]


# =============================================================================
# Configuration
# =============================================================================

_DEFAULT_THEME: Final[str] = "light"

_DEFAULT_FONT: Final[str] = (
    "'Inter',"
    "'Segoe UI',"
    "'Helvetica Neue',"
    "Arial,"
    "sans-serif"
)

_DEFAULT_RADIUS: Final[str] = "14px"

_DEFAULT_TRANSITION: Final[str] = (
    "all 0.25s ease"
)


# =============================================================================
# CSS Builder
# =============================================================================


@dataclass(slots=True)
class CSSBuilder:
    """
    Generates the application's CSS.

    Example
    -------
    >>> CSSBuilder.inject()

    >>> css = CSSBuilder.build()
    """

    theme: str = _DEFAULT_THEME

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @property
    def palette(self) -> ColorPalette:
        """Return active color palette."""
        return Colors.get(self.theme)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @classmethod
    def inject(
        cls,
        theme: str = _DEFAULT_THEME,
    ) -> None:
        """
        Inject CSS into Streamlit.

        Parameters
        ----------
        theme:
            Theme name.
        """

        render_html(cls(theme).build())

    # -------------------------------------------------------------------------

    def build(self) -> str:
        """
        Build complete CSS.

        Returns
        -------
        str
            HTML style block.
        """

        css = "\n".join(
            [
                "<style>",
                self._variables(),
                self._reset(),
                self._layout(),
                self._typography(),
                self._cards(),
                self._hero(),
                self._buttons(),
                self._inputs(),
                self._containers(),
                self._sidebar(),
                self._navigation(),
                self._tabs(),
                self._metrics(),
                self._badges(),
                self._progress(),
                self._expanders(),
                
                "</style>",
            ]
        )

        return css

    # =========================================================================
    # CSS Variables
    # =========================================================================

    
    def _variables(self) -> str:
        """
        Generate CSS variables.
        """

        c = self.palette

        return f"""
:root {{

    /* --------------------------------------------------------------------- */
    /* Brand */
    /* --------------------------------------------------------------------- */

    --color-primary: {c.primary};
    --color-secondary: {c.secondary};
    --color-accent: {c.accent};

    /* --------------------------------------------------------------------- */
    /* Semantic */
    /* --------------------------------------------------------------------- */

    --color-success: {c.success};
    --color-warning: {c.warning};
    --color-error: {c.error};
    --color-info: {c.info};

    /* --------------------------------------------------------------------- */
    /* Backgrounds */
    /* --------------------------------------------------------------------- */

    --color-background: {c.background};
    --color-surface: {c.surface};
    --color-surface-elevated: {c.surface_elevated};

    /* --------------------------------------------------------------------- */
    /* Text */
    /* --------------------------------------------------------------------- */

    --color-text-primary: {c.text_primary};
    --color-text-secondary: {c.text_secondary};
    --color-text-muted: {c.text_muted};
    --color-text-inverse: {c.text_inverse};

    /* --------------------------------------------------------------------- */
    /* Borders */
    /* --------------------------------------------------------------------- */

    --color-border: {c.border};
    --color-border-light: {c.border_light};

    --color-disabled: {c.disabled};

    /* --------------------------------------------------------------------- */
    /* Charts */
    /* --------------------------------------------------------------------- */

    --chart-primary: {c.chart_primary};
    --chart-secondary: {c.chart_secondary};
    --chart-success: {c.chart_success};
    --chart-warning: {c.chart_warning};
    --chart-error: {c.chart_error};

    /* --------------------------------------------------------------------- */
    /* Typography */
    /* --------------------------------------------------------------------- */

    --font-family: {_DEFAULT_FONT};

    --font-xs: 0.75rem;
    --font-sm: 0.875rem;
    --font-md: 1rem;
    --font-lg: 1.125rem;
    --font-xl: 1.35rem;
    --font-2xl: 1.75rem;
    --font-3xl: 2.25rem;

    /* --------------------------------------------------------------------- */
    /* Radius */
    /* --------------------------------------------------------------------- */

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: {_DEFAULT_RADIUS};
    --radius-xl: 22px;

    /* --------------------------------------------------------------------- */
    /* Shadow */
    /* --------------------------------------------------------------------- */

    --shadow-sm:
        0 1px 2px rgba(0,0,0,.05);

    --shadow-md:
        0 6px 12px rgba(0,0,0,.08);

    --shadow-lg:
        0 14px 28px rgba(0,0,0,.12);

    /* --------------------------------------------------------------------- */
    /* Spacing */
    /* --------------------------------------------------------------------- */

    --space-1: .25rem;
    --space-2: .5rem;
    --space-3: .75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
    --space-7: 2.5rem;
    --space-8: 3rem;

    /* --------------------------------------------------------------------- */

    --transition: {_DEFAULT_TRANSITION};

}}
"""

    # =========================================================================
    # Reset
    # =========================================================================

    def _reset(self) -> str:
        """
        Global CSS reset.
        """

        return """
*,
*::before,
*::after{
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{
    margin:0;
    padding:0;
    background:var(--color-background);
    color:var(--color-text-primary);
    font-family:var(--font-family);
    line-height:1.6;
}

a{
    color:var(--color-primary);
    text-decoration:none;
}

img{
    max-width:100%;
    display:block;
}
"""

    # =========================================================================
    # Layout
    # =========================================================================

    def _layout(self) -> str:
        """
        Application layout CSS.
        """

        return """
.main .block-container{

    max-width:1400px;

    padding-top:2rem;

    padding-bottom:3rem;

    padding-left:2rem;

    padding-right:2rem;

}

section.main{

    background:var(--color-background);

}

div[data-testid="stVerticalBlock"]{

    gap:1rem;

}

hr{

    border:none;

    border-top:1px solid var(--color-border-light);

    margin:1.5rem 0;

}
"""

    # =========================================================================
    # Typography
    # =========================================================================

    def _typography(self) -> str:
        """
        Typography rules.
        """

        return """
h1{

    font-size:var(--font-3xl);

    font-weight:700;

    color:var(--color-text-primary);

    margin-bottom:.75rem;

}

h2{

    font-size:var(--font-2xl);

    font-weight:700;

    color:var(--color-text-primary);

}

h3{

    font-size:var(--font-xl);

    font-weight:600;

    color:var(--color-text-primary);

}

h4{

    font-size:var(--font-lg);

    font-weight:600;

}

p{

    color:var(--color-text-secondary);

    font-size:var(--font-md);

}

small{

    color:var(--color-text-muted);

}

strong{

    color:var(--color-text-primary);

}
"""

    # =========================================================================
    # Cards
    # =========================================================================

    def _cards(self) -> str:
        """
        Card components.
        """

        return """
/* ------------------------------------------------------------------------- */
/* Generic Card */
/* ------------------------------------------------------------------------- */

.ai-card{

    background:var(--color-surface);

    border:1px solid var(--color-border-light);

    border-radius:var(--radius-lg);

    padding:1.5rem;

    box-shadow:var(--shadow-sm);

    transition:var(--transition);

}

.ai-card:hover{

    transform:translateY(-2px);

    box-shadow:var(--shadow-md);

}

.ai-card-header{

    display:flex;

    justify-content:space-between;

    align-items:center;

    margin-bottom:1rem;

}

.ai-card-title{

    font-size:var(--font-lg);

    font-weight:700;

    color:var(--color-text-primary);

}

.ai-card-subtitle{

    font-size:var(--font-sm);

    color:var(--color-text-muted);

}

.ai-card-body{

    color:var(--color-text-secondary);

}

.ai-card-footer{

    margin-top:1.25rem;

    padding-top:1rem;

    border-top:1px solid var(--color-border-light);

}

/* ------------------------------------------------------------------------- */
/* Elevated Card */
/* ------------------------------------------------------------------------- */

.ai-card-elevated{

    background:var(--color-surface);

    border-radius:var(--radius-xl);

    border:none;

    box-shadow:var(--shadow-lg);

}

/* ------------------------------------------------------------------------- */
/* Compact Card */
/* ------------------------------------------------------------------------- */

.ai-card-compact{

    padding:1rem;

}
"""

    # =========================================================================
    # Hero Banner
    # =========================================================================

    def _hero(self) -> str:
        """
        Hero banner styles.
        """

        return """
.ai-hero{

    background:linear-gradient(
        135deg,
        var(--color-primary),
        var(--color-secondary)
    );

    border-radius:var(--radius-xl);

    padding:3rem;

    color:white;

    margin-bottom:2rem;

    overflow:hidden;

    position:relative;

}

.ai-hero::before{

    content:"";

    position:absolute;

    inset:0;

    opacity:.08;

    background:
        radial-gradient(circle at top right,
        white 0%,
        transparent 70%);

}

.ai-hero-title{

    position:relative;

    font-size:2.4rem;

    font-weight:700;

    margin-bottom:.75rem;

    color:white;

}

.ai-hero-subtitle{

    position:relative;

    max-width:760px;

    color:rgba(255,255,255,.92);

    font-size:1.1rem;

    line-height:1.8;

}
"""

    # =========================================================================
    # Buttons
    # =========================================================================

    def _buttons(self) -> str:
        """
        Button styling.
        """

        return """
.stButton>button{

    border:none;

    border-radius:var(--radius-md);

    background:var(--color-primary);

    color:white;

    font-weight:600;

    min-height:44px;

    transition:var(--transition);

}

.stButton>button:hover{

    transform:translateY(-1px);

    box-shadow:var(--shadow-md);

    background:var(--color-secondary);

}

.stButton>button:focus{

    outline:none;

}

.stDownloadButton>button{

    border-radius:var(--radius-md);

    border:none;

    background:var(--color-success);

    color:white;

    transition:var(--transition);

}

.stDownloadButton>button:hover{

    background:var(--color-primary);

}

.stFormSubmitButton>button{

    background:var(--color-primary);

    border:none;

    color:white;

    border-radius:var(--radius-md);

}
"""

    # =========================================================================
    # Inputs
    # =========================================================================

    def _inputs(self) -> str:
        """
        Form controls.
        """

        return """
.stTextInput input,
.stNumberInput input,
.stTextArea textarea{

    border-radius:var(--radius-md);

    border:1px solid var(--color-border);

    background:var(--color-surface);

    color:var(--color-text-primary);

}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus{

    border-color:var(--color-primary);

    box-shadow:0 0 0 3px rgba(37,99,235,.15);

}

.stSelectbox div[data-baseweb="select"]{

    border-radius:var(--radius-md);

}

.stMultiSelect div[data-baseweb="select"]{

    border-radius:var(--radius-md);

}

.stDateInput input{

    border-radius:var(--radius-md);

}

.stFileUploader{

    border-radius:var(--radius-lg);

}

section[data-testid="stFileUploaderDropzone"]{

    border:2px dashed var(--color-border);

    border-radius:var(--radius-lg);

    background:var(--color-surface);

    transition:var(--transition);

}

section[data-testid="stFileUploaderDropzone"]:hover{

    border-color:var(--color-primary);

}
"""

    # =========================================================================
    # Containers
    # =========================================================================

    def _containers(self) -> str:
        """
        Shared layout containers.
        """

        return """
.ai-section{

    margin-bottom:2rem;

}

.ai-grid{

    display:grid;

    gap:1.5rem;

}

.ai-grid-2{

    grid-template-columns:repeat(2,1fr);

}

.ai-grid-3{

    grid-template-columns:repeat(3,1fr);

}

.ai-grid-4{

    grid-template-columns:repeat(4,1fr);

}

.ai-flex{

    display:flex;

    gap:1rem;

}

.ai-flex-between{

    display:flex;

    justify-content:space-between;

    align-items:center;

}

.ai-center{

    display:flex;

    justify-content:center;

    align-items:center;

}

.ai-divider{

    height:1px;

    background:var(--color-border-light);

    margin:2rem 0;

}
"""

    # =========================================================================
    # Sidebar
    # =========================================================================

    def _sidebar(self) -> str:
        """
        Sidebar styling.
        """

        return """
section[data-testid="stSidebar"]{

    background:var(--color-surface);

    border-right:1px solid var(--color-border-light);

}

section[data-testid="stSidebar"] .block-container{

    padding-top:1.5rem;

    padding-left:1rem;

    padding-right:1rem;

}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{

    color:var(--color-text-primary);

}

section[data-testid="stSidebar"] hr{

    border-top:1px solid var(--color-border-light);

}
"""

    # =========================================================================
    # Navigation
    # =========================================================================

    def _navigation(self) -> str:
        """
        Navigation widgets.
        """

        return """
.stRadio > div{

    gap:.5rem;

}

.stRadio label{

    border-radius:var(--radius-md);

    transition:var(--transition);

}

.stRadio label:hover{

    background:var(--color-surface-elevated);

}

.stCheckbox label{

    color:var(--color-text-primary);

}

.stToggle label{

    color:var(--color-text-primary);

}
"""

    # =========================================================================
    # Tabs
    # =========================================================================

    def _tabs(self) -> str:
        """
        Tab styling.
        """

        return """
.stTabs [data-baseweb="tab-list"]{

    gap:.5rem;

    border-bottom:1px solid var(--color-border-light);

}

.stTabs [data-baseweb="tab"]{

    border-radius:var(--radius-md);

    padding:.75rem 1.25rem;

    transition:var(--transition);

}

.stTabs [aria-selected="true"]{

    background:var(--color-primary);

    color:white;

}
"""

    # =========================================================================
    # Metrics
    # =========================================================================

    def _metrics(self) -> str:
        """
        Metric card styling.
        """

        return """
div[data-testid="stMetric"]{

    background:var(--color-surface);

    border:1px solid var(--color-border-light);

    border-radius:var(--radius-lg);

    padding:1rem;

    box-shadow:var(--shadow-sm);

}

div[data-testid="stMetric"]:hover{

    box-shadow:var(--shadow-md);

}

div[data-testid="stMetricLabel"]{

    color:var(--color-text-muted);

}

div[data-testid="stMetricValue"]{

    color:var(--color-text-primary);

    font-weight:700;

}
"""

    # =========================================================================
    # Status Badges
    # =========================================================================

    def _badges(self) -> str:
        """
        Badge components.
        """

        return """
.ai-badge{

    display:inline-flex;

    align-items:center;

    gap:.35rem;

    padding:.35rem .75rem;

    border-radius:999px;

    font-size:.80rem;

    font-weight:600;

}

.ai-badge-success{

    background:rgba(22,163,74,.10);

    color:var(--color-success);

}

.ai-badge-warning{

    background:rgba(217,119,6,.10);

    color:var(--color-warning);

}

.ai-badge-error{

    background:rgba(220,38,38,.10);

    color:var(--color-error);

}

.ai-badge-info{

    background:rgba(2,132,199,.10);

    color:var(--color-info);

}
"""

    # =========================================================================
    # Progress
    # =========================================================================

    def _progress(self) -> str:
        """
        Progress bar styling.
        """

        return """
div[data-testid="stProgressBar"]{

    margin-top:.5rem;

    margin-bottom:1rem;

}

div[data-testid="stProgressBar"] > div{

    border-radius:999px;

    overflow:hidden;

}

div[data-testid="stProgressBar"] div[role="progressbar"]{

    background:linear-gradient(
        90deg,
        var(--color-primary),
        var(--color-accent)
    );

}

.ai-progress-label{

    display:flex;

    justify-content:space-between;

    font-size:.9rem;

    margin-bottom:.4rem;

    color:var(--color-text-secondary);

}
"""

    # =========================================================================
    # Expanders
    # =========================================================================

    def _expanders(self) -> str:
        """
        Expander styling.
        """

        return """
details{

    border:1px solid var(--color-border-light);

    border-radius:var(--radius-lg);

    background:var(--color-surface);

}

summary{

    font-weight:600;

    padding:.85rem 1rem;

    cursor:pointer;

}

details[open] summary{

    border-bottom:1px solid var(--color-border-light);

}
"""

    # =========================================================================
    # Tables
    # =========================================================================

    def _tables(self) -> str:
        """
        Table and dataframe styling.
        """

        return """
/* ------------------------------------------------------------------------- */
/* Streamlit DataFrame */
/* ------------------------------------------------------------------------- */

div[data-testid="stDataFrame"]{

    border:1px solid var(--color-border-light);

    border-radius:var(--radius-lg);

    overflow:hidden;

    box-shadow:var(--shadow-sm);

}

/* ------------------------------------------------------------------------- */
/* HTML Tables */
/* ------------------------------------------------------------------------- */

table{

    width:100%;

    border-collapse:collapse;

    background:var(--color-surface);

    border-radius:var(--radius-lg);

    overflow:hidden;

}

thead{

    background:var(--color-primary);

    color:white;

}

th{

    padding:.9rem 1rem;

    text-align:left;

    font-weight:600;

}

td{

    padding:.85rem 1rem;

    border-bottom:1px solid var(--color-border-light);

    color:var(--color-text-secondary);

}

tbody tr{

    transition:var(--transition);

}

tbody tr:hover{

    background:var(--color-surface-elevated);

}

tbody tr:last-child td{

    border-bottom:none;

}
"""

    # =========================================================================
    # Alerts
    # =========================================================================

    def _alerts(self) -> str:
        """
        Alert components.
        """

        return """
.ai-alert{

    display:flex;

    align-items:flex-start;

    gap:.75rem;

    padding:1rem 1.25rem;

    border-radius:var(--radius-lg);

    margin:1rem 0;

    border-left:5px solid transparent;

}

.ai-alert-success{

    background:rgba(22,163,74,.08);

    border-left-color:var(--color-success);

    color:var(--color-success);

}

.ai-alert-warning{

    background:rgba(217,119,6,.08);

    border-left-color:var(--color-warning);

    color:var(--color-warning);

}

.ai-alert-error{

    background:rgba(220,38,38,.08);

    border-left-color:var(--color-error);

    color:var(--color-error);

}

.ai-alert-info{

    background:rgba(2,132,199,.08);

    border-left-color:var(--color-info);

    color:var(--color-info);

}
"""

    # =========================================================================
    # Dialogs
    # =========================================================================

    def _dialogs(self) -> str:
        """
        Dialog and modal styling.
        """

        return """
div[data-testid="stDialog"]{

    border-radius:var(--radius-xl);

    border:none;

    box-shadow:var(--shadow-lg);

}

div[data-testid="stModal"]{

    border-radius:var(--radius-xl);

}

.ai-dialog{

    background:var(--color-surface);

    border-radius:var(--radius-xl);

    padding:2rem;

    box-shadow:var(--shadow-lg);

}

.ai-dialog-header{

    font-size:var(--font-xl);

    font-weight:700;

    margin-bottom:1rem;

}

.ai-dialog-footer{

    display:flex;

    justify-content:flex-end;

    gap:1rem;

    margin-top:2rem;

}
"""

    # =========================================================================
    # Code Blocks
    # =========================================================================

    def _code_blocks(self) -> str:
        """
        Code block styling.
        """

        return """
pre{

    background:#0F172A;

    color:#E2E8F0;

    border-radius:var(--radius-lg);

    padding:1rem;

    overflow-x:auto;

    font-size:.90rem;

}

code{

    font-family:
        "JetBrains Mono",
        "Consolas",
        monospace;

}

.stCodeBlock{

    border-radius:var(--radius-lg);

    overflow:hidden;

    box-shadow:var(--shadow-sm);

}

kbd{

    background:var(--color-surface-elevated);

    border:1px solid var(--color-border);

    border-radius:6px;

    padding:.15rem .45rem;

    font-size:.85rem;

}
"""

# =============================================================================
# File        : app/ui/theme/css_builder.py
# Part        : 4B
# =============================================================================

    # -------------------------------------------------------------------------
    # Layout CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_layout_css() -> str:
        """
        Generate application layout styles.

        Returns:
            str: CSS block for layouts.
        """

        return """
        /* ================================================================
           Layout System
           ================================================================ */

        .app-container {
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--space-xl);
        }


        .section {
            margin-bottom: var(--space-xl);
        }


        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: var(--space-md);
        }


        .section-title {
            font-family: var(--font-family-heading);
            font-size: var(--font-size-xl);
            font-weight: var(--font-weight-semibold);
            color: var(--color-text-primary);
        }


        .section-description {
            font-size: var(--font-size-sm);
            color: var(--color-text-secondary);
            margin-top: var(--space-xs);
        }


        .grid {
            display: grid;
            gap: var(--space-lg);
        }


        .grid-2 {
            grid-template-columns: repeat(
                2,
                minmax(0, 1fr)
            );
        }


        .grid-3 {
            grid-template-columns: repeat(
                3,
                minmax(0, 1fr)
            );
        }


        .grid-4 {
            grid-template-columns: repeat(
                4,
                minmax(0, 1fr)
            );
        }


        @media(max-width: 1024px) {

            .grid-4,
            .grid-3 {
                grid-template-columns:
                    repeat(2, minmax(0, 1fr));
            }

        }


        @media(max-width: 768px) {

            .grid-4,
            .grid-3,
            .grid-2 {

                grid-template-columns:
                    1fr;
            }

        }
        """


    # -------------------------------------------------------------------------
    # Card Components
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_card_css() -> str:
        """
        Generate reusable card component CSS.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Card Components
           ================================================================ */


        .card {

            background:
                var(--color-background-card);

            border:
                1px solid
                var(--color-border);

            border-radius:
                var(--radius-lg);

            padding:
                var(--space-lg);

            box-shadow:
                var(--shadow-sm);

            transition:
                all
                var(--transition-fast);

        }



        .card:hover {

            box-shadow:
                var(--shadow-md);

            transform:
                translateY(-2px);

        }



        .card-header {

            display:
                flex;

            align-items:
                center;

            justify-content:
                space-between;

            margin-bottom:
                var(--space-md);

        }



        .card-title {

            font-size:
                var(--font-size-lg);

            font-weight:
                var(--font-weight-semibold);

            color:
                var(--color-text-primary);

        }



        .card-content {

            color:
                var(--color-text-secondary);

            line-height:
                1.6;

        }



        .card-footer {

            margin-top:
                var(--space-lg);

            padding-top:
                var(--space-md);

            border-top:
                1px solid
                var(--color-border);

        }

        """


    # -------------------------------------------------------------------------
    # Metric Card CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_metric_css() -> str:
        """
        Generate dashboard metric card styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Metric Cards
           ================================================================ */


        .metric-card {

            background:
                var(--color-background-card);

            border-radius:
                var(--radius-lg);

            padding:
                var(--space-lg);

            border:
                1px solid
                var(--color-border);

            text-align:
                center;

        }



        .metric-value {

            font-size:
                var(--font-size-3xl);

            font-weight:
                var(--font-weight-bold);

            color:
                var(--color-primary);

            line-height:
                1.2;

        }



        .metric-label {

            margin-top:
                var(--space-sm);

            font-size:
                var(--font-size-sm);

            color:
                var(--color-text-secondary);

        }



        .metric-change {

            margin-top:
                var(--space-xs);

            font-size:
                var(--font-size-xs);

        }



        .metric-positive {

            color:
                var(--color-success);

        }



        .metric-negative {

            color:
                var(--color-danger);

        }

        """
        

# =============================================================================
# File        : app/ui/theme/css_builder.py
# Part        : 4C
# =============================================================================


    # -------------------------------------------------------------------------
    # Button System CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_button_css() -> str:
        """
        Generate button component styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Button System
           ================================================================ */


        .btn {

            display:
                inline-flex;

            align-items:
                center;

            justify-content:
                center;

            gap:
                var(--space-sm);

            padding:
                var(--space-sm)
                var(--space-lg);

            border-radius:
                var(--radius-md);

            font-family:
                var(--font-family-body);

            font-size:
                var(--font-size-sm);

            font-weight:
                var(--font-weight-medium);

            cursor:
                pointer;

            transition:
                all
                var(--transition-fast);

            border:
                none;

        }



        .btn-primary {

            background:
                var(--color-primary);

            color:
                var(--color-text-on-primary);

        }



        .btn-primary:hover {

            background:
                var(--color-primary-hover);

            transform:
                translateY(-1px);

        }



        .btn-secondary {

            background:
                var(--color-secondary);

            color:
                var(--color-text-on-secondary);

        }



        .btn-outline {

            background:
                transparent;

            border:
                1px solid
                var(--color-primary);

            color:
                var(--color-primary);

        }



        .btn-danger {

            background:
                var(--color-danger);

            color:
                white;

        }



        .btn-disabled {

            opacity:
                0.6;

            cursor:
                not-allowed;

        }

        """



    # -------------------------------------------------------------------------
    # Form Controls CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_form_css() -> str:
        """
        Generate form input styling.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Form Controls
           ================================================================ */


        input,
        textarea,
        select {

            width:
                100%;

            padding:
                var(--space-sm)
                var(--space-md);

            border-radius:
                var(--radius-md);

            border:
                1px solid
                var(--color-border);

            background:
                var(--color-background-input);

            color:
                var(--color-text-primary);

            font-size:
                var(--font-size-sm);

            transition:
                border
                var(--transition-fast);

        }



        input:focus,
        textarea:focus,
        select:focus {

            outline:
                none;

            border-color:
                var(--color-primary);

            box-shadow:
                0 0 0 2px
                var(--color-primary-alpha);

        }



        label {

            font-size:
                var(--font-size-sm);

            font-weight:
                var(--font-weight-medium);

            color:
                var(--color-text-primary);

            margin-bottom:
                var(--space-xs);

        }

        """



    # -------------------------------------------------------------------------
    # Streamlit Widget Overrides
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_streamlit_override_css() -> str:
        """
        Override Streamlit default component styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Streamlit Overrides
           ================================================================ */


        .stApp {

            background:
                var(--color-background-page);

            color:
                var(--color-text-primary);

        }



        div[data-testid="stSidebar"] {

            background:
                var(--color-background-sidebar);

            border-right:
                1px solid
                var(--color-border);

        }



        div[data-testid="stMetric"] {

            background:
                var(--color-background-card);

            padding:
                var(--space-md);

            border-radius:
                var(--radius-lg);

            border:
                1px solid
                var(--color-border);

        }



        div[data-testid="stButton"] button {

            border-radius:
                var(--radius-md);

            font-weight:
                var(--font-weight-medium);

            transition:
                all
                var(--transition-fast);

        }



        div[data-testid="stButton"] button:hover {

            transform:
                translateY(-1px);

        }



        .stMarkdown {

            color:
                var(--color-text-primary);

        }

        """



    # -------------------------------------------------------------------------
    # File Uploader CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_file_uploader_css() -> str:
        """
        Style Streamlit file uploader.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           File Upload Component
           ================================================================ */


        div[data-testid="stFileUploader"] {

            background:
                var(--color-background-card);

            padding:
                var(--space-lg);

            border-radius:
                var(--radius-lg);

            border:
                1px dashed
                var(--color-border);

        }



        div[data-testid="stFileUploader"]:hover {

            border-color:
                var(--color-primary);

        }



        section[data-testid="stFileUploaderDropzone"] {

            background:
                var(--color-background-page);

            border-radius:
                var(--radius-md);

        }

        """



    # -------------------------------------------------------------------------
    # Progress Components CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_progress_css() -> str:
        """
        Generate progress indicator styling.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Progress Components
           ================================================================ */


        .progress-container {

            width:
                100%;

            background:
                var(--color-background-muted);

            border-radius:
                var(--radius-full);

            overflow:
                hidden;

            height:
                12px;

        }



        .progress-bar {

            height:
                100%;

            background:
                var(--color-success);

            transition:
                width
                var(--transition-normal);

        }



        .progress-text {

            margin-top:
                var(--space-xs);

            font-size:
                var(--font-size-sm);

            color:
                var(--color-text-secondary);

        }

        """



    # -------------------------------------------------------------------------
    # Status Badge CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_badge_css() -> str:
        """
        Generate status badge styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Status Badges
           ================================================================ */


        .badge {

            display:
                inline-flex;

            align-items:
                center;

            padding:
                4px
                10px;

            border-radius:
                var(--radius-full);

            font-size:
                var(--font-size-xs);

            font-weight:
                var(--font-weight-medium);

        }



        .badge-success {

            background:
                var(--color-success-bg);

            color:
                var(--color-success);

        }



        .badge-warning {

            background:
                var(--color-warning-bg);

            color:
                var(--color-warning);

        }



        .badge-danger {

            background:
                var(--color-danger-bg);

            color:
                var(--color-danger);

        }



        .badge-info {

            background:
                var(--color-info-bg);

            color:
                var(--color-info);

        }

        """

# =============================================================================
# File        : app/ui/theme/css_builder.py
# Part        : 4D
# =============================================================================


    # -------------------------------------------------------------------------
    # Hero Banner CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_hero_css() -> str:
        """
        Generate hero banner styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Hero Banner
           ================================================================ */


        .hero {

            background:
                linear-gradient(
                    135deg,
                    var(--color-primary),
                    var(--color-secondary)
                );

            border-radius:
                var(--radius-xl);

            padding:
                var(--space-2xl);

            color:
                white;

            margin-bottom:
                var(--space-xl);

        }



        .hero-title {

            font-size:
                var(--font-size-4xl);

            font-weight:
                var(--font-weight-bold);

            margin-bottom:
                var(--space-sm);

        }



        .hero-subtitle {

            font-size:
                var(--font-size-lg);

            opacity:
                0.9;

            line-height:
                1.6;

        }



        .hero-actions {

            margin-top:
                var(--space-lg);

            display:
                flex;

            gap:
                var(--space-md);

        }

        """



    # -------------------------------------------------------------------------
    # Navigation CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_navigation_css() -> str:
        """
        Generate navigation menu styling.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Navigation
           ================================================================ */


        .nav-item {

            display:
                flex;

            align-items:
                center;

            gap:
                var(--space-sm);

            padding:
                var(--space-sm)
                var(--space-md);

            border-radius:
                var(--radius-md);

            color:
                var(--color-text-secondary);

            text-decoration:
                none;

            transition:
                all
                var(--transition-fast);

        }



        .nav-item:hover {

            background:
                var(--color-background-hover);

            color:
                var(--color-primary);

        }



        .nav-item.active {

            background:
                var(--color-primary-light);

            color:
                var(--color-primary);

            font-weight:
                var(--font-weight-semibold);

        }

        """



    # -------------------------------------------------------------------------
    # Alert Components CSS
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_alert_css() -> str:
        """
        Generate notification and alert styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Alerts
           ================================================================ */


        .alert {

            display:
                flex;

            gap:
                var(--space-sm);

            padding:
                var(--space-md);

            border-radius:
                var(--radius-md);

            margin-bottom:
                var(--space-md);

            font-size:
                var(--font-size-sm);

        }



        .alert-success {

            background:
                var(--color-success-bg);

            color:
                var(--color-success);

        }



        .alert-warning {

            background:
                var(--color-warning-bg);

            color:
                var(--color-warning);

        }



        .alert-error {

            background:
                var(--color-danger-bg);

            color:
                var(--color-danger);

        }



        .alert-info {

            background:
                var(--color-info-bg);

            color:
                var(--color-info);

        }

        """



    # -------------------------------------------------------------------------
    # Research Report Styling
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_report_css() -> str:
        """
        Generate research report presentation styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Research Report Styling
           ================================================================ */


        .report {

            background:
                var(--color-background-card);

            padding:
                var(--space-xl);

            border-radius:
                var(--radius-lg);

            border:
                1px solid
                var(--color-border);

            line-height:
                1.75;

        }



        .report h1,
        .report h2,
        .report h3 {

            color:
                var(--color-text-primary);

            font-weight:
                var(--font-weight-semibold);

            margin-top:
                var(--space-xl);

            margin-bottom:
                var(--space-md);

        }



        .report p {

            color:
                var(--color-text-secondary);

            margin-bottom:
                var(--space-md);

        }



        .report blockquote {

            border-left:
                4px solid
                var(--color-primary);

            padding-left:
                var(--space-md);

            color:
                var(--color-text-muted);

            font-style:
                italic;

        }

        """



    # -------------------------------------------------------------------------
    # Table Styling
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_table_css() -> str:
        """
        Generate table styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Tables
           ================================================================ */


        table {

            width:
                100%;

            border-collapse:
                collapse;

        }



        th {

            background:
                var(--color-background-muted);

            color:
                var(--color-text-primary);

            font-weight:
                var(--font-weight-semibold);

            text-align:
                left;

            padding:
                var(--space-sm);

        }



        td {

            padding:
                var(--space-sm);

            border-bottom:
                1px solid
                var(--color-border);

            color:
                var(--color-text-secondary);

        }



        tr:hover {

            background:
                var(--color-background-hover);

        }

        """



    # -------------------------------------------------------------------------
    # Code Block Styling
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_code_css() -> str:
        """
        Generate code block styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Code Blocks
           ================================================================ */


        code {

            font-family:
                var(--font-family-mono);

            font-size:
                var(--font-size-sm);

        }



        pre {

            background:
                var(--color-code-background);

            color:
                var(--color-code-text);

            padding:
                var(--space-lg);

            border-radius:
                var(--radius-md);

            overflow-x:
                auto;

        }

        """



    # -------------------------------------------------------------------------
    # Scrollbar Styling
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_scrollbar_css() -> str:
        """
        Generate custom scrollbar styles.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Scrollbars
           ================================================================ */


        ::-webkit-scrollbar {

            width:
                8px;

        }



        ::-webkit-scrollbar-track {

            background:
                var(--color-background-muted);

        }



        ::-webkit-scrollbar-thumb {

            background:
                var(--color-border);

            border-radius:
                var(--radius-full);

        }



        ::-webkit-scrollbar-thumb:hover {

            background:
                var(--color-primary);

        }

        """



    # -------------------------------------------------------------------------
    # Animation Utilities
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_animation_css() -> str:
        """
        Generate animation utilities.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Animations
           ================================================================ */


        @keyframes fadeIn {

            from {

                opacity:
                    0;

                transform:
                    translateY(8px);

            }


            to {

                opacity:
                    1;

                transform:
                    translateY(0);

            }

        }



        .animate-fade {

            animation:
                fadeIn
                0.3s ease-in-out;

        }



        .transition {

            transition:
                all
                var(--transition-fast);

        }

        """



    # -------------------------------------------------------------------------
    # Accessibility Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_accessibility_css() -> str:
        """
        Generate accessibility helpers.

        Returns:
            str: CSS block.
        """

        return """
        /* ================================================================
           Accessibility
           ================================================================ */


        .sr-only {

            position:
                absolute;

            width:
                1px;

            height:
                1px;

            padding:
                0;

            overflow:
                hidden;

            clip:
                rect(0,0,0,0);

            white-space:
                nowrap;

            border:
                0;

        }



        :focus-visible {

            outline:
                3px solid
                var(--color-primary);

            outline-offset:
                2px;

        }

        """

    # -------------------------------------------------------------------------
    # Export CSS File
    # -------------------------------------------------------------------------

    @classmethod
    def export(cls, path: str, theme: str = _DEFAULT_THEME) -> None:
        """
        Export generated stylesheet.

        Args:
            path:
                Destination CSS file path.
        """

        css = cls(theme).build()


        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(css)



    # -------------------------------------------------------------------------
    # Debug Information
    # -------------------------------------------------------------------------

    @classmethod
    def stats(cls) -> dict:
        """
        Return CSS generation statistics.

        Returns:
            dict:
                CSS metadata.
        """

        css = cls(_DEFAULT_THEME).build()


        return {

            "characters":
                len(css),

            "lines":
                css.count("\n"),

            "components":
                [

                    "layout",
                    "cards",
                    "metrics",
                    "buttons",
                    "forms",
                    "streamlit",
                    "upload",
                    "progress",
                    "badges",
                    "hero",
                    "navigation",
                    "alerts",
                    "reports",
                    "tables",
                    "code",
                    "animations",
                    "accessibility",

                ],

        }

