from __future__ import annotations

from vibe import VIBE_ROOT
from vibe.utils.paths import GlobalPath, get_omv_home

OMV_HOME = GlobalPath(get_omv_home)
VIBE_HOME = OMV_HOME
GLOBAL_ENV_FILE = GlobalPath(lambda: OMV_HOME.path / ".env")
SESSION_LOG_DIR = GlobalPath(lambda: VIBE_HOME.path / "logs" / "session")
WORKTREES_DIR = GlobalPath(lambda: VIBE_HOME.path / "worktrees")
TRUSTED_FOLDERS_FILE = GlobalPath(lambda: VIBE_HOME.path / "trusted_folders.toml")
LOG_DIR = GlobalPath(lambda: VIBE_HOME.path / "logs")
LOG_FILE = GlobalPath(lambda: OMV_HOME.path / "logs" / "omv.log")
CACHE_FILE = GlobalPath(lambda: VIBE_HOME.path / "cache.toml")
PROJECTS_FILE = GlobalPath(lambda: VIBE_HOME.path / "projects.toml")
CONNECTOR_BOOTSTRAP_CACHE_FILE = GlobalPath(
    lambda: VIBE_HOME.path / "connector_bootstrap_cache.json"
)
HISTORY_FILE = GlobalPath(lambda: OMV_HOME.path / "omv_history")
PLANS_DIR = GlobalPath(lambda: VIBE_HOME.path / "plans")

DEFAULT_TOOL_DIR = GlobalPath(lambda: VIBE_ROOT / "core" / "tools" / "builtins")
