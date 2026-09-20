"""
AI Research Assistant
General Settings - Sections Package

Contains UI section renderers for General Settings.

Each section is responsible for:
    - Rendering related settings groups
    - Communicating with GeneralSettingsState
    - Keeping UI modular

Version:
    1.0.0
"""

from .appearance_section import AppearanceSection
from .application_section import ApplicationSection
from .storage_section import StorageSection


__all__ = [
    "AppearanceSection",
    "ApplicationSection",
    "StorageSection",
]