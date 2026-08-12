## Purpose

Defines the independent product identity and namespace boundaries required for Oh My Vibe to be distributed without presenting upstream Mistral Vibe branding, commands, or state as its own.

## ADDED Requirements

### Requirement: Canonical package and executable identity

The distribution MUST identify itself as `oh-my-vibe` and MUST publish `omv`, `omv-acp`, and `omv-app-server` as its canonical executable names. Release metadata MUST NOT publish the upstream `vibe`, `vibe-acp`, or `vibe-app-server` names as Oh My Vibe entry points.

#### Scenario: Package metadata uses the downstream identity

- **WHEN** a release consumer inspects project metadata
- **THEN** the package name is `oh-my-vibe` and the canonical scripts are exactly the three `omv` variants

#### Scenario: Canonical CLI starts

- **WHEN** a user invokes each canonical executable with `--help`
- **THEN** the executable starts successfully and reports Oh My Vibe usage

### Requirement: Namespaced global state

Oh My Vibe MUST default global state, logs, caches, skills, agents, and related persistent data under `~/.omv` and MUST support `OMV_HOME` as the explicit global-state override. The product MUST NOT consult `VIBE_HOME` as an Oh My Vibe end-user override.

#### Scenario: Default state is isolated

- **WHEN** no downstream state override is set
- **THEN** global Oh My Vibe state resolves below `~/.omv` and does not resolve below `~/.vibe`

#### Scenario: Explicit state override is honored

- **WHEN** `OMV_HOME` points to a user-selected directory
- **THEN** global Oh My Vibe state resolves below that directory

#### Scenario: Upstream override is not silently reused

- **WHEN** only `VIBE_HOME` is set
- **THEN** Oh My Vibe does not treat it as the downstream global-state override

### Requirement: Non-affiliation branding and attribution

User-facing distribution surfaces MUST use Oh My Vibe branding, MUST not use upstream logos as product identity, and MUST include a clear statement that the project is a fork and is not affiliated with, endorsed by, or sponsored by Mistral AI. Factual upstream attribution and links MAY remain where needed for provenance.

#### Scenario: README identifies the fork

- **WHEN** a user reads the README
- **THEN** it identifies Oh My Vibe as a fork, includes the non-affiliation disclaimer, and does not present Mistral Vibe as the current product name

#### Scenario: Distribution metadata uses downstream branding

- **WHEN** a user inspects an installer, editor integration, release artifact, or application label
- **THEN** it uses Oh My Vibe naming and assets and does not imply Mistral AI endorsement

### Requirement: Migration is explicit and non-destructive

The project MUST document migration from upstream Vibe state and commands. Migration tooling MUST validate before writing, require explicit source and destination when copying state, and MUST NOT automatically read, rewrite, move, or delete `~/.vibe` data.

#### Scenario: Migration validation is read-only

- **WHEN** a user runs migration tooling without an explicit write operation
- **THEN** it reports the proposed changes without modifying either source or destination

#### Scenario: Migration writes only with explicit consent

- **WHEN** a user supplies an explicit source, destination, and write confirmation
- **THEN** only the selected data is copied to the selected destination and the source remains intact

#### Scenario: Existing state is not implicitly adopted

- **WHEN** a user installs or starts Oh My Vibe without requesting migration
- **THEN** existing `~/.vibe` state is neither modified nor silently used as Oh My Vibe state

### Requirement: Branding invariants are continuously verified

The repository MUST provide an executable compatibility check covering package metadata, scripts, state paths, installers, updaters, documentation-critical distribution metadata, and editor integrations. CI and release validation MUST run this check and fail when an invariant is violated.

#### Scenario: Real repository passes the invariant check

- **WHEN** CI runs the compatibility check against the repository
- **THEN** the check passes only when all downstream identity and isolation invariants hold

#### Scenario: Deliberate upstream identity regression fails

- **WHEN** a fixture reintroduces an upstream package name, executable, state override, updater command, or distribution identifier
- **THEN** the compatibility check reports the violated invariant and exits unsuccessfully
