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
                self._professional_workspace(),

                "</style>",
            ]
        )

        return css

    def _professional_workspace(self) -> str:
        """SYS-inspired production workspace overrides used by live pages."""

        return """
/* Professional blue–royal-purple workspace */
.stApp {
    background:
      radial-gradient(circle at 88% 2%, rgba(124,58,237,.09), transparent 24rem),
      linear-gradient(180deg,#f8faff 0%,#f5f7fc 100%);
}
.main .block-container { max-width:1280px; padding:2rem 2.5rem 4rem; }
[data-testid="stHeader"] { background:rgba(248,250,255,.82); backdrop-filter:blur(14px); }

.hero, .ara-page-hero {
    position:relative; overflow:hidden; margin:0 0 1.75rem;
    padding:2rem 2.25rem; border:1px solid rgba(124,58,237,.18);
    border-radius:24px; color:#fff;
    background:linear-gradient(125deg,#0f2c68 0%,#2457d6 48%,#7137c8 100%);
    box-shadow:0 18px 45px rgba(32,57,139,.18);
}
.hero::after, .ara-page-hero::after {
    content:""; position:absolute; width:230px; height:230px; right:-65px; top:-105px;
    border:34px solid rgba(255,255,255,.10); border-radius:50%;
}
.hero-title, .ara-page-title { position:relative; z-index:1; color:#fff; font-size:2rem; font-weight:800; letter-spacing:-.025em; }
.hero-subtitle, .ara-page-description { position:relative; z-index:1; margin-top:.45rem; color:rgba(255,255,255,.84); font-size:1rem; max-width:760px; }
.ara-page-kicker { position:relative; z-index:1; display:inline-flex; padding:.3rem .7rem; margin-bottom:.7rem; border:1px solid rgba(255,255,255,.22); border-radius:999px; background:rgba(255,255,255,.10); color:#fff; font-size:.72rem; font-weight:700; letter-spacing:.09em; text-transform:uppercase; }

.section { margin:1.75rem 0 1rem; }
.section-title { color:#10234f; font-size:1.25rem; font-weight:800; letter-spacing:-.015em; }
.section-description { margin-top:.25rem; color:#64748b; font-size:.9rem; }
.card { min-height:118px; padding:1.25rem; margin:.35rem 0 .75rem; border:1px solid #dce4f3; border-radius:17px; background:rgba(255,255,255,.94); box-shadow:0 8px 24px rgba(15,35,79,.07); transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease; }
.card:hover { transform:translateY(-2px); border-color:rgba(99,72,214,.35); box-shadow:0 14px 30px rgba(15,35,79,.11); }
.card-title { color:#172554; font-size:1rem; font-weight:750; }
.card-content { margin-top:.5rem; color:#5a6984; font-size:.88rem; line-height:1.65; }
.metric-card { position:relative; min-height:154px; padding:1.15rem 1.2rem; border:1px solid #dce4f3; border-radius:18px; background:linear-gradient(145deg,#fff,#f7f9ff); box-shadow:0 9px 24px rgba(15,35,79,.07); overflow:hidden; }
.metric-card::after { content:""; position:absolute; width:72px; height:72px; right:-26px; top:-26px; border-radius:50%; background:linear-gradient(135deg,rgba(37,99,235,.13),rgba(124,58,237,.13)); }
.metric-icon { display:grid; place-items:center; width:34px; height:34px; margin-bottom:.75rem; border-radius:10px; background:#eef2ff; font-size:1rem; }
.metric-value { color:#13265a; font-size:1.7rem; line-height:1; font-weight:850; }.metric-label { margin-top:.42rem; color:#53627d; font-size:.78rem; }.metric-change { margin-top:.65rem; color:#64748b; font-size:.7rem; font-weight:700; }.metric-positive { color:#15803d; }.metric-negative { color:#b91c1c; }
.ara-status-panel { display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:1.1rem 1.25rem; margin:1rem 0 1.8rem; border:1px solid #dce4f3; border-radius:16px; background:#fff; box-shadow:0 7px 20px rgba(15,35,79,.05); }.ara-status-title { color:#172554; font-weight:800; }.ara-status-copy { margin-top:.2rem; color:#64748b; font-size:.82rem; }.ara-status-pill { padding:.35rem .7rem; border-radius:999px; color:#4338ca; background:#eef2ff; font-size:.72rem; font-weight:800; text-transform:capitalize; }
.stColumn .card { height:130px; }.stColumn .stButton>button { width:100%; }
.ara-provider-bar { display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:.8rem 1rem; margin:-.45rem 0 1.15rem; border:1px solid #dbe4f4; border-radius:14px; background:rgba(255,255,255,.92); box-shadow:0 6px 18px rgba(15,35,79,.05); }.ara-provider-label { color:#64748b; font-size:.78rem; font-weight:700; }.ara-provider-value { display:inline-flex; align-items:center; gap:.4rem; padding:.32rem .7rem; border-radius:999px; color:#4338ca; background:#eef2ff; font-size:.75rem; font-weight:800; }
.ara-info-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin:1rem 0 1.4rem; }.ara-info-card { padding:1.2rem; border:1px solid #dce4f3; border-radius:17px; background:#fff; box-shadow:0 8px 22px rgba(15,35,79,.06); }.ara-info-card h3 { margin:0 0 .45rem; color:#172554; font-size:1rem; }.ara-info-card p { margin:0; color:#64748b; font-size:.84rem; }.ara-chip { display:inline-flex; margin:.25rem .3rem .1rem 0; padding:.28rem .58rem; border-radius:999px; color:#475569; background:#f1f5f9; font-size:.68rem; font-weight:700; }
.ara-history-meta { display:flex; flex-wrap:wrap; gap:.4rem; margin:.65rem 0 .8rem; }.ara-history-title { color:#172554; font-size:.98rem; font-weight:800; line-height:1.45; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-color:#dce4f3!important; border-radius:17px!important; background:#fff; box-shadow:0 8px 22px rgba(15,35,79,.055); }
[data-testid="stHorizontalBlock"] { gap:1rem; }
.stRadio [role="radiogroup"] { gap:.5rem; }.stRadio [role="radiogroup"] label { padding:.5rem .8rem; border:1px solid #dce4f3; border-radius:10px; background:#fff; }.stRadio [role="radiogroup"] label:has(input:checked) { border-color:#7c6adc; background:#f1efff; }
.ara-settings-panel { padding:1.35rem; margin:.6rem 0 1.2rem; border:1px solid #dce4f3; border-radius:17px; background:linear-gradient(145deg,#fff,#fafbff); box-shadow:0 8px 22px rgba(15,35,79,.055); }.ara-settings-panel-title { color:#172554; font-size:1.05rem; font-weight:800; }.ara-settings-panel-copy { margin-top:.35rem; color:#64748b; font-size:.86rem; }
.ara-report-title { padding:1rem 1.2rem; margin:.6rem 0 1rem; border-left:4px solid #6d4bd4; border-radius:0 14px 14px 0; color:#172554; background:#f6f4ff; font-size:1.05rem; font-weight:800; }.ara-analysis-document { padding:1.5rem; border:1px solid #dce4f3; border-radius:18px; background:#fff; box-shadow:0 10px 28px rgba(15,35,79,.06); }

div[data-testid="stMetric"] { min-height:116px; padding:1rem 1.15rem; border:1px solid #dce4f3; border-radius:17px; background:linear-gradient(145deg,#fff,#f8faff); box-shadow:0 8px 22px rgba(15,35,79,.06); }
div[data-testid="stMetricValue"] { color:#172554; font-size:1.65rem; font-weight:800; }
div[data-testid="stMetricLabel"] { color:#64748b; font-weight:650; }

.stButton>button, .stDownloadButton>button { min-height:42px; border-radius:11px; font-weight:700; border:1px solid transparent; }
.stButton>button[kind="primary"] { background:linear-gradient(110deg,#2563eb,#7137c8); box-shadow:0 8px 18px rgba(69,70,196,.20); }
.stButton>button:hover { transform:translateY(-1px); border-color:#6d4bd4; box-shadow:0 9px 20px rgba(69,70,196,.15); }
.stDownloadButton>button { color:#fff; background:linear-gradient(110deg,#15803d,#16a34a); }

div[data-testid="stFileUploader"] { padding:1rem; border:1px solid #d9e2f2; border-radius:18px; background:#fff; box-shadow:0 8px 24px rgba(15,35,79,.05); }
section[data-testid="stFileUploaderDropzone"] { min-height:120px; border:1.5px dashed #8aa5dc; border-radius:14px; background:linear-gradient(135deg,#f7faff,#faf8ff); }
.stTextInput input, .stTextArea textarea, .stNumberInput input { min-height:44px; border-color:#d6dfef; border-radius:11px; background:#fff; }
.stSelectbox [data-baseweb="select"], .stDateInput input { border-color:#d6dfef; border-radius:11px; background:#fff; }
[data-testid="stExpander"] { border:1px solid #dce4f3; border-radius:14px; background:#fff; box-shadow:0 5px 16px rgba(15,35,79,.04); }
[data-testid="stAlert"] { border-radius:13px; border-left-width:4px; }
[data-testid="stProgress"] > div > div { background:linear-gradient(90deg,#2563eb,#7c3aed); }

section[data-testid="stSidebar"] { background:linear-gradient(180deg,#0b1f48 0%,#14275b 55%,#281b58 100%); border-right:0; box-shadow:8px 0 28px rgba(15,23,42,.16); }
section[data-testid="stSidebar"] .block-container { padding:1.4rem .9rem 1.5rem; }
section[data-testid="stSidebar"] * { color:#dbe7ff; }
.ara-side-brand { padding:1rem .85rem 1.25rem; margin-bottom:1rem; border-bottom:1px solid rgba(255,255,255,.13); }
.ara-side-mark { display:grid; place-items:center; width:44px; height:44px; margin-bottom:.75rem; border-radius:13px; background:linear-gradient(135deg,#fff,#e9edff); color:#3158ca !important; font-size:1.35rem; box-shadow:0 8px 22px rgba(0,0,0,.18); }
.ara-side-name { color:#fff !important; font-size:1rem; font-weight:800; line-height:1.25; }
.ara-side-subtitle { margin-top:.3rem; color:#aebfe8 !important; font-size:.72rem; line-height:1.4; }
.ara-side-version { display:inline-block; margin-top:.7rem; padding:.2rem .5rem; border-radius:999px; background:rgba(255,255,255,.09); color:#c9d6f4 !important; font-size:.65rem; }
section[data-testid="stSidebar"] [role="radiogroup"] { gap:.35rem; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label { min-height:42px; padding:.55rem .65rem; border:1px solid transparent; border-radius:11px; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(255,255,255,.08); border-color:rgba(255,255,255,.10); }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background:linear-gradient(100deg,rgba(60,112,255,.36),rgba(133,70,210,.34)); border-color:rgba(176,192,255,.30); }
section[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.12); }

.ara-footer { margin-top:2.5rem; padding:1.2rem 1.4rem; border:1px solid #dce4f3; border-radius:16px; background:#fff; box-shadow:0 6px 20px rgba(15,35,79,.05); }
.ara-footer-divider { display:none; }
.ara-footer-content { display:flex; align-items:center; justify-content:space-between; gap:1rem; color:#64748b; font-size:.78rem; }
.ara-footer-left { display:flex; align-items:center; gap:.55rem; }
.ara-footer-left strong,.ara-footer-right strong { color:#172554; }
.empty-state { padding:2rem; text-align:center; border:1px solid #dce4f3; border-radius:18px; background:linear-gradient(145deg,#fff,#f8faff); box-shadow:0 8px 24px rgba(15,35,79,.06); }
.empty-state-icon { font-size:2rem; }.empty-state-title { margin-top:.65rem; color:#172554; font-size:1.1rem; font-weight:800; }.empty-state-message { margin-top:.35rem; color:#64748b; }
.badge,.ai-badge { display:inline-flex; padding:.3rem .65rem; border-radius:999px; font-size:.72rem; font-weight:750; }.badge-info { color:#dbeafe; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18); }
code { border-radius:7px; color:#5b21b6; background:#f1edff; }.stCodeBlock { border:1px solid #dce4f3; border-radius:14px; overflow:hidden; }

@media(max-width:800px){
  .main .block-container{padding:1.25rem 1rem 3rem}.hero,.ara-page-hero{padding:1.5rem}.hero-title,.ara-page-title{font-size:1.6rem}.ara-footer-content{align-items:flex-start;flex-direction:column}
  .ara-info-grid{grid-template-columns:1fr}.ara-provider-bar{align-items:flex-start;flex-direction:column}
}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important;animation:none!important}}

/* -------------------------------------------------------------------------
   Interface refinement: quiet hierarchy, compact navigation and actions
   ------------------------------------------------------------------------- */
.main .block-container {
    padding-top: 1.55rem;
}

.hero, .ara-page-hero {
    min-height: 0;
    margin-bottom: 1.35rem;
    padding: 1.55rem 1.8rem;
    border-radius: 18px;
    box-shadow: 0 12px 30px rgba(31, 56, 133, .16);
}
.hero::after, .ara-page-hero::after {
    width: 190px;
    height: 190px;
    top: -108px;
    right: -38px;
    border-width: 28px;
}
.hero-title, .ara-page-title {
    font-size: 1.65rem;
    line-height: 1.2;
}
.hero-subtitle, .ara-page-description {
    margin-top: .35rem;
    font-size: .86rem;
}
.ara-page-kicker {
    margin-bottom: .5rem;
    padding: .22rem .55rem;
    font-size: .62rem;
}

/* Default actions are deliberately neutral. Only explicit primary actions
   receive the brand gradient. This restores a professional action hierarchy. */
.stButton > button,
.stDownloadButton > button {
    min-height: 39px;
    border: 1px solid #cad5e8 !important;
    border-radius: 9px;
    color: #23345d !important;
    background: #ffffff !important;
    box-shadow: 0 2px 6px rgba(15, 35, 79, .04);
    font-size: .82rem;
    font-weight: 700;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #5b67c8 !important;
    color: #3446a8 !important;
    background: #f7f8ff !important;
    box-shadow: 0 5px 14px rgba(38, 52, 126, .10);
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    border-color: transparent !important;
    color: #ffffff !important;
    background: linear-gradient(110deg, #245fda, #6342c8) !important;
    box-shadow: 0 7px 16px rgba(56, 68, 180, .20);
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    color: #ffffff !important;
    background: linear-gradient(110deg, #1e50bd, #5435b2) !important;
}

/* History action semantics. Streamlit exposes widget keys as wrapper classes. */
[class*="st-key-d"] .stButton > button {
    border-color: #fecaca !important;
    color: #b42318 !important;
    background: #fffafa !important;
}
[class*="st-key-d"] .stButton > button:hover {
    border-color: #ef4444 !important;
    color: #991b1b !important;
    background: #fff1f2 !important;
}
[class*="st-key-v"] .stButton > button {
    border-color: #b8c7eb !important;
    color: #294b9b !important;
    background: #f8faff !important;
}

/* Remove inherited white pills from the dark sidebar. */
section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    color: #9fb1d8 !important;
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
}
section[data-testid="stSidebar"] [role="radiogroup"] {
    gap: .2rem !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label {
    min-height: 40px;
    padding: .48rem .62rem;
    border: 1px solid transparent !important;
    border-radius: 9px;
    color: #d8e4fb !important;
    background: transparent !important;
    font-size: .82rem;
    font-weight: 600;
    text-transform: none;
    letter-spacing: 0;
}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    border-color: rgba(255,255,255,.10) !important;
    color: #ffffff !important;
    background: rgba(255,255,255,.07) !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    border-color: rgba(157, 176, 255, .28) !important;
    color: #ffffff !important;
    background: linear-gradient(100deg, rgba(52, 105, 230, .34), rgba(118, 67, 196, .30)) !important;
    box-shadow: inset 3px 0 0 #8aa8ff;
}
section[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: inherit !important;
    font-size: inherit !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] {
    color: inherit !important;
}
section[data-testid="stSidebar"] [role="radio"] {
    transform: scale(.82);
    opacity: .78;
}

.ara-provider-bar {
    margin: 0 0 1rem;
    padding: .72rem .9rem;
    border-radius: 12px;
    box-shadow: none;
}
.ara-provider-label { font-size: .66rem; letter-spacing: .05em; }
.ara-provider-value { font-size: .69rem; }

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important;
    box-shadow: 0 5px 16px rgba(15, 35, 79, .045);
}
.ara-history-title {
    font-size: .93rem;
    line-height: 1.4;
}
.ara-history-meta {
    margin: .55rem 0 .65rem;
}
.ara-chip {
    margin: 0;
    padding: .24rem .5rem;
    color: #526078;
    background: #f2f5fa;
    font-size: .64rem;
}

@media (max-width: 800px) {
    .hero, .ara-page-hero { padding: 1.25rem; border-radius: 15px; }
    .hero-title, .ara-page-title { font-size: 1.38rem; }
}
"""

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

