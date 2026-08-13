from __future__ import annotations

from collections.abc import Callable
import os
from pathlib import Path


class GlobalPath:
    def __init__(self, resolver: Callable[[], Path]) -> None:
        self._resolver = resolver

    @property
    def path(self) -> Path:
        return self._resolver()


_DEFAULT_OMV_HOME = Path.home() / ".omv"


def get_omv_home() -> Path:
    if omv_home := os.getenv("OMV_HOME"):
        return Path(omv_home).expanduser().resolve()
    return _DEFAULT_OMV_HOME


get_vibe_home = get_omv_home


def is_dangerous_directory(path: Path | str = ".") -> tuple[bool, str]:
    """Check if the current directory is a dangerous folder that would cause
    issues if we were to run the tool there.

    Args:
        path: Path to check (defaults to current directory)

    Returns:
        tuple[bool, str]: (is_dangerous, reason) where reason explains why it's dangerous
    """
    path = Path(path).resolve()

    home_dir = Path.home()

    dangerous_paths = {
        home_dir: "home directory",
        home_dir / "Documents": "Documents folder",
        home_dir / "Desktop": "Desktop folder",
        home_dir / "Downloads": "Downloads folder",
        home_dir / "Pictures": "Pictures folder",
        home_dir / "Movies": "Movies folder",
        home_dir / "Music": "Music folder",
        home_dir / "Library": "Library folder",
        Path("/Applications"): "Applications folder",
        Path("/System"): "System folder",
        Path("/Library"): "System Library folder",
        Path("/usr"): "System usr folder",
        Path("/private"): "System private folder",
    }

    for dangerous_path, description in dangerous_paths.items():
        try:
            if path == dangerous_path:
                return True, f"You are in the {description}"
        except (OSError, ValueError):
            continue
    return False, ""
