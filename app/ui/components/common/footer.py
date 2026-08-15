"""
===============================================================================
Project      : AI Research Assistant
File         : app/ui/components/common/footer.py
Version      : 1.0.0
Author       : Dr. B. Sudhakar

Description:
    Application footer UI component.

Responsibilities:
    - Render consistent application footer.
    - Display version and attribution information.
    - Provide professional branding area.

Non-Responsibilities:
    - Application configuration.
    - Navigation.
    - Business logic.

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.config.branding import get_brand_config
from app.ui.html_renderer import render_html
from app.ui.theme.theme_config import UI_THEME


@dataclass(frozen=True)
class Footer:
    """
    Represents application footer.

    Attributes:
        application_name:
            Application title.

        version:
            Application version.

        author:
            Creator information.

        note:
            Optional footer note.
    """

    application_name: str = ""
    version: str = ""
    author: str = ""

    note: str | None = None

    def render(self) -> None:
        """
        Render footer.
        """

        brand = get_brand_config()
        application_name = self.application_name or brand.application_name
        version = self.version or brand.version
        credit = brand.credit
        theme = UI_THEME
        color = theme.colors.TEXT_SECONDARY

        note_html = (
            f"""
            <div>
                {self.note}
            </div>
            """
            if self.note
            else ""
        )

        render_html(f"""
            <div class="app-footer"
                 style="
                    color:{color};
                    text-align:center;
                    padding:20px;
                 ">

                <hr>

                <div>
                    {application_name}
                    v{version}
                </div>

                <div>
                    {credit}
                </div>

                {note_html}

            </div>
            """)


def render_footer(
    *,
    application_name: str | None = None,
    version: str | None = None,
    author: str | None = None,
    note: str | None = None,
) -> None:
    """
    Functional helper for footer rendering.
    """

    brand = get_brand_config()
    footer = Footer(
        application_name=application_name or brand.application_name,
        version=version or brand.version,
        author=author or brand.author,
        note=note,
    )

    footer.render()


__all__ = [
    "Footer",
    "render_footer",
]
