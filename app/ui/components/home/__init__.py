"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/home/__init__.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Home page component package initialization.

Responsibilities:
    - Expose Home page UI components.
    - Provide clean import boundaries.
    - Maintain modular Streamlit UI architecture.

Non-Responsibilities:
    - Business logic.
    - Data access.
    - AI processing.
    - Pipeline execution.

===============================================================================
"""

from __future__ import annotations


from app.ui.components.home.developer_card import (
    DeveloperCard,
    render_developer_card,
)

from app.ui.components.home.feature_card import (
    FeatureCard,
    render_feature_card,
)

from app.ui.components.home.highlights import (
    Highlight,
    Highlights,
    render_highlights,
)

from app.ui.components.home.hero_section import (
    HeroSection,
    render_hero_section,
)

from app.ui.components.home.research_domains import (
    ResearchDomains,
    render_research_domains,
)

from app.ui.components.home.statistics_panel import (
    StatisticItem,
    StatisticsPanel,
    render_statistics_panel,
)

from app.ui.components.home.technology_stack import (
    TechnologyStack,
    render_technology_stack,
)

from app.ui.components.home.workflow import (
    Workflow,
    WorkflowStep,
    render_workflow,
)


__version__ = "1.0.0"


__all__ = [
    # Hero
    "HeroSection",
    "render_hero_section",

    # Statistics
    "StatisticItem",
    "StatisticsPanel",
    "render_statistics_panel",

    # Features
    "FeatureCard",
    "render_feature_card",

    # Highlights
    "Highlight",
    "Highlights",
    "render_highlights",

    # Research domains
    "ResearchDomains",
    "render_research_domains",

    # Workflow
    "Workflow",
    "WorkflowStep",
    "render_workflow",

    # Technology
    "TechnologyStack",
    "render_technology_stack",

    # Developer
    "DeveloperCard",
    "render_developer_card",
]