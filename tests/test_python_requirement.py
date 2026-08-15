"""Declared Python version vs StrEnum (no requirement change)."""

from __future__ import annotations

from pathlib import Path


def test_project_declares_python_3_11() -> None:
    enums = Path("app/settings/api/enums.py").read_text(encoding="utf-8")
    assert "3.11+" in enums
    navigation = Path("app/config/navigation_config.py").read_text(encoding="utf-8")
    assert "StrEnum" in navigation
