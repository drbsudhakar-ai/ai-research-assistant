"""Experimental Analyze Paper UI.

This package is deliberately not connected to the live navigation route.  It
is retained for review while ``app.ui.pages.analyze`` remains the canonical,
tested Analyze Paper implementation.
"""

from .analyze import render


__all__ = [
    "render",
]
