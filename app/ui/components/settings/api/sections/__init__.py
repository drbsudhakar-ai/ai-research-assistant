"""
app/ui/components/settings/api/sections/__init__.py

API Settings UI section exports.

Contains modular Streamlit UI sections for:
- Provider selection
- Connection settings
- Model settings
- Generation controls
- Advanced options
- Connection testing

Author : AI Research Assistant
Version: 1.0.0
"""

from __future__ import annotations


from .provider_section import (
    render_provider_section,
)

from .connection_section import (
    render_connection_section,
)

from .model_section import (
    render_model_section,
)

from .generation_section import (
    render_generation_section,
)

from .advanced_section import (
    render_advanced_section,
)

from .test_connection import (
    render_connection_test,
)


__version__ = "1.0.0"


__all__ = [

    "render_provider_section",

    "render_connection_section",

    "render_model_section",

    "render_generation_section",

    "render_advanced_section",

    "render_connection_test",

    "__version__",
]