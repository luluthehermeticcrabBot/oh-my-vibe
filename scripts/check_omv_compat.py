#!/usr/bin/env -S uv run python
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tomllib


class CompatibilityError(Exception):
    pass


def check(root: Path) -> list[str]:
    errors: list[str] = []
    pyproject = tomllib.loads((root / "pyproject.toml").read_text())
    project = pyproject.get("project", {})
    scripts = project.get("scripts", {})
    if project.get("name") != "oh-my-vibe":
        errors.append("project.name must be oh-my-vibe")
    if set(scripts) != {"omv", "omv-acp", "omv-app-server"}:
        errors.append(
            "project.scripts must contain only omv, omv-acp, and omv-app-server"
        )
    if any(name in scripts for name in ("vibe", "vibe-acp", "vibe-app-server")):
        errors.append("vanilla Vibe executable names must not be packaged")

    paths = (root / "vibe/utils/paths.py").read_text()
    if '_DEFAULT_OMV_HOME = Path.home() / ".omv"' not in paths:
        errors.append("default global state directory must be ~/.omv")
    if 'os.getenv("OMV_HOME")' not in paths:
        errors.append("OMV_HOME must be the global state override")
    if 'os.getenv("VIBE_HOME")' in paths:
        errors.append("VIBE_HOME must not be consulted as an end-user override")
    agents = (root / "vibe/core/paths/_agents_home.py").read_text()
    if 'Path.home() / ".agents"' in agents or 'OMV_HOME.path / "agents"' not in agents:
        errors.append("global agents state must be stored under ~/.omv/agents")
    acp_logger = (root / "vibe/acp/acp_logger.py").read_text()
    if 'Path.home() / ".vibe"' in acp_logger:
        errors.append("ACP logs must not use ~/.vibe")

    updater = (root / "vibe/cli/update_notifier/update.py").read_text()
    if "uv tool upgrade oh-my-vibe" not in updater:
        errors.append("runtime update instructions must upgrade oh-my-vibe")
    if "uv tool upgrade mistral-vibe" in updater:
        errors.append("runtime updates must not upgrade mistral-vibe")

    installer = (root / "scripts/install.sh").read_text()
    if (
        "uv tool install mistral-vibe" in installer
        or "uv tool upgrade mistral-vibe" in installer
    ):
        errors.append("installer must not install or upgrade mistral-vibe")

    zed = (root / "distribution/zed/extension.toml").read_text()
    if "mistral-vibe" in zed or "vibe-acp" in zed:
        errors.append("Zed distribution must use Oh My Vibe and omv-acp")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Oh My Vibe upstream compatibility invariants"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("Oh My Vibe compatibility invariants passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
