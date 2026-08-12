## Context

The repository is a downstream fork whose current package metadata, scripts, state paths, installers, updater text, editor integration, and UI still identify the upstream product. The merged safety change intentionally excluded this migration, so the implementation must start from `origin/main` and preserve existing upstream behavior where it is not part of the downstream boundary.

## Goals / Non-Goals

**Goals:**

- Establish `oh-my-vibe`, `omv`, `omv-acp`, and `omv-app-server` as the canonical distribution identity.
- Isolate downstream global state under `~/.omv` with `OMV_HOME` override semantics.
- Replace product-facing upstream branding and artwork while retaining factual provenance.
- Provide explicit, non-destructive migration guidance and tooling.
- Make identity and namespace invariants executable in tests, CI, and release validation.

**Non-Goals:**

- Building a desktop application.
- Defining the cross-harness plugin standard or extracting an SDK.
- Automatically migrating or deleting existing user state.
- Removing every factual mention of Mistral from historical changelog or attribution material.
- Changing provider functionality or upstream API semantics.

## Decisions

### Canonical names are downstream-only

The package and canonical scripts use the Oh My Vibe namespace. Alternatives considered were retaining upstream scripts indefinitely or shipping aliases in the same package. Retaining upstream entry points would preserve namespace collision and branding ambiguity; if compatibility aliases are needed, they must be separately designed and clearly deprecated rather than silently treated as canonical.

### State isolation is explicit and non-destructive

`~/.omv` and `OMV_HOME` become the downstream state contract. Alternatives considered were reusing `~/.vibe` or automatically copying it. Reuse would couple independent products; automatic copying risks data loss and surprising behavior. Migration therefore requires explicit source, destination, validation, and write consent.

### Provenance is retained but product branding is replaced

The README and selected documentation will identify the project as a fork and preserve an upstream link, while logos, package presentation, install commands, and user-facing product labels use Oh My Vibe. The alternative of deleting all upstream references would harm attribution and troubleshooting clarity.

### Compatibility checking is source-level plus artifact-level

A repository checker catches source and configuration regressions; wheel metadata, executable smoke tests, installer checks, and Zed metadata checks catch distribution regressions. Relying only on grep or only on source checks would miss generated/package surfaces.

### Desktop and plugin standard remain separate changes

Desktop work is deferred to a future project. Plugin work begins with a separate foundation specification and does not promise SDK interoperability until trust, isolation, and adapter semantics are proven.

## Risks / Trade-offs

- [Breaking command rename] → Publish migration instructions and make canonical names explicit before release.
- [Existing users rely on `~/.vibe`] → Preserve source state, document explicit migration, and test no-implicit-adoption behavior.
- [Incomplete branding inventory] → Use repository scans, artifact inspection, fixture checks, and review of generated assets.
- [Historical documentation contains upstream names] → Distinguish factual attribution/history from current product identity; do not rewrite history unnecessarily.
- [Release artifacts diverge from source metadata] → Validate wheels, installers, Zed manifests, and smoke executables in CI.

## Migration Plan

1. Add the invariant checker, fixtures, and target identity tests before changing all surfaces.
2. Change package metadata, entry points, state resolution, installers, updater, onboarding, distribution files, and documentation in grouped commits.
3. Add explicit migration utility/documentation and verify source preservation.
4. Run focused tests, artifact checks, full CI, and release dry runs.
5. Release only after the compatibility gates pass.
6. Roll back by reverting the release if necessary; never roll back by deleting or rewriting user state.
