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

### Requirement: Run enforces declared change scope

The system SHALL capture a `ScopeManifest` containing normalized POSIX-relative include globs, exclude globs, allowed operations (`create`, `modify`, `delete`, `rename`), symlink policy, generated-file policy, and a canonical baseline identity before write-capable work begins. After UTF-8 decoding and NFC normalization, a valid path is one or more Unicode scalar values excluding NUL, `/`, `\\`, C0 controls, and C1 controls, separated by `/`; empty segments, `.`/`..`, drive prefixes, UNC prefixes, absolute paths, and invalid UTF-8 are rejected. Matching is case-sensitive and non-ASCII scalars are permitted. Glob escaping is unsupported: backslash is always rejected. A valid glob uses the same segment grammar, with `*` matching zero or more non-`/` scalars, `?` matching exactly one non-`/` scalar, and `**` as a complete segment matching zero or more complete segments, including zero segments at a slash boundary; thus `src/**` matches `src` and `src/a.py`, while `src/**/` is invalid. `foo**bar` and malformed patterns are rejected. Paths are slash-normalized, dot-segment-free, and sorted by normalized UTF-8 bytes; excludes take precedence over includes, and a rename is represented as delete-old plus create-new unless rename is explicitly allowed. Symlink entries match the link path and target digest separately; traversal through a symlink is never implicit. The server SHALL derive changed paths from a canonical diff against that baseline, including tracked, staged, untracked, deleted, renamed, symlink, generated, and ignored-file changes according to the manifest policy; child-reported paths are evidence only. A result outside the manifest MUST be rejected deterministically with `scope_violation`, and its workspace MUST be retained for explicit user disposition.

#### Scenario: In-scope changes
- **WHEN** a child changes only paths allowed by the run scope and returns those paths in its result
- **THEN** the reducer can consider the result for application after the revision and policy checks pass

#### Scenario: Same-head out-of-scope change
- **WHEN** a child changes a path outside the declared scope without changing the target revision
- **THEN** the reducer deterministically rejects the result with `scope_violation`, leaves the primary workspace unchanged, and retains the child workspace

#### Scenario: Scope matching
- **WHEN** a changed path matches an include pattern, no exclude pattern, and an allowed operation under the canonical diff rules
- **THEN** the server marks it in scope and permits the reducer to continue revision and policy checks

#### Scenario: Delete, rename, or symlink violation
- **WHEN** a child deletes, renames, creates an untracked file, or changes a symlink contrary to the manifest
- **THEN** the server reports `scope_violation`, does not apply the result to the primary workspace, and retains the child workspace

#### Scenario: Path and glob conformance
- **WHEN** the manifest contains `src/**`, `src/*.py`, `foo**bar`, `foo/**/`, `C:/x`, `//host/share`, an empty segment, or composed/decomposed Unicode paths such as `café.py` and `café.py`
- **THEN** `src/**`, `src/*.py`, `café.py`, and `café.py` are valid and the Unicode forms normalize to one bytewise identity; the other malformed/absolute patterns are rejected before execution

#### Scenario: Glob matching conformance
- **WHEN** the matcher evaluates `src/*`, `src/?`, `src/**`, `src/**/`, and `src\\x` against `src/a`, `src/ab`, `src`, and `src/lib/a.py`
- **THEN** `src/*` matches `src/a` but not `src/lib/a.py`, `src/?` matches neither `src/ab` nor `src/lib/a.py`, `src/**` matches `src` and `src/lib/a.py`, and the trailing-slash and backslash patterns are rejected

#### Scenario: Post-rejection disposition
- **WHEN** a user requests disposition of a retained scope-violating workspace
- **THEN** the server presents the canonical changed-path set and offers only explicit export, retain, or discard operations; disposition cannot approve or implicitly apply the rejected result

### Requirement: Review results are revision-bound

The system SHALL bind every review request and result to an exact source revision and SHALL reject or mark stale any result whose source revision differs from the current target revision.

#### Scenario: Review targets current head
- **WHEN** a reviewer starts against revision A and the target remains at revision A
- **THEN** its findings can be considered for the configured fix/review policy

#### Scenario: Review is stale
- **WHEN** a target changes to revision B before a reviewer result is applied
- **THEN** the system marks the result stale and requires a fresh review or explicit user override

### Requirement: Child permissions cannot weaken parent policy

The system SHALL evaluate each capability in this order: deterministic safety policy, parent run policy, child role declaration, then approval policy. Capability identifiers SHALL be stable. The typed outcome SHALL be exactly one of `allowed`, `role_denied`, `parent_denied`, `deterministically_denied`, or `approval_required`. Only `approval_required` may create an approval request, and only when the parent policy permits the capability. Approval responses SHALL identify the run, child, capability, approver, decision, expiry, and retry boundary.

#### Scenario: Child requests a parent-permitted capability
- **WHEN** a child requests a capability allowed by the parent policy but omitted from its narrower role declaration
- **THEN** the operation may be escalated for explicit approval without expanding the parent policy, and the decision is recorded

#### Scenario: Child requests a parent-denied capability
- **WHEN** a child attempts an operation denied by deterministic safety policy or the parent run policy
- **THEN** the operation fails closed, cannot be granted by child or user approval, and the denial is recorded in child evidence

#### Scenario: Capability decision order
- **WHEN** a child requests a capability
- **THEN** the server evaluates deterministic policy before parent and role policy, returns one typed outcome, and records the policy inputs and outcome

#### Scenario: Approval audit
- **WHEN** a parent-permitted but role-narrowed capability requires approval
- **THEN** the server emits one typed approval request and records the approving authority, decision, expiry, and retry result; an expired approval cannot authorize a later attempt

### Requirement: Child lifecycle is observable and recoverable

The system SHALL publish child-started, child-progress, child-completed, child-failed, child-cancelled, and child-stale events with stable identifiers. A reconnecting client SHALL be able to retrieve the current run projection without constructing child runtimes itself.

#### Scenario: Client reconnects
- **WHEN** a client reconnects during an active run
- **THEN** the server returns the authoritative run state and linked child projections, including children that completed while disconnected
