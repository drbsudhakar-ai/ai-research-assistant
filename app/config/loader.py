"""Load and cache the canonical ApplicationConfig.

Precedence (highest wins):

1. explicit runtime overrides passed to ``load_application_config``
2. environment variables (including values from an optional ``.env`` file
   that does not override already-exported variables)
3. safe application defaults

``SettingsManager`` persisted JSON is **not** auto-merged. That file is
user-editable API settings for the Settings UI (T016). Auto-applying it
would change the current live analysis defaults.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from app.config.application_config import (
    DEFAULT_GEMINI_BASE_URL,
    PROJECT_ROOT,
    ApplicationConfig,
    default_application_config,
    merge_application_config,
    validate_application_config,
)
from app.config.env_names import (
    ENV_CONFIG_DIR,
    ENV_DATA_DIR,
    ENV_DATABASE_PATH,
    ENV_DEBUG,
    ENV_DEVELOPER_MODE,
    ENV_ENVIRONMENT,
    ENV_EXPORT_DEFAULT_FORMAT,
    ENV_LLM_API_KEY,
    ENV_LLM_BASE_URL,
    ENV_LLM_CONNECT_TIMEOUT,
    ENV_LLM_MAX_INPUT_CHARACTERS,
    ENV_LLM_MAX_RETRIES,
    ENV_LLM_MAX_TOKENS,
    ENV_LLM_MODEL,
    ENV_LLM_PROVIDER,
    ENV_LLM_TEMPERATURE,
    ENV_LLM_TIMEOUT,
    ENV_LLM_TOP_P,
    ENV_LOG_FILE,
    ENV_LOG_LEVEL,
    ENV_LOGS_DIR,
    ENV_REPORTS_DIR,
    ENV_TEMP_DIR,
    ENV_UPLOADS_DIR,
)
from app.config.exceptions import ConfigurationError

_LOGGER = logging.getLogger(__name__)
_current: ApplicationConfig | None = None


def load_dotenv_file(path: Path | None = None) -> None:
    """Load ``.env`` if python-dotenv is installed. Existing env wins."""

    dotenv_path = path or (PROJECT_ROOT / ".env")
    if not dotenv_path.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(dotenv_path, override=False)


def load_application_config(
    *,
    environ: Mapping[str, str] | None = None,
    overrides: Mapping[str, Any] | None = None,
    dotenv_path: Path | None = None,
    load_dotenv: bool = True,
    set_as_current: bool = True,
) -> ApplicationConfig:
    """Build a validated ApplicationConfig from defaults, env, and overrides."""

    if load_dotenv and environ is None:
        load_dotenv_file(dotenv_path)

    source = environ if environ is not None else os.environ
    config = default_application_config()
    env_overrides = _overrides_from_environ(
        source, project_root=config.paths.project_root
    )
    if env_overrides:
        config = merge_application_config(config, env_overrides)
    if overrides:
        config = merge_application_config(config, overrides)
    config = validate_application_config(config)
    if set_as_current:
        return set_application_config(config)
    return config


def get_application_config() -> ApplicationConfig:
    """Return the process configuration, loading defaults/env on first use."""

    if _current is None:
        return load_application_config()
    return _current


def set_application_config(config: ApplicationConfig) -> ApplicationConfig:
    """Replace the process-wide configuration after validation."""

    global _current
    _current = validate_application_config(config)
    return _current


def reset_application_config() -> None:
    """Clear the cached configuration. Intended for tests."""

    global _current
    _current = None


def configure_logging(config: ApplicationConfig | None = None) -> None:
    """Apply logging level and optional file handler. Secrets are not logged."""

    resolved = config or get_application_config()
    level = getattr(logging, resolved.logging.level)
    logging.basicConfig(level=level, force=True)
    if resolved.logging.log_file is not None:
        resolved.logging.log_file.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(resolved.logging.log_file, encoding="utf-8")
        handler.setLevel(level)
        logging.getLogger().addHandler(handler)
    _LOGGER.debug("Application configuration loaded: %s", resolved.to_safe_dict())


def ensure_runtime_directories(config: ApplicationConfig | None = None) -> None:
    """Create data/upload/temp/report/log directories if missing."""

    resolved = config or get_application_config()
    for path in (
        resolved.paths.data_dir,
        resolved.paths.uploads_dir,
        resolved.paths.temp_dir,
        resolved.paths.reports_dir,
        resolved.paths.logs_dir,
        resolved.paths.config_dir,
        resolved.database.path.parent,
    ):
        path.mkdir(parents=True, exist_ok=True)


def _overrides_from_environ(
    environ: Mapping[str, str],
    *,
    project_root: Path,
) -> dict[str, Any]:
    application: dict[str, Any] = {}
    llm: dict[str, Any] = {}
    database: dict[str, Any] = {}
    paths: dict[str, Any] = {}
    export: dict[str, Any] = {}
    logging_cfg: dict[str, Any] = {}

    if ENV_ENVIRONMENT in environ:
        application["environment"] = environ[ENV_ENVIRONMENT]
    if ENV_DEVELOPER_MODE in environ:
        application["developer_mode"] = _parse_bool(
            environ[ENV_DEVELOPER_MODE],
            field=ENV_DEVELOPER_MODE,
        )
    if ENV_DEBUG in environ:
        application["debug"] = _parse_bool(environ[ENV_DEBUG], field=ENV_DEBUG)

    if ENV_LLM_PROVIDER in environ:
        llm["provider"] = environ[ENV_LLM_PROVIDER]
    if ENV_LLM_MODEL in environ:
        llm["model"] = environ[ENV_LLM_MODEL]
    if ENV_LLM_BASE_URL in environ:
        llm["base_url"] = environ[ENV_LLM_BASE_URL]
    elif str(llm.get("provider", "")).strip().lower() == "gemini":
        llm["base_url"] = DEFAULT_GEMINI_BASE_URL
    if ENV_LLM_API_KEY in environ:
        llm["api_key"] = environ[ENV_LLM_API_KEY]
    if ENV_LLM_TEMPERATURE in environ:
        llm["temperature"] = _parse_float(
            environ[ENV_LLM_TEMPERATURE],
            field=ENV_LLM_TEMPERATURE,
        )
    if ENV_LLM_TOP_P in environ:
        llm["top_p"] = _parse_float(environ[ENV_LLM_TOP_P], field=ENV_LLM_TOP_P)
    if ENV_LLM_MAX_TOKENS in environ:
        llm["max_tokens"] = _parse_int(
            environ[ENV_LLM_MAX_TOKENS],
            field=ENV_LLM_MAX_TOKENS,
        )
    if ENV_LLM_TIMEOUT in environ:
        llm["timeout_seconds"] = _parse_int(
            environ[ENV_LLM_TIMEOUT],
            field=ENV_LLM_TIMEOUT,
        )
    if ENV_LLM_CONNECT_TIMEOUT in environ:
        llm["connect_timeout_seconds"] = _parse_int(
            environ[ENV_LLM_CONNECT_TIMEOUT],
            field=ENV_LLM_CONNECT_TIMEOUT,
        )
    if ENV_LLM_MAX_RETRIES in environ:
        llm["max_retries"] = _parse_int(
            environ[ENV_LLM_MAX_RETRIES],
            field=ENV_LLM_MAX_RETRIES,
        )
    if ENV_LLM_MAX_INPUT_CHARACTERS in environ:
        llm["max_input_characters"] = _parse_int(
            environ[ENV_LLM_MAX_INPUT_CHARACTERS],
            field=ENV_LLM_MAX_INPUT_CHARACTERS,
        )

    if ENV_DATABASE_PATH in environ:
        database["path"] = _resolve_path(environ[ENV_DATABASE_PATH], project_root)

    if ENV_DATA_DIR in environ:
        data_dir = _resolve_path(environ[ENV_DATA_DIR], project_root)
        paths["data_dir"] = data_dir
        if ENV_UPLOADS_DIR not in environ:
            paths["uploads_dir"] = data_dir / "uploads"
        if ENV_TEMP_DIR not in environ:
            paths["temp_dir"] = data_dir / "tmp"
        if ENV_REPORTS_DIR not in environ:
            paths["reports_dir"] = data_dir / "reports"
        if ENV_LOGS_DIR not in environ:
            paths["logs_dir"] = data_dir / "logs"
        if ENV_DATABASE_PATH not in environ:
            database["path"] = data_dir / "history.db"
    if ENV_UPLOADS_DIR in environ:
        paths["uploads_dir"] = _resolve_path(environ[ENV_UPLOADS_DIR], project_root)
    if ENV_TEMP_DIR in environ:
        paths["temp_dir"] = _resolve_path(environ[ENV_TEMP_DIR], project_root)
    if ENV_REPORTS_DIR in environ:
        paths["reports_dir"] = _resolve_path(environ[ENV_REPORTS_DIR], project_root)
    if ENV_LOGS_DIR in environ:
        paths["logs_dir"] = _resolve_path(environ[ENV_LOGS_DIR], project_root)
    if ENV_CONFIG_DIR in environ:
        config_dir = _resolve_path(environ[ENV_CONFIG_DIR], project_root)
        paths["config_dir"] = config_dir
        paths["settings_file"] = config_dir / "settings.json"

    if ENV_EXPORT_DEFAULT_FORMAT in environ:
        export["default_format"] = environ[ENV_EXPORT_DEFAULT_FORMAT]

    if ENV_LOG_LEVEL in environ:
        logging_cfg["level"] = environ[ENV_LOG_LEVEL]
    if ENV_LOG_FILE in environ:
        logging_cfg["log_file"] = _resolve_path(environ[ENV_LOG_FILE], project_root)

    overrides: dict[str, Any] = {}
    if application:
        overrides["application"] = application
    if llm:
        overrides["llm"] = llm
    if database:
        overrides["database"] = database
    if paths:
        overrides["paths"] = paths
    if export:
        overrides["export"] = export
    if logging_cfg:
        overrides["logging"] = logging_cfg
    return overrides


def _resolve_path(value: str, project_root: Path) -> Path:
    path = Path(value.strip())
    if not path.is_absolute():
        path = project_root / path
    return path


def _parse_bool(value: str, *, field: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"Invalid boolean for {field}: {value!r}.", field=field)


def _parse_int(value: str, *, field: str) -> int:
    try:
        return int(value.strip())
    except ValueError as exc:
        raise ConfigurationError(
            f"Invalid integer for {field}: {value!r}.", field=field
        ) from exc


def _parse_float(value: str, *, field: str) -> float:
    try:
        return float(value.strip())
    except ValueError as exc:
        raise ConfigurationError(
            f"Invalid number for {field}: {value!r}.", field=field
        ) from exc
