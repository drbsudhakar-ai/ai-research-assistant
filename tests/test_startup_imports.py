"""Startup import path tests that avoid running Streamlit page config."""

from __future__ import annotations

import ast
from pathlib import Path


def test_streamlit_entry_imports_navigation_and_theme() -> None:
    source = Path("streamlit_app.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    assert "app.core.navigation" in imported
    assert "app.ui.theme" in imported
    assert "app.config.branding" in imported


def test_navigation_routes_cover_major_screens() -> None:
    source = Path("app/core/navigation.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assigned: dict[str, object] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "PAGE_ROUTES":
                    assigned["PAGE_ROUTES"] = ast.unparse(node.value)
    routes = assigned.get("PAGE_ROUTES", "")
    assert "PageKey.DASHBOARD" in routes
    assert "PageKey.ANALYZE" in routes
    assert "PageKey.HISTORY" in routes
    assert "PageKey.SETTINGS" in routes
    assert "PageKey.ABOUT" in routes
