## Purpose

Define safe, typed coordination between an implementer, read-only explorers, independent reviewers, and fix workers while preserving workspace isolation, exact-revision identity, and explicit permission boundaries.

## ADDED Requirements

### Requirement: Child work uses structured contracts

The system SHALL represent delegated work with a typed request containing a goal, role, scope, write permission, workspace identity, budget, timeout, and expected result shape. Child completion SHALL include status, summary, changed paths, validation evidence, and unresolved concerns.

#### Scenario: Read-only exploration
- **WHEN** an explorer is delegated with no-write permission
- **THEN** the child cannot mutate the implementation workspace and returns structured discovery evidence

#### Scenario: Missing required result fields
- **WHEN** a child returns malformed or incomplete structured output
- **THEN** the parent marks the child result invalid and does not treat it as successful evidence

### Requirement: Parallel writers are isolated

The system SHALL require separate isolated workspaces for concurrent children that can write. The parent SHALL use an explicit reducer or selection step before applying one child result to the primary workspace.

#### Scenario: Concurrent implementations
- **WHEN** two write-capable children are launched in parallel
- **THEN** each receives a distinct workspace identity and neither can silently overwrite the other child’s files

#### Scenario: Reducer rejects conflicting changes
- **WHEN** parallel child outputs modify overlapping paths incompatibly
- **THEN** the reducer reports a conflict and leaves the primary workspace unchanged

### Requirement: Review results are revision-bound

The system SHALL bind every review request and result to an exact source revision and SHALL reject or mark stale any result whose source revision differs from the current target revision.

#### Scenario: Review targets current head
- **WHEN** a reviewer starts against revision A and the target remains at revision A
- **THEN** its findings can be considered for the configured fix/review policy

#### Scenario: Review is stale
- **WHEN** a target changes to revision B before a reviewer result is applied
- **THEN** the system marks the result stale and requires a fresh review or explicit user override

### Requirement: Child permissions cannot weaken parent policy

The system SHALL enforce parent-approved capabilities, deterministic safety policy, and explicit human denial before child tool execution. A child MUST NOT grant itself broader write, shell, network, credential, or delegation access than the parent run permits.

#### Scenario: Child requests disallowed capability
- **WHEN** a child attempts an operation outside its declared or parent-approved capabilities
- **THEN** the operation is denied or escalated for approval and the denial is recorded in the child evidence

### Requirement: Child lifecycle is observable and recoverable

The system SHALL publish child-started, child-progress, child-completed, child-failed, child-cancelled, and child-stale events with stable identifiers. A reconnecting client SHALL be able to retrieve the current run projection without constructing child runtimes itself.

#### Scenario: Client reconnects
- **WHEN** a client reconnects during an active run
- **THEN** the server returns the authoritative run state and linked child projections, including children that completed while disconnected
