## Why

Oh My Vibe is currently distributed with upstream Mistral Vibe package names, executable names, state paths, updater commands, and visual identity. This creates namespace collisions, confuses users about project ownership, and prevents the fork from presenting a clear independent product identity. The merged safety work intentionally deferred this migration; it is now the highest-priority follow-up.

## What Changes

- **BREAKING** Make `oh-my-vibe` the package identity and `omv`, `omv-acp`, and `omv-app-server` the canonical console scripts.
- **BREAKING** Move default global Oh My Vibe state to `~/.omv` and use `OMV_HOME` as its explicit override.
- Add explicit, non-destructive migration guidance from existing `~/.vibe` state; never silently move, delete, or reinterpret user state.
- Replace Mistral-owned logos and product presentation with Oh My Vibe branding.
- Update README, documentation, onboarding, updater, installer, release tooling, Nix, Zed integration, package metadata, and user-facing strings.
- Preserve factual upstream attribution and add a clear non-affiliation disclaimer.
- Add compatibility invariants, fixture tests, package metadata checks, CLI smoke tests, and CI/release gates for the migration.
- Document deprecated command/path behavior and the supported migration window.

## Capabilities

### New Capabilities

- `oh-my-vibe-identity`: Defines the canonical package, executable, state, branding, attribution, and distribution identity.
- `explicit-state-migration`: Provides safe, user-controlled migration guidance and tooling from upstream Vibe state to Oh My Vibe state.

### Modified Capabilities

- None. Existing repository behavior is being re-identified and extended through new downstream contracts rather than modifying an existing OpenSpec capability.

## Impact

Affected areas include `pyproject.toml`, CLI entry points, path/config resolution, installers and updaters, onboarding and UI text, README and documentation, release scripts, Nix, Zed distribution metadata, tests, snapshots, and CI. Existing users may need to update commands and explicitly migrate state; no automatic data movement is permitted.