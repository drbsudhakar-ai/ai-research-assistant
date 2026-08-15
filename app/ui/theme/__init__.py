"""
Public interface for the AI Research Assistant UI theme system.
"""

from app.ui.theme.color_palette import (
    ColorPalette,
)
from app.ui.theme.colors import (
    Colors,
)
from app.ui.theme.components import (
    COMPONENTS,
)
from app.ui.theme.css_builder import (
    CSSBuilder,
)
from app.ui.theme.design_tokens import (
    DesignTokens,
)
from app.ui.theme.spacing import (
    SPACING,
)
from app.ui.theme.theme_config import (
    UI_THEME,
)
from app.ui.theme.theme_manager import (
    ThemeConfig,
    ThemeManager,
    ThemeMode,
)
from app.ui.theme.typography import (
    TYPOGRAPHY,
    Typography,
)

COLORS = UI_THEME.colors

__all__ = [
    "COLORS",
    "COMPONENTS",
    "SPACING",
    "TYPOGRAPHY",
    "UI_THEME",
    "CSSBuilder",
    "ColorPalette",
    "Colors",
    "DesignTokens",
    "ThemeConfig",
    "ThemeManager",
    "ThemeMode",
    "Typography",
]

__version__ = "1.0.0"
