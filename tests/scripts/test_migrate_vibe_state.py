from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parents[2]
SCRIPT = ROOT / "scripts" / "migrate_vibe_state.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_dry_run_does_not_write(tmp_path: Path) -> None:
    source = tmp_path / ".vibe"
    destination = tmp_path / ".omv"
    source.mkdir()
    (source / "config.toml").write_text("active_model = 'test'\n", encoding="utf-8")
    result = run("--source", str(source), "--destination", str(destination))
    assert result.returncode == 0
    assert not destination.exists()
    assert (source / "config.toml").exists()


def test_apply_copies_without_modifying_source(tmp_path: Path) -> None:
    source = tmp_path / ".vibe"
    destination = tmp_path / ".omv"
    source.mkdir()
    original = "active_model = 'test'\n"
    (source / "config.toml").write_text(original, encoding="utf-8")
    result = run("--source", str(source), "--destination", str(destination), "--apply")
    assert result.returncode == 0
    assert (destination / "config.toml").read_text(encoding="utf-8") == original
    assert (source / "config.toml").read_text(encoding="utf-8") == original


def test_rejects_destination_inside_source(tmp_path: Path) -> None:
    source = tmp_path / ".vibe"
    source.mkdir()
    result = run("--source", str(source), "--destination", str(source / "copy"))
    assert result.returncode == 1
    assert "inside source" in result.stderr


def test_rejects_existing_destination_conflicts(tmp_path: Path) -> None:
    source = tmp_path / ".vibe"
    destination = tmp_path / ".omv"
    source.mkdir()
    destination.mkdir()
    (source / "config.toml").write_text("new\n", encoding="utf-8")
    (destination / "config.toml").write_text("existing\n", encoding="utf-8")
    result = run("--source", str(source), "--destination", str(destination), "--apply")
    assert result.returncode == 1
    assert "would be overwritten" in result.stderr
    assert (destination / "config.toml").read_text(encoding="utf-8") == "existing\n"
