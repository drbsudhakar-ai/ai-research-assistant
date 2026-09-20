"""
AI Research Assistant
General Settings - State Management

Maintains runtime state for General Settings.

Responsibilities:
    - Store current settings values
    - Load default values
    - Track modifications
    - Reset settings
    - Validate configuration
    - Export configuration dictionary

No Streamlit dependency.

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from ..defaults import (
    DEFAULT_APP_NAME,
    DEFAULT_THEME_MODE,
    DEFAULT_UI_DENSITY,
    DEFAULT_LANGUAGE,
    DEFAULT_STARTUP_PAGE,
    DEFAULT_WORKSPACE_PATH,
    DEFAULT_HISTORY_STORAGE_MODE,
    DEFAULT_HISTORY_PATH,
    DEFAULT_AUTO_SAVE_MODE,
    DEFAULT_CONFIRMATION_MODE,
    DEFAULT_DATE_FORMAT,
    DEFAULT_LOGGING_LEVEL,
    DEFAULT_SHOW_TOOLTIPS,
    DEFAULT_SHOW_ADVANCED_OPTIONS,
    DEFAULT_ENABLE_ANIMATIONS,
    DEFAULT_REMEMBER_LAST_PAGE,
    DEFAULT_CLEAR_TEMP_FILES_ON_EXIT,
    DEFAULT_CACHE_ENABLED,
)

from ..enums import (
    ThemeMode,
    UIDensity,
    ApplicationLanguage,
    StartupPage,
    HistoryStorageMode,
    AutoSaveMode,
    ConfirmationMode,
    DateFormat,
    LoggingLevel,
)

from ..validators import validate_general_settings


# ============================================================
# State Model
# ============================================================


@dataclass
class GeneralSettingsState:
    """
    Runtime state container for General Settings.
    """

    # Application
    app_name: str = DEFAULT_APP_NAME

    # UI
    theme_mode: ThemeMode = DEFAULT_THEME_MODE
    ui_density: UIDensity = DEFAULT_UI_DENSITY
    language: ApplicationLanguage = DEFAULT_LANGUAGE

    # Startup
    startup_page: StartupPage = DEFAULT_STARTUP_PAGE

    # Storage
    workspace_path: Path = DEFAULT_WORKSPACE_PATH
    history_storage_mode: HistoryStorageMode = (
        DEFAULT_HISTORY_STORAGE_MODE
    )
    history_path: Path = DEFAULT_HISTORY_PATH

    # Behaviour
    auto_save_mode: AutoSaveMode = (
        DEFAULT_AUTO_SAVE_MODE
    )

    confirmation_mode: ConfirmationMode = (
        DEFAULT_CONFIRMATION_MODE
    )

    date_format: DateFormat = DEFAULT_DATE_FORMAT

    logging_level: LoggingLevel = (
        DEFAULT_LOGGING_LEVEL
    )

    # UI Flags
    show_tooltips: bool = DEFAULT_SHOW_TOOLTIPS

    show_advanced_options: bool = (
        DEFAULT_SHOW_ADVANCED_OPTIONS
    )

    enable_animations: bool = (
        DEFAULT_ENABLE_ANIMATIONS
    )

    # Privacy
    remember_last_page: bool = (
        DEFAULT_REMEMBER_LAST_PAGE
    )

    clear_temp_files_on_exit: bool = (
        DEFAULT_CLEAR_TEMP_FILES_ON_EXIT
    )

    # Performance
    cache_enabled: bool = (
        DEFAULT_CACHE_ENABLED
    )

    # Internal state
    _original_state: dict[str, Any] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )


    # ========================================================
    # Initialization
    # ========================================================

    def __post_init__(self) -> None:
        """
        Store initial state snapshot.
        """

        self._original_state = (
            self.to_dict()
        )


    # ========================================================
    # Factory
    # ========================================================

    @classmethod
    def load_defaults(
        cls,
    ) -> "GeneralSettingsState":
        """
        Create state using default configuration.
        """

        return cls()


    # ========================================================
    # Update Operations
    # ========================================================

    def update(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Update a single setting value.
        """

        if not hasattr(self, key):
            raise AttributeError(
                f"Unknown setting: {key}"
            )

        setattr(
            self,
            key,
            value,
        )


    def update_many(
        self,
        values: dict[str, Any],
    ) -> None:
        """
        Update multiple settings.
        """

        for key, value in values.items():
            self.update(
                key,
                value,
            )


    # ========================================================
    # Change Tracking
    # ========================================================

    def is_dirty(
        self,
    ) -> bool:
        """
        Check whether settings changed.
        """

        return (
            self.to_dict()
            != self._original_state
        )


    def mark_saved(
        self,
    ) -> None:
        """
        Save current state as baseline.
        """

        self._original_state = (
            self.to_dict()
        )


    # ========================================================
    # Reset Operations
    # ========================================================

    def reset(
        self,
    ) -> None:
        """
        Reset current values to defaults.
        """

        default_state = (
            GeneralSettingsState()
        )

        self.update_many(
            default_state.to_dict()
        )


    # ========================================================
    # Validation
    # ========================================================

    def validate(
        self,
    ) -> tuple[bool, list[str]]:
        """
        Validate current configuration.
        """

        return validate_general_settings(
            self.to_dict()
        )


    # ========================================================
    # Serialization
    # ========================================================

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Convert state into dictionary.
        """

        data = asdict(self)

        data.pop(
            "_original_state",
            None,
        )

        return data


    def export_json_ready(
        self,
    ) -> dict[str, Any]:
        """
        Convert state into JSON serializable format.
        """

        result: dict[str, Any] = {}

        for key, value in self.to_dict().items():

            if isinstance(
                value,
                Path,
            ):
                result[key] = str(value)

            elif hasattr(
                value,
                "value",
            ):
                result[key] = value.value

            else:
                result[key] = value

        return result


    # ========================================================
    # Convenience
    # ========================================================

    def get(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve setting value.
        """

        if not hasattr(self, key):
            raise AttributeError(
                f"Unknown setting: {key}"
            )

        return getattr(
            self,
            key,
        )


__all__ = [
    "GeneralSettingsState",
]