"""Application configuration package.

Canonical runtime configuration is loaded from ``app.config.loader``.
Product identity remains ``app.config.branding.BrandConfig``.
"""

from __future__ import annotations

from typing import Any

from app.config.branding import BrandConfig, get_brand_config

__all__ = [
    "ApplicationConfig",
    "BrandConfig",
    "ConfigurationError",
    "get_application_config",
    "get_brand_config",
    "load_application_config",
    "reset_application_config",
]


def __getattr__(name: str) -> Any:
    if name == "ApplicationConfig":
        from app.config.application_config import ApplicationConfig

        return ApplicationConfig
    if name == "ConfigurationError":
        from app.config.exceptions import ConfigurationError

        return ConfigurationError
    if name in {
        "get_application_config",
        "load_application_config",
        "reset_application_config",
    }:
        from app.config import loader

        return getattr(loader, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
