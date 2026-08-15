"""Branding configuration tests."""

from __future__ import annotations

from pathlib import Path

from app.config.app_config import APP_NAME, AUTHOR, CREDIT
from app.config.branding import BrandConfig, get_brand_config


def test_brand_config_required_identity() -> None:
    brand = get_brand_config()
    assert isinstance(brand, BrandConfig)
    assert brand.application_name == "AI Research Assistant"
    assert brand.author == "Dr. B. Sudhakar"
    assert brand.credit == "Developed by Dr. B. Sudhakar"
    assert brand.document_title
    assert brand.tagline
    assert brand.icon


def test_app_config_reexports_branding() -> None:
    brand = get_brand_config()
    assert APP_NAME == brand.application_name
    assert AUTHOR == brand.author
    assert CREDIT == brand.credit


def test_layout_and_report_modules_consume_brand_config() -> None:
    paths = [
        Path("app/ui/layout/header.py"),
        Path("app/ui/layout/footer.py"),
        Path("app/ui/layout/sidebar.py"),
        Path("app/reports/markdown_renderer.py"),
        Path("app/reports/html_renderer.py"),
        Path("app/reports/report_document.py"),
    ]
    for path in paths:
        source = path.read_text(encoding="utf-8")
        assert (
            "get_brand_config" in source
            or "BrandConfig" in source
            or "resolved_brand" in source
        )
        assert 'title: str = "AI Research Assistant"' not in source
        assert 'application: str = (\n        "AI Research Assistant"' not in source
