## Purpose

Defines the stable, harness-neutral prerequisites for plugins that analyze commands, provide sandbox capabilities, or expose future agent extensions without granting plugins authority to bypass host safety policy.

## ADDED Requirements

### Requirement: Plugin manifests are versioned and capability-scoped

A plugin manifest MUST identify a stable name, semantic version, plugin API version, kind, capabilities, and callable entry point. Hosts MUST reject unsupported API versions, duplicate names, missing required fields, and capabilities outside the declared kind.

#### Scenario: Valid manifest is accepted

- **WHEN** a host loads a manifest with supported fields and API version
- **THEN** the plugin is available under its declared capabilities

#### Scenario: Unsupported manifest is rejected

- **WHEN** a manifest has an unsupported API version or undeclared capability
- **THEN** the host rejects it without registering executable behavior

### Requirement: Plugin authority is advisory by default

A plugin MUST NOT be able to approve a command, remove a required permission, disable a sandbox, or override explicit human denial. Host deterministic policy MUST remain authoritative.

#### Scenario: Advisory allow meets a core restriction

- **WHEN** an analyzer returns ALLOW for a command requiring outside-directory, sensitive-command, denylist, or sandbox controls
- **THEN** the host preserves the core restriction and does not auto-approve the command

#### Scenario: Plugin attempts to select execution authority

- **WHEN** plugin output requests unsandboxed execution or an authority level not in its contract
- **THEN** the host rejects the authority request and fails safely to human approval or denial

### Requirement: Plugin failure is fail-safe and observable

Exceptions, malformed results, unsupported asynchronous behavior, and timeouts MUST not crash the host or produce automatic approval. The host MUST expose evaluator and failure metadata sufficient for diagnostics.

#### Scenario: Analyzer times out

- **WHEN** an analyzer exceeds its configured timeout
- **THEN** the host returns an approval-needed result and records the timeout

#### Scenario: Analyzer raises an exception

- **WHEN** an analyzer raises while evaluating a command
- **THEN** the host continues with deterministic policy and records the failure

### Requirement: Isolation claims are explicit

A plugin standard MUST distinguish trusted in-process plugins from process-isolated plugins. It MUST NOT claim that thread timeouts or metadata alone provide process isolation.

#### Scenario: Trusted in-process plugin is configured

- **WHEN** a host enables a trusted in-process plugin
- **THEN** the host records that trust boundary and applies bounded execution semantics

#### Scenario: Untrusted plugin lacks isolation

- **WHEN** an untrusted plugin is requested but no isolating process runtime is available
- **THEN** the host refuses to execute it as untrusted code
