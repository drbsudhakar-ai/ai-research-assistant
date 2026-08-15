"""Canonical typed application configuration.

This module defines validated configuration objects. It does not read
environment variables; ``app.config.loader`` is the loading boundary.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from enum import StrEnum
from pathlib import Path
from typing import Any, Final
from urllib.parse import urlparse

from app.config.branding import BrandConfig, get_brand_config
from app.config.exceptions import ConfigurationError

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[2]

SUPPORTED_RUNTIME_PROVIDERS: Final[frozenset[str]] = frozenset({"ollama"})
SUPPORTED_EXPORT_FORMATS: Final[frozenset[str]] = frozenset({"markdown", "html"})
SUPPORTED_LOG_LEVELS: Final[frozenset[str]] = frozenset(
    {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}
)

DEFAULT_LLM_PROVIDER: Final[str] = "ollama"
DEFAULT_LLM_MODEL: Final[str] = "qwen3:4b"
DEFAULT_LLM_BASE_URL: Final[str] = "http://localhost:11434"
DEFAULT_TEMPERATURE: Final[float] = 0.2
DEFAULT_TOP_P: Final[float] = 0.95
DEFAULT_MAX_TOKENS: Final[int | None] = None
DEFAULT_TIMEOUT_SECONDS: Final[int] = 120
DEFAULT_CONNECT_TIMEOUT_SECONDS: Final[int] = 30
DEFAULT_MAX_RETRIES: Final[int] = 3
DEFAULT_MAX_INPUT_CHARACTERS: Final[int] = 10000
DEFAULT_EXPORT_FORMAT: Final[str] = "markdown"

SECRET_MASK: Final[str] = "********"


class AppEnvironment(StrEnum):
    """Process environment classification."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class ApplicationRuntimeConfig:
    """Process-level application settings."""

    name: str
    version: str
    environment: AppEnvironment = AppEnvironment.DEVELOPMENT
    developer_mode: bool = False
    debug: bool = False


@dataclass(frozen=True, slots=True)
class LLMRuntimeConfig:
    """Runtime LLM connection and generation settings.

    Live analysis currently uses Ollama only. Other provider names in
    ``app.settings.api`` are settings-UI catalogs, not runtime backends.
    """

    provider: str = DEFAULT_LLM_PROVIDER
    model: str = DEFAULT_LLM_MODEL
    base_url: str = DEFAULT_LLM_BASE_URL
    api_key: str = ""
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    max_tokens: int | None = DEFAULT_MAX_TOKENS
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    connect_timeout_seconds: int = DEFAULT_CONNECT_TIMEOUT_SECONDS
    max_retries: int = DEFAULT_MAX_RETRIES
    max_input_characters: int = DEFAULT_MAX_INPUT_CHARACTERS


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """SQLite history database settings."""

    engine: str = "sqlite"
    path: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "history.db")


@dataclass(frozen=True, slots=True)
class PathConfig:
    """Project filesystem locations resolved against the repository root."""

    project_root: Path = PROJECT_ROOT
    data_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data")
    uploads_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "uploads")
    temp_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "tmp")
    reports_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "reports")
    logs_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "data" / "logs")
    config_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "config")
    settings_file: Path = field(
        default_factory=lambda: PROJECT_ROOT / "config" / "settings.json"
    )


@dataclass(frozen=True, slots=True)
class ExportRuntimeConfig:
    """Report export settings for formats that already exist.

    PDF and DOCX generation is not implemented. Those flags stay false.
    """

    default_format: str = DEFAULT_EXPORT_FORMAT
    markdown_enabled: bool = True
    html_enabled: bool = True
    pdf_enabled: bool = False
    docx_enabled: bool = False
    include_metadata: bool = True


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Logging destination and level."""

    level: str = "INFO"
    log_file: Path | None = None


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    """Authoritative runtime configuration for the application process."""

    application: ApplicationRuntimeConfig
    llm: LLMRuntimeConfig
    database: DatabaseConfig
    paths: PathConfig
    export: ExportRuntimeConfig
    logging: LoggingConfig
    brand: BrandConfig = field(default_factory=get_brand_config)

    def to_safe_dict(self) -> dict[str, Any]:
        """Serialize configuration with secrets redacted."""

        return {
            "application": {
                "name": self.application.name,
                "version": self.application.version,
                "environment": self.application.environment.value,
                "developer_mode": self.application.developer_mode,
                "debug": self.application.debug,
            },
            "llm": {
                "provider": self.llm.provider,
                "model": self.llm.model,
                "base_url": self.llm.base_url,
                "api_key": SECRET_MASK if self.llm.api_key else "",
                "temperature": self.llm.temperature,
                "top_p": self.llm.top_p,
                "max_tokens": self.llm.max_tokens,
                "timeout_seconds": self.llm.timeout_seconds,
                "connect_timeout_seconds": self.llm.connect_timeout_seconds,
                "max_retries": self.llm.max_retries,
                "max_input_characters": self.llm.max_input_characters,
            },
            "database": {
                "engine": self.database.engine,
                "path": str(self.database.path),
            },
            "paths": {
                "project_root": str(self.paths.project_root),
                "data_dir": str(self.paths.data_dir),
                "uploads_dir": str(self.paths.uploads_dir),
                "temp_dir": str(self.paths.temp_dir),
                "reports_dir": str(self.paths.reports_dir),
                "logs_dir": str(self.paths.logs_dir),
                "config_dir": str(self.paths.config_dir),
                "settings_file": str(self.paths.settings_file),
            },
            "export": {
                "default_format": self.export.default_format,
                "markdown_enabled": self.export.markdown_enabled,
                "html_enabled": self.export.html_enabled,
                "pdf_enabled": self.export.pdf_enabled,
                "docx_enabled": self.export.docx_enabled,
                "include_metadata": self.export.include_metadata,
            },
            "logging": {
                "level": self.logging.level,
                "log_file": (
                    str(self.logging.log_file) if self.logging.log_file else None
                ),
            },
        }


def default_application_config(
    *, brand: BrandConfig | None = None
) -> ApplicationConfig:
    """Return validated defaults matching the current live application."""

    resolved_brand = brand or get_brand_config()
    config = ApplicationConfig(
        application=ApplicationRuntimeConfig(
            name=resolved_brand.application_name,
            version=resolved_brand.version,
        ),
        llm=LLMRuntimeConfig(),
        database=DatabaseConfig(),
        paths=PathConfig(),
        export=ExportRuntimeConfig(),
        logging=LoggingConfig(),
        brand=resolved_brand,
    )
    return validate_application_config(config)


def validate_application_config(config: ApplicationConfig) -> ApplicationConfig:
    """Validate configuration values. Does not probe provider availability."""

    provider = config.llm.provider.strip().lower()
    if provider not in SUPPORTED_RUNTIME_PROVIDERS:
        raise ConfigurationError(
            f"Unsupported runtime LLM provider '{config.llm.provider}'. "
            f"Live analysis supports: {', '.join(sorted(SUPPORTED_RUNTIME_PROVIDERS))}.",
            field="llm.provider",
        )

    model = config.llm.model.strip()
    if not model:
        raise ConfigurationError("LLM model name is required.", field="llm.model")

    _validate_http_url(config.llm.base_url, field="llm.base_url")

    if not 0.0 <= config.llm.temperature <= 2.0:
        raise ConfigurationError(
            "Temperature must be between 0 and 2.",
            field="llm.temperature",
        )

    if not 0.0 <= config.llm.top_p <= 1.0:
        raise ConfigurationError("top_p must be between 0 and 1.", field="llm.top_p")

    if config.llm.max_tokens is not None and config.llm.max_tokens < 1:
        raise ConfigurationError(
            "max_tokens must be positive when set.",
            field="llm.max_tokens",
        )

    if config.llm.timeout_seconds < 1:
        raise ConfigurationError(
            "timeout_seconds must be >= 1.", field="llm.timeout_seconds"
        )

    if config.llm.connect_timeout_seconds < 1:
        raise ConfigurationError(
            "connect_timeout_seconds must be >= 1.",
            field="llm.connect_timeout_seconds",
        )

    if config.llm.max_retries < 1:
        raise ConfigurationError("max_retries must be >= 1.", field="llm.max_retries")

    if config.llm.max_input_characters < 1:
        raise ConfigurationError(
            "max_input_characters must be >= 1.",
            field="llm.max_input_characters",
        )

    if config.database.engine != "sqlite":
        raise ConfigurationError(
            f"Unsupported database engine '{config.database.engine}'.",
            field="database.engine",
        )

    if not str(config.database.path).strip():
        raise ConfigurationError("Database path is required.", field="database.path")

    export_format = config.export.default_format.strip().lower()
    if export_format not in SUPPORTED_EXPORT_FORMATS:
        raise ConfigurationError(
            f"Unsupported export format '{config.export.default_format}'. "
            "Implemented formats: markdown, html.",
            field="export.default_format",
        )

    level = config.logging.level.strip().upper()
    if level not in SUPPORTED_LOG_LEVELS:
        raise ConfigurationError(
            f"Unsupported log level '{config.logging.level}'.",
            field="logging.level",
        )

    return replace(
        config,
        llm=replace(config.llm, provider=provider, model=model),
        export=replace(config.export, default_format=export_format),
        logging=replace(config.logging, level=level),
        database=replace(config.database, path=Path(config.database.path)),
    )


def merge_application_config(
    base: ApplicationConfig,
    overrides: Mapping[str, Any],
) -> ApplicationConfig:
    """Apply nested mapping overrides onto an existing configuration."""

    application = _merge_dataclass(base.application, overrides.get("application"))
    llm = _merge_dataclass(base.llm, overrides.get("llm"))
    database = _merge_dataclass(base.database, overrides.get("database"))
    paths = _merge_dataclass(base.paths, overrides.get("paths"))
    export = _merge_dataclass(base.export, overrides.get("export"))
    logging = _merge_dataclass(base.logging, overrides.get("logging"))
    return ApplicationConfig(
        application=application,
        llm=llm,
        database=database,
        paths=paths,
        export=export,
        logging=logging,
        brand=base.brand,
    )


def _merge_dataclass(instance: Any, values: Any) -> Any:
    if not values:
        return instance
    if not isinstance(values, Mapping):
        raise ConfigurationError("Override sections must be mappings.")
    allowed = set(instance.__dataclass_fields__)
    unknown = set(values) - allowed
    if unknown:
        raise ConfigurationError(f"Unknown configuration fields: {sorted(unknown)}")
    coerced: dict[str, Any] = {}
    for key, value in values.items():
        current = getattr(instance, key)
        if isinstance(current, AppEnvironment) and not isinstance(
            value, AppEnvironment
        ):
            coerced[key] = _parse_environment(str(value))
        elif isinstance(current, Path) or (
            current is None and key in {"log_file"} and value is not None
        ):
            coerced[key] = Path(value) if value not in (None, "") else None
        else:
            coerced[key] = value
    return replace(instance, **coerced)


def _parse_environment(value: str) -> AppEnvironment:
    normalized = value.strip().lower()
    try:
        return AppEnvironment(normalized)
    except ValueError as exc:
        raise ConfigurationError(
            f"Unsupported environment '{value}'.",
            field="application.environment",
        ) from exc


def _validate_http_url(value: str, *, field: str) -> None:
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ConfigurationError(
            f"Invalid URL for {field}: {value!r}. Expected an http(s) URL.",
            field=field,
        )
