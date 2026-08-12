from __future__ import annotations

from pathlib import Path

from scripts.check_omv_compat import check

ROOT = Path(__file__).parents[2]


def test_repository_passes_omv_compatibility_invariants() -> None:
    assert check(ROOT) == []


def test_checker_rejects_vanilla_entrypoint(tmp_path: Path) -> None:
    (tmp_path / "vibe/utils").mkdir(parents=True)
    (tmp_path / "vibe/cli/update_notifier").mkdir(parents=True)
    (tmp_path / "vibe/core/paths").mkdir(parents=True)
    (tmp_path / "vibe/acp").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "distribution/zed").mkdir(parents=True)
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "oh-my-vibe"\n[project.scripts]\nvibe = "vibe.cli.entrypoint:main"\n'
    )
    (tmp_path / "vibe/utils/paths.py").write_text(
        '_DEFAULT_OMV_HOME = Path.home() / ".omv"\nos.getenv("OMV_HOME")\n'
    )
    (tmp_path / "vibe/cli/update_notifier/update.py").write_text(
        '"uv tool upgrade oh-my-vibe"\n'
    )
    (tmp_path / "vibe/core/paths/_agents_home.py").write_text(
        'OMV_HOME.path / "agents"\n'
    )
    (tmp_path / "vibe/acp/acp_logger.py").write_text("")
    (tmp_path / "distribution/zed/extension.toml").write_text("omv-acp\n")
    (tmp_path / "scripts/install.sh").write_text("uv tool install -e .\n")
    assert "project.scripts" in " ".join(check(tmp_path))
