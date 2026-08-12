"""Stable extension contracts for Oh My Vibe plugins."""

from __future__ import annotations

from vibe.core.plugins.registry import (
    PLUGIN_API_VERSION,
    PluginManifest,
    PluginRegistry,
    discover_plugins,
)

__all__ = ["PLUGIN_API_VERSION", "PluginManifest", "PluginRegistry", "discover_plugins"]
