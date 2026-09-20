"""
===============================================================================
Project      : AI Research Assistant
Module       : UI Layout System
File         : app/ui/layout/footer.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Application footer component.

    Responsibilities:
        - Render application footer.
        - Display version information.
        - Display author attribution.
        - Display technology information.
        - Provide future extension points for:
            * Documentation links
            * GitHub repository link
            * License information

    Non-Responsibilities:
        - Page content rendering.
        - Navigation handling.
        - Business logic.

Dependencies:
    Internal:
        - app.ui.theme

    External:
        - streamlit
        - Python >= 3.11
        - dataclasses (standard library)
        - typing (standard library)

Usage:
    from app.ui.layout.footer import render_footer

    render_footer()

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from app.config.branding import get_brand_config
from app.ui.html_renderer import render_html


@dataclass(frozen=True)
class Footer:
    """
    Footer configuration.

    Defaults come from BrandConfig. Do not hard-code product identity here.
    """

    application: str = field(
        default_factory=lambda: get_brand_config().application_name
    )
    version: str = field(default_factory=lambda: get_brand_config().version_label)
    author: str = field(default_factory=lambda: get_brand_config().author)
    technology: str = "Python • Streamlit • AI"


def render_footer(
    config: Footer | None = None,
) -> None:
    """
    Render application footer.

    Args:
        config:
            Optional footer configuration.
    """

    if config is None:
        brand = get_brand_config()
        config = Footer(
            application=brand.application_name,
            version=brand.version_label,
            author=brand.author,
        )

    render_html(f"""
        <div class="ara-footer">

            <div class="ara-footer-divider">
            </div>


            <div class="ara-footer-content">

                <div class="ara-footer-left">

                    <strong>
                        {config.application}
                    </strong>

                    <span>
                        {config.version}
                    </span>

                </div>


                <div class="ara-footer-center">

                    {config.technology}

                </div>


                <div class="ara-footer-right">

                    Developed by
                    <strong>
                        {config.author}
                    </strong>

                </div>

            </div>

        </div>
        """)


def render_minimal_footer(
    text: str,
) -> None:
    """
    Render simple footer text.

    Useful for small pages.

    Args:
        text:
            Footer message.
    """

    render_html(f"""
        <div class="ara-footer-minimal">

            {text}

        </div>
        """)


__all__: Final = [
    "Footer",
    "render_footer",
    "render_minimal_footer",
]
