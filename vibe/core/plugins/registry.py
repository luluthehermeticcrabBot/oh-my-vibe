"""Plugin discovery and registration with failure isolation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from importlib.metadata import EntryPoint, entry_points
import logging
from typing import Any, Protocol, cast

PLUGIN_API_VERSION = "1"
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PluginManifest:
    name: str
    version: str
    api_version: str
    kind: str
    capabilities: frozenset[str] = frozenset()

    def validate(self) -> None:
        for field_name in ("name", "version", "api_version", "kind"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"plugin manifest field {field_name!r} is required")
        if self.api_version != PLUGIN_API_VERSION:
            raise ValueError(
                f"unsupported plugin API version {self.api_version!r}; "
                f"expected {PLUGIN_API_VERSION!r}"
            )


class PluginRegistrar(Protocol):
    manifest: PluginManifest

    def register(self, registry: PluginRegistry) -> None: ...


@dataclass
class PluginRegistry:
    """Registry of extension callbacks; core safety rules remain outside it."""

    manifests: dict[str, PluginManifest] = field(default_factory=dict)
    analyzers: dict[str, Callable[..., Any]] = field(default_factory=dict)
    sandbox_backends: dict[str, Callable[..., Any]] = field(default_factory=dict)

    def register_plugin(self, plugin: PluginRegistrar) -> None:
        plugin.manifest.validate()
        if plugin.manifest.name in self.manifests:
            raise ValueError(f"duplicate plugin name: {plugin.manifest.name}")
        self.manifests[plugin.manifest.name] = plugin.manifest
        plugin.register(self)

    def register_analyzer(self, name: str, analyzer: Callable[..., Any]) -> None:
        if not name.strip():
            raise ValueError("analyzer name cannot be empty")
        self.analyzers[name] = analyzer

    def register_sandbox_backend(self, name: str, factory: Callable[..., Any]) -> None:
        if not name.strip():
            raise ValueError("sandbox backend name cannot be empty")
        self.sandbox_backends[name] = factory


def _load_entry_point(ep: EntryPoint) -> PluginRegistrar:
    loaded = ep.load()
    plugin = (
        loaded() if callable(loaded) and not hasattr(loaded, "manifest") else loaded
    )
    if not hasattr(plugin, "manifest") or not hasattr(plugin, "register"):
        raise TypeError(f"entry point {ep.name!r} is not an Oh My Vibe plugin")
    return cast(PluginRegistrar, plugin)


def discover_plugins(
    enabled: set[str], *, registry: PluginRegistry | None = None
) -> PluginRegistry:
    """Load only explicitly enabled plugins; isolate each plugin failure."""
    result = registry or PluginRegistry()
    try:
        candidates = entry_points(group="omv.plugins")
    except TypeError:  # pragma: no cover - Python 3.11 compatibility
        candidates = entry_points().select(group="omv.plugins")
    for ep in candidates:
        if ep.name not in enabled:
            continue
        try:
            result.register_plugin(_load_entry_point(ep))
        except Exception:
            logger.exception("Skipping Oh My Vibe plugin %s", ep.name)
    return result
