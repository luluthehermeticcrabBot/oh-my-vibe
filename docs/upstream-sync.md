# Safe upstream synchronization

Oh My Vibe tracks Mistral Vibe through the `upstream` Git remote, but upstream changes are never installed directly for Oh My Vibe users.

## Branch model

`main` is the Oh My Vibe default and release branch. It is not a vanilla upstream mirror. Do not merge `upstream/main` directly into `main` without review.

Upstream synchronization is prepared from downstream `main` on a temporary `upstream-sync/YYYYMMDD-HHMMSS` branch. That branch contains the upstream merge plus the existing Oh My Vibe commits, so conflicts are resolved against the downstream invariants rather than by overwriting them. The reviewed sync branch is merged back into Oh My Vibe `main` only after all gates pass.

An optional local `upstream-main` tracking branch may be useful for inspection, but it is not authoritative and should not be used as the release base. The `upstream` remote-tracking ref is sufficient for normal operation.

## Local review

From a clean checkout:

```bash
git fetch upstream main
uv run python scripts/sync_upstream.py
```

The script creates a dated `upstream-sync/...` branch, merges `upstream/main` without committing, and runs the focused-test gates. A conflict or failed gate aborts the merge and returns to the original branch.

After reviewing the merge and running the full suite, commit and push the branch manually. Do not merge it until CI passes and the changes have been checked for conflicts with Oh My Vibe memory, skills, configuration, commands, and state paths. Intentional Oh My Vibe edits are protected by review and compatibility gates, not by blindly preferring either side of a merge.

For automation, the scheduled `.github/workflows/upstream-sync.yml` workflow uses `--commit` and opens a pull request. It does not publish a package or update the default branch.

## Required gates

```bash
uv lock --check
uv run pytest
```

Branding and upstream-compatibility invariants are validated in the separate branding/upstream synchronization change, not in this safety/plugin change.

## Configuration migration

Migration is explicit and non-destructive. It validates a TOML file first and only copies it when `--write` is supplied:

```bash
uv run python scripts/migrate_omv_config.py ./config.toml \
  --destination "$HOME/.omv/config.toml" --write
```

The tool never discovers, rewrites, or deletes `~/.vibe` automatically. Keep vanilla Vibe state separate unless a user explicitly chooses a migration source and destination.

## Release policy

Only publish from the reviewed Oh My Vibe default branch. Upstream synchronization is source integration, not a release. A failed compatibility gate, failed test, unresolved merge conflict, or unreviewed generated artifact blocks release.
