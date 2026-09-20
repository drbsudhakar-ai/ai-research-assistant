"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Theme System
File         : design_tokens.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Centralized design tokens for the Streamlit UI.

    Design tokens provide consistent visual values used across the application:
    - Colors
    - Typography
    - Spacing
    - Border radius
    - Shadows
    - Component dimensions

Purpose:
    - Avoid hardcoded UI styling values.
    - Maintain a professional and consistent application theme.
    - Provide a single source of truth for UI design decisions.

Usage:
    from app.ui.theme.design_tokens import DesignTokens

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class ColorTokens:
    """
    Color palette tokens.

    Values are intentionally separated from components so the complete
    application theme can be changed without modifying UI components.
    """

    PRIMARY: str = "#2563EB"
    PRIMARY_LIGHT: str = "#60A5FA"
    PRIMARY_DARK: str = "#1E40AF"

    SECONDARY: str = "#64748B"
    SECONDARY_LIGHT: str = "#CBD5E1"
    SECONDARY_DARK: str = "#334155"

    SUCCESS: str = "#16A34A"
    WARNING: str = "#F59E0B"
    ERROR: str = "#DC2626"
    INFO: str = "#0284C7"

    BACKGROUND: str = "#F8FAFC"
    SURFACE: str = "#FFFFFF"
    CARD_BACKGROUND: str = "#FFFFFF"

    TEXT_PRIMARY: str = "#0F172A"
    TEXT_SECONDARY: str = "#475569"
    TEXT_MUTED: str = "#64748B"

    BORDER: str = "#E2E8F0"
    DIVIDER: str = "#CBD5E1"


@dataclass(frozen=True)
class TypographyTokens:
    """
    Typography scale tokens.
    """

    FONT_FAMILY: str = (
        "Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
    )

    FONT_SIZE_SMALL: str = "0.875rem"
    FONT_SIZE_BODY: str = "1rem"
    FONT_SIZE_MEDIUM: str = "1.125rem"
    FONT_SIZE_LARGE: str = "1.5rem"
    FONT_SIZE_XLARGE: str = "2rem"
    FONT_SIZE_TITLE: str = "2.5rem"

    FONT_WEIGHT_NORMAL: int = 400
    FONT_WEIGHT_MEDIUM: int = 500
    FONT_WEIGHT_SEMIBOLD: int = 600
    FONT_WEIGHT_BOLD: int = 700


@dataclass(frozen=True)
class SpacingTokens:
    """
    Standard spacing scale.
    """

    XS: str = "0.25rem"
    SM: str = "0.5rem"
    MD: str = "1rem"
    LG: str = "1.5rem"
    XL: str = "2rem"
    XXL: str = "3rem"


@dataclass(frozen=True)
class BorderTokens:
    """
    Border and radius tokens.
    """

    RADIUS_SMALL: str = "4px"
    RADIUS_MEDIUM: str = "8px"
    RADIUS_LARGE: str = "12px"
    RADIUS_ROUNDED: str = "999px"

    BORDER_WIDTH: str = "1px"


@dataclass(frozen=True)
class ShadowTokens:
    """
    Shadow definitions.
    """

    SMALL: str = (
        "0 1px 2px rgba(0, 0, 0, 0.05)"
    )

    MEDIUM: str = (
        "0 4px 6px rgba(0, 0, 0, 0.08)"
    )

    LARGE: str = (
        "0 10px 20px rgba(0, 0, 0, 0.12)"
    )


@dataclass(frozen=True)
class ComponentTokens:
    """
    Common component dimensions.
    """

    BUTTON_HEIGHT: str = "2.5rem"

    INPUT_HEIGHT: str = "2.75rem"

    CARD_PADDING: str = "1.25rem"

    PAGE_MAX_WIDTH: str = "1200px"

    SIDEBAR_WIDTH: str = "280px"


@dataclass(frozen=True)
class AnimationTokens:
    """
    Animation timing tokens.
    """

    FAST: str = "150ms"

    NORMAL: str = "300ms"

    SLOW: str = "500ms"

    TRANSITION: str = (
        "all 300ms ease-in-out"
    )


@dataclass(frozen=True)
class DesignTokens:
    """
    Root design token container.

    Import this class in UI components instead of individual token classes.
    """

    COLORS: Final = ColorTokens()

    TYPOGRAPHY: Final = TypographyTokens()

    SPACING: Final = SpacingTokens()

    BORDERS: Final = BorderTokens()

    SHADOWS: Final = ShadowTokens()

    COMPONENTS: Final = ComponentTokens()

    ANIMATIONS: Final = AnimationTokens()


# Global application design token instance
TOKENS: Final = DesignTokens()