"""SettingsManager classification and secret-safe diagnostics."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.config.env_names import ENV_CONFIG_DIR
from app.config.loader import load_application_config, reset_application_config


@pytest.fixture(autouse=True)
def _reset_config() -> None:
    reset_application_config()
    yield
    reset_application_config()


def test_settings_manager_paths_follow_application_config(tmp_path: Path) -> None:
    config = load_application_config(
        environ={ENV_CONFIG_DIR: str(tmp_path / "cfg")},
        load_dotenv=False,
        set_as_current=True,
    )
    from app.config.settings_manager import SettingsManager

    SettingsManager._instance = None
    manager = SettingsManager()
    assert manager.config_path == config.paths.settings_file
    diagnostics = manager.safe_diagnostics()
    assert diagnostics["config_path"] == str(config.paths.settings_file)
    for provider in diagnostics["export"].get("providers", {}).values():
        assert provider.get("api_key", "") == ""
