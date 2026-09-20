"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/theme/color_palette.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Provides a structured color palette access layer for the UI design system.

    This module acts as a bridge between raw color definitions and higher-level
    design tokens/components. It provides semantic access to application colors
    without exposing internal color storage details.

Responsibilities:
    • Provide convenient palette access.
    • Manage active theme palette selection.
    • Expose semantic color groups.
    • Provide utility methods for UI components.
    • Keep color usage consistent across the application.

Non-Responsibilities:
    • Generate CSS.
    • Render UI components.
    • Handle Streamlit operations.
    • Manage theme persistence.

Dependencies:
    • app.ui.theme.colors

Used By:
    • design_tokens.py
    • css_builder.py
    • UI components.
    • Theme facade.

Status:
    Production Foundation Module

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.ui.theme.colors import ColorPalette
from app.ui.theme.colors import Colors


@dataclass(frozen=True)
class SemanticColors:
    """
    Semantic color grouping.

    Provides meaningful names instead of raw color values.
    """

    success: str
    warning: str
    error: str
    info: str


@dataclass(frozen=True)
class SurfaceColors:
    """
    Application surface color grouping.
    """

    background: str
    surface: str
    elevated: str


@dataclass(frozen=True)
class TextColors:
    """
    Application typography color grouping.
    """

    primary: str
    secondary: str
    muted: str
    inverse: str


@dataclass(frozen=True)
class BorderColors:
    """
    Border color grouping.
    """

    default: str
    light: str


class ColorPaletteManager:
    """
    Provides access to application color palettes.

    This class prevents direct dependency on the internal color registry.

    Example:

        palette = ColorPaletteManager.light()

        button_color = palette.primary
        error_color = palette.semantic.error
    """

    def __init__(
        self,
        palette: ColorPalette,
    ) -> None:
        """
        Initialize palette manager.

        Args:
            palette:
                Active ColorPalette instance.
        """

        self._palette = palette

    @property
    def primary(self) -> str:
        """Primary brand color."""
        return self._palette.primary

    @property
    def secondary(self) -> str:
        """Secondary brand color."""
        return self._palette.secondary

    @property
    def accent(self) -> str:
        """Accent color."""
        return self._palette.accent

    @property
    def semantic(self) -> SemanticColors:
        """
        Semantic application colors.
        """

        return SemanticColors(
            success=self._palette.success,
            warning=self._palette.warning,
            error=self._palette.error,
            info=self._palette.info,
        )

    @property
    def surfaces(self) -> SurfaceColors:
        """
        Surface colors.
        """

        return SurfaceColors(
            background=self._palette.background,
            surface=self._palette.surface,
            elevated=self._palette.surface_elevated,
        )

    @property
    def text(self) -> TextColors:
        """
        Text colors.
        """

        return TextColors(
            primary=self._palette.text_primary,
            secondary=self._palette.text_secondary,
            muted=self._palette.text_muted,
            inverse=self._palette.text_inverse,
        )

    @property
    def borders(self) -> BorderColors:
        """
        Border colors.
        """

        return BorderColors(
            default=self._palette.border,
            light=self._palette.border_light,
        )

    @property
    def disabled(self) -> str:
        """
        Disabled UI element color.
        """

        return self._palette.disabled

    @property
    def charts(self) -> dict[str, str]:
        """
        Chart visualization colors.

        Returns:
            Mapping of chart semantic colors.
        """

        return {
            "primary": self._palette.chart_primary,
            "secondary": self._palette.chart_secondary,
            "success": self._palette.chart_success,
            "warning": self._palette.chart_warning,
            "error": self._palette.chart_error,
        }

    @property
    def raw(self) -> ColorPalette:
        """
        Return underlying palette.

        Useful for advanced integrations.
        """

        return self._palette

    @classmethod
    def light(cls) -> "ColorPaletteManager":
        """
        Create light theme palette manager.
        """

        return cls(Colors.LIGHT)

    @classmethod
    def dark(cls) -> "ColorPaletteManager":
        """
        Create dark theme palette manager.
        """

        return cls(Colors.DARK)

    @classmethod
    def from_mode(
        cls,
        mode: str,
    ) -> "ColorPaletteManager":
        """
        Create palette from theme mode.

        Args:
            mode:
                light or dark

        Returns:
            ColorPaletteManager instance.
        """

        return cls(
            Colors.get(mode)
        )


# =============================================================================
# Public Palette Instances
# =============================================================================

LIGHT_PALETTE = ColorPaletteManager.light()

DARK_PALETTE = ColorPaletteManager.dark()


# Backward-compatible color access
#
# Used by:
#   app.ui.theme.__init__
#   legacy UI components
#

COLORS = {
    "light": LIGHT_PALETTE,
    "dark": DARK_PALETTE,
}


__all__ = [
    "SemanticColors",
    "SurfaceColors",
    "TextColors",
    "BorderColors",
    "ColorPaletteManager",
    "LIGHT_PALETTE",
    "DARK_PALETTE",
    "COLORS",
]