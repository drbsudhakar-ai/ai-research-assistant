"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/shared/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Public interface for shared reusable UI components.

    Provides:

        - Hero banner component
        - Statistical metric cards
        - Status badge components

Usage:

    from app.ui.components.shared import (
        HeroBanner,
        StatCard,
        StatusBadge,
    )

===============================================================================
"""



# =============================================================================
# Hero Component
# =============================================================================

from app.ui.components.shared.hero_banner import (
    HeroBanner,
    HeroAction,
)



# =============================================================================
# Statistics Components
# =============================================================================

from app.ui.components.shared.stat_card import (
    StatCard,
    StatValue,
)



# =============================================================================
# Status Components
# =============================================================================

from app.ui.components.shared.status_badge import (
    StatusBadge,
    StatusType,
)



# =============================================================================
# Public API
# =============================================================================


__all__ = [

    # Hero
    "HeroBanner",
    "HeroAction",


    # Metrics
    "StatCard",
    "StatValue",


    # Status
    "StatusBadge",
    "StatusType",

]



__version__ = "1.0.0"