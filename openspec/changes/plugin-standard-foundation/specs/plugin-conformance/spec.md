## Purpose

Defines conformance evidence that an implementation must provide before Oh My Vibe can claim compatibility with a shared plugin standard or publish a standalone plugin SDK.

## ADDED Requirements

### Requirement: Conformance tests cover every declared capability

A plugin implementation MUST have contract tests for manifest parsing, discovery, capability registration, invalid output, failure, timeout, authority boundaries, and lifecycle behavior for each capability it exposes.

#### Scenario: Existing analyzer registry is evaluated

- **WHEN** the conformance suite runs against the current analyzer registry
- **THEN** it verifies registration and all fail-safe safety cases without requiring network credentials

#### Scenario: Missing conformance evidence blocks compatibility claims

- **WHEN** a plugin or adapter lacks required contract coverage
- **THEN** the project does not label it standard-compatible or SDK-ready

### Requirement: Adapter semantics are documented before implementation

A harness adapter MUST document mapping for manifests, decisions, permissions, sandbox state, errors, timeouts, and lifecycle before claiming interoperability.

#### Scenario: Adapter design is reviewed

- **WHEN** an adapter proposal maps all required contract concepts
- **THEN** it can proceed to an implementation-specific design review

#### Scenario: Adapter omits a safety concept

- **WHEN** an adapter has no defined mapping for host permission or sandbox authority
- **THEN** it is rejected as incomplete and cannot be released as compatible

### Requirement: SDK extraction has explicit exit criteria

The project MUST NOT extract or publish a standalone SDK until the manifest, compatibility/versioning, trust/isolation, conformance, and at least one adapter mapping are stable and reviewed.

#### Scenario: Prerequisites are incomplete

- **WHEN** process isolation or version-negotiation behavior remains undefined
- **THEN** SDK extraction remains deferred

#### Scenario: Prerequisites are complete

- **WHEN** all documented exit criteria and conformance evidence are satisfied
- **THEN** a separate SDK implementation change may be proposed
