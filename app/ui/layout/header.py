"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Layout System
File         : app/ui/layout/header.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Application header component.

    Responsibilities:
        - Render application branding.
        - Display application title and tagline.
        - Display version information.
        - Provide reusable top-level header layout.

    Non-Responsibilities:
        - Navigation logic.
        - Authentication.
        - Page-specific content.

Dependencies:
    Internal:
        - app.ui.theme
        - app.core.config (optional future integration)

    External:
        - streamlit
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.layout.header import render_header

    render_header()

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.config.branding import get_brand_config
from app.ui.html_renderer import render_html


@dataclass(frozen=True)
class Header:
    """
    Header configuration.

    Defaults come from BrandConfig. Do not hard-code product identity here.
    """

    title: str = field(default_factory=lambda: get_brand_config().application_name)
    tagline: str = field(default_factory=lambda: get_brand_config().tagline)
    version: str = field(default_factory=lambda: get_brand_config().version_label)
    icon: str = field(default_factory=lambda: get_brand_config().icon)


def render_header(
    config: Header | None = None,
) -> None:
    """
    Render application header.

    Args:
        config:
            Optional header configuration.
    """

    if config is None:
        brand = get_brand_config()
        config = Header(
            title=brand.application_name,
            tagline=brand.tagline,
            version=brand.version_label,
            icon=brand.icon,
        )

    render_html(f"""
        <div class="ara-header">

            <div class="ara-header-content">

                <div class="ara-header-brand">

                    <div class="ara-header-icon">
                        {config.icon}
                    </div>

                    <div>

                        <h1 class="ara-header-title">
                            {config.title}
                        </h1>

                        <p class="ara-header-tagline">
                            {config.tagline}
                        </p>

                    </div>

                </div>


                <div class="ara-header-version">

                    {config.version}

                </div>

            </div>

        </div>
        """)
