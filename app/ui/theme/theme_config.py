"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme System
File         : app/ui/theme/theme_config.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Central theme configuration for the Streamlit application.

    This module provides a single access point for all UI theme resources:
        - Colors
        - Design tokens
        - Typography
        - Spacing
        - Component tokens
        - Streamlit CSS theme

Purpose:
    - Simplify theme imports across UI modules.
    - Maintain clean dependency boundaries.
    - Provide future support for:
        * Light theme
        * Dark theme
        * Custom user themes

Dependencies:
    Internal:
        - app.ui.theme.color_palette
        - app.ui.theme.components
        - app.ui.theme.design_tokens
        - app.ui.theme.spacing
        - app.ui.theme.streamlit_theme
        - app.ui.theme.typography

    External:
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.theme.theme_config import UI_THEME

    primary_color = UI_THEME.colors.PRIMARY

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


# from app.ui.theme.color_palette import COLORS
from app.ui.theme.components import COMPONENTS
from app.ui.theme.design_tokens import TOKENS
from app.ui.theme.spacing import SPACING
from app.ui.theme.streamlit_theme import apply_streamlit_theme
from app.ui.theme.typography import TYPOGRAPHY


@dataclass(frozen=True)
class ThemeMetadata:
    """
    Theme identification metadata.
    """

    NAME: str = "AI Research Assistant Professional"

    VERSION: str = "1.0.0"

    DESCRIPTION: str = (
        "Academic research intelligence interface theme."
    )


@dataclass(frozen=True)
class ThemeFeatures:
    """
    Enabled theme capabilities.
    """

    RESPONSIVE_LAYOUT: bool = True

    STREAMLIT_CSS: bool = True

    CARD_COMPONENTS: bool = True

    METRIC_COMPONENTS: bool = True

    ANALYSIS_RESULT_STYLING: bool = True


@dataclass(frozen=True)
class UITheme:
    """
    Complete UI theme configuration.

    This is the primary object consumed by UI modules.
    """

    metadata: Final = ThemeMetadata()

    features: Final = ThemeFeatures()

    colors: Final = TOKENS.COLORS

    tokens: Final = TOKENS

    typography: Final = TYPOGRAPHY

    spacing: Final = SPACING

    components: Final = COMPONENTS

    apply_css: Final = staticmethod(
        apply_streamlit_theme
    )


# Global theme instance
UI_THEME: Final = UITheme()


# =============================================================================
# Backward Compatibility
# =============================================================================

class ThemeConfig:
    """
    Backward-compatible wrapper for legacy UI components.

    Old code:
        theme = ThemeConfig()
        theme.colors.primary

    New code:
        UI_THEME.colors.PRIMARY
    """

    def __new__(cls):
        return UI_THEME