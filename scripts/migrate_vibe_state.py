from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


def validate(source: Path, destination: Path) -> list[str]:
    errors: list[str] = []
    if not source.is_dir():
        errors.append(f"source is not a directory: {source}")
    if source == destination:
        errors.append("source and destination must differ")
    try:
        destination.relative_to(source)
    except ValueError:
        pass
    else:
        errors.append("destination must not be inside source")
    if destination.exists() and not destination.is_dir():
        errors.append(f"destination is not a directory: {destination}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Explicitly copy upstream Vibe state")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="perform the copy")
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    destination = args.destination.expanduser().resolve()
    errors = validate(source, destination)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    files = [path.relative_to(source) for path in source.rglob("*") if path.is_file()]
    conflicts = [relative for relative in files if (destination / relative).exists()]
    if conflicts:
        print(
            "ERROR: destination already contains files that would be overwritten:\n"
            + "\n".join(f"  - {relative}" for relative in conflicts)
            + "\nChoose an empty destination or remove the conflicting files first.",
            file=sys.stderr,
        )
        return 1
    print(f"Source:      {source}")
    print(f"Destination: {destination}")
    print(f"Files:       {len(files)}")
    if not args.apply:
        print("Dry run only. Re-run with --apply to copy; the source will not be modified.")
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    for relative in files:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, target)
    print("Migration copy completed; source was not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
