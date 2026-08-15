"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/theme/colors.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Central color system for the AI Research Assistant UI design framework.

    This module defines all application colors in one place. It provides
    reusable color definitions for light and dark themes and prevents
    hardcoded colors throughout the application.

Responsibilities:
    • Define brand colors.
    • Define semantic colors.
    • Define surface and background colors.
    • Define text and border colors.
    • Provide light and dark theme palettes.
    • Provide chart and visualization colors.

Non-Responsibilities:
    • UI rendering.
    • CSS generation.
    • Theme switching.
    • Streamlit integration.

Dependencies:
    • Python Standard Library only.

Used By:
    • color_palette.py
    • design_tokens.py
    • css_builder.py
    • UI components.

Status:
    Production Foundation Module

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ColorName(str, Enum):
    """
    Semantic color identifiers used across the application.
    """

    PRIMARY = "primary"
    SECONDARY = "secondary"
    ACCENT = "accent"

    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"

    BACKGROUND = "background"
    SURFACE = "surface"
    SURFACE_ELEVATED = "surface_elevated"

    TEXT_PRIMARY = "text_primary"
    TEXT_SECONDARY = "text_secondary"
    TEXT_MUTED = "text_muted"
    TEXT_INVERSE = "text_inverse"

    BORDER = "border"
    BORDER_LIGHT = "border_light"

    DISABLED = "disabled"


@dataclass(frozen=True)
class ColorPalette:
    """
    Complete application color palette.

    All values are CSS-compatible color strings.
    """

    # Brand colors
    primary: str
    secondary: str
    accent: str

    # Semantic colors
    success: str
    warning: str
    error: str
    info: str

    # Backgrounds
    background: str
    surface: str
    surface_elevated: str

    # Text
    text_primary: str
    text_secondary: str
    text_muted: str
    text_inverse: str

    # Borders
    border: str
    border_light: str

    # Disabled state
    disabled: str

    # Data visualization colors
    chart_primary: str
    chart_secondary: str
    chart_success: str
    chart_warning: str
    chart_error: str


class Colors:
    """
    Application color registry.

    Usage:

        from app.ui.theme.colors import Colors

        background = Colors.LIGHT.background
        primary = Colors.DARK.primary
    """

    LIGHT = ColorPalette(
        # Brand
        primary="#2563EB",
        secondary="#7C3AED",
        accent="#06B6D4",

        # Semantic
        success="#16A34A",
        warning="#D97706",
        error="#DC2626",
        info="#0284C7",

        # Background
        background="#F8FAFC",
        surface="#FFFFFF",
        surface_elevated="#F1F5F9",

        # Text
        text_primary="#0F172A",
        text_secondary="#334155",
        text_muted="#64748B",
        text_inverse="#FFFFFF",

        # Borders
        border="#CBD5E1",
        border_light="#E2E8F0",

        # Disabled
        disabled="#94A3B8",

        # Charts
        chart_primary="#2563EB",
        chart_secondary="#7C3AED",
        chart_success="#16A34A",
        chart_warning="#D97706",
        chart_error="#DC2626",
    )

    DARK = ColorPalette(
        # Brand
        primary="#60A5FA",
        secondary="#A78BFA",
        accent="#22D3EE",

        # Semantic
        success="#4ADE80",
        warning="#FBBF24",
        error="#F87171",
        info="#38BDF8",

        # Background
        background="#020617",
        surface="#0F172A",
        surface_elevated="#1E293B",

        # Text
        text_primary="#F8FAFC",
        text_secondary="#CBD5E1",
        text_muted="#94A3B8",
        text_inverse="#020617",

        # Borders
        border="#334155",
        border_light="#475569",

        # Disabled
        disabled="#64748B",

        # Charts
        chart_primary="#60A5FA",
        chart_secondary="#A78BFA",
        chart_success="#4ADE80",
        chart_warning="#FBBF24",
        chart_error="#F87171",
    )

    @classmethod
    def get(cls, mode: str = "light") -> ColorPalette:
        """
        Retrieve a theme palette.

        Args:
            mode:
                Theme mode name.

        Returns:
            ColorPalette instance.

        Raises:
            ValueError:
                If an unsupported theme is requested.
        """

        normalized = mode.lower().strip()

        if normalized == "light":
            return cls.LIGHT

        if normalized == "dark":
            return cls.DARK

        raise ValueError(
            f"Unsupported color theme: {mode}. "
            "Supported themes: light, dark."
        )