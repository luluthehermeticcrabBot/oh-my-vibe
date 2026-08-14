## Purpose

Provide an explicit, bounded workflow that can carry a coding task from discovery through implementation, verification, independent review, and evidence-backed completion without changing the default single-agent path.

## ADDED Requirements

### Requirement: User can start an explicit autonomous development run

The system SHALL allow a user or supported client to start an autonomous development run with a goal, repository/workspace, and optional workflow policy. Starting a run MUST return a stable run identifier and an initial lifecycle state.

#### Scenario: Run starts with defaults
- **WHEN** a user starts a run with only a goal in a trusted repository
- **THEN** the system creates a run with bounded default budgets, records the target workspace revision, and reports the run identifier and `planning` state

#### Scenario: Run is not implicit
- **WHEN** a user starts an ordinary coding session without requesting an autonomous run
- **THEN** the system uses the existing single-agent path and does not create an autonomous-run record

### Requirement: Run protects existing workspace changes

The system SHALL capture a `WorkspaceBaseline` containing repository identity, worktree path, HEAD commit, index tree, tracked/untracked/ignored file status, linked-worktree occupancy, and a declared scope before starting a write-capable run. The workspace policy SHALL be one of `reject_dirty`, `isolated_worktree`, or `snapshot`; `reject_dirty` is the default. An active session, live run, or linked worktree using the target path SHALL make it occupied. Snapshots SHALL be immutable, owned by the run, and restorable only by an explicit user command. Run cleanup MUST NOT delete or overwrite baseline or run-created changes without explicit confirmation.

#### Scenario: Dirty primary workspace
- **WHEN** a user starts a write-capable run in a workspace with uncommitted or staged changes and no isolation policy
- **THEN** the run is rejected before child work starts and reports the conflicting workspace state

#### Scenario: Isolated workspace policy
- **WHEN** a user explicitly selects an isolated worktree for a dirty primary workspace
- **THEN** the run records both workspace identities, performs writes only in the isolated worktree, and leaves the primary changes untouched

#### Scenario: Occupied workspace
- **WHEN** the target path is used by an active session, live run, or linked worktree
- **THEN** the run is rejected with `workspace_occupied` unless `isolated_worktree` selects a distinct path, and no files are changed

#### Scenario: Snapshot policy
- **WHEN** the user selects `snapshot` for a dirty but unoccupied workspace
- **THEN** the server creates and records an immutable run-owned snapshot of the baseline, runs only after snapshot success, and reports snapshot creation failure without starting child work

#### Scenario: Cancellation with changes
- **WHEN** a run is cancelled or fails after producing workspace changes
- **THEN** cleanup preserves those changes or requires explicit confirmation before removal, and the final evidence names the retained workspace

#### Scenario: Cleanup disposition
- **WHEN** a run ends with run-created changes
- **THEN** cleanup computes the diff against the immutable baseline, retains or exports the changed workspace by default, and can remove it only after an explicit confirmation naming the workspace and changed paths

#### Scenario: Concurrent disposition
- **WHEN** two disposition requests target the same workspace and expected tuple-set digest
- **THEN** only the first compare-and-set from `pending` with the matching digest can transition to `confirmed`/`applied`; the other receives `disposition_conflict`, and the workspace remains retained

### Requirement: Run progresses through bounded workflow states

The system SHALL expose the states `planning`, `implementing`, `verifying`, `reviewing`, `fixing`, `completed`, `failed`, `cancelled`, and `blocked`. A run MUST move through valid transitions only and MUST record the reason for terminal or blocked states.

#### Scenario: Successful implementation loop
- **WHEN** planning, implementation, verification, and independent review complete without blocking findings
- **THEN** the run transitions to `completed` and publishes an evidence summary

#### Scenario: Review finding enters fix loop
- **WHEN** an independent review reports a valid blocking finding and the review budget remains
- **THEN** the run transitions to `fixing`, records the finding, and schedules verification before another review

#### Scenario: Invalid transition is rejected
- **WHEN** a client requests a transition that is not valid for the current state
- **THEN** the server rejects the request without changing the run state and returns a structured error

### Requirement: Run enforces budgets and cancellation

The system SHALL enforce configured limits for wall-clock duration, total turns, child runs, and review/fix iterations using an atomic ledger with inclusive limits. A user MUST be able to cancel a live run, and cancellation MUST stop or detach child work without silently applying unverified changes. Before terminal finalization, competing causes SHALL be resolved by this fixed priority: explicit user cancellation, deterministic policy denial, budget/deadline exhaustion, stale or scope rejection, child execution failure, then success. Terminal finalization SHALL be a compare-and-set operation over the run revision; after finalization, later causes become evidence only.

#### Scenario: Policy budget exhaustion
- **WHEN** any configured run budget is exhausted
- **THEN** the run becomes `blocked`, records the exhausted budget and stop reason, remains resumable only through an explicit new budget policy, and schedules no further child work

#### Scenario: Internal execution failure
- **WHEN** a child or coordinator encounters an unrecoverable internal execution error unrelated to a configured budget
- **THEN** the run becomes `failed`, records the error classification and stop reason, and schedules no further child work

#### Scenario: Competing terminal causes
- **WHEN** cancellation, budget exhaustion, and child failure are observed before terminal finalization
- **THEN** the coordinator records `cancelled` as the terminal state regardless of arrival order, commits the winning cause once, and records the other causes as secondary evidence

#### Scenario: Terminal finalization race
- **WHEN** two workers attempt to finalize the same run revision
- **THEN** exactly one compare-and-set succeeds; the losing worker cannot change state and records its cause as secondary evidence

#### Scenario: User cancellation
- **WHEN** a user cancels a live run
- **THEN** the run becomes `cancelled`, active children receive cancellation, and the final report distinguishes completed changes from unverified work

### Requirement: Run produces auditable evidence

The system SHALL retain the target revision, state transitions, child-task identifiers, verification commands/results, review findings, fix commits or workspace changes, and final stop reason. The final report MUST distinguish passed, failed, skipped, and unavailable validation.

#### Scenario: Completion report
- **WHEN** a run reaches a terminal state
- **THEN** a client can retrieve a report containing the exact revision, lifecycle history, validation evidence, review result, and remaining concerns

#### Scenario: Validation unavailable
- **WHEN** a required check cannot run because of environment or dependency failure
- **THEN** the report marks that check unavailable and does not claim the run is verified

### Requirement: Run exposes typed lifecycle commands

The server SHALL expose versioned `autonomous-run/start`, `autonomous-run/get`, `autonomous-run/cancel`, `autonomous-run/resume`, and `autonomous-run/evidence` operations. Start requests SHALL contain a goal, workspace, policy, and idempotency key; responses SHALL contain `protocol_version`, `run_id`, state, workspace baseline, and scope. Get/evidence responses SHALL contain the authoritative state, transition sequence, child links, evidence, and stop reason. Invalid transitions, stale run revisions, denied actions, and missing runs SHALL use stable error codes. Resume SHALL require the run ID and an explicit policy for any changed budget or workspace.

#### Scenario: Start and inspect
- **WHEN** a client sends a valid versioned start request
- **THEN** the server returns a stable run ID and `planning` projection, and a subsequent get returns the same protocol version, baseline, scope, and transition sequence

#### Scenario: Idempotent retry
- **WHEN** the same client retries a start request with the same idempotency key
- **THEN** the server returns the original run ID without creating a second run

#### Scenario: Invalid or stale command
- **WHEN** a client sends a cancel/resume command for a missing run, invalid state, or stale run revision
- **THEN** the server returns `run_not_found`, `invalid_transition`, or `stale_run` respectively and does not mutate the run

#### Scenario: Reconnect and resume
- **WHEN** a client reconnects or explicitly resumes a persisted run
- **THEN** the server returns authoritative state and ordered events from the requested watermark, and never requires the client to construct a child runtime

### Requirement: Run events have ordered replay semantics

Every run event SHALL use a versioned envelope containing `protocol_version`, `run_id`, `event_id`, monotonic per-run `sequence`, `timestamp`, `event_type`, `state_revision`, and typed payload. The authoritative run projection, state revision, event record, terminal evidence, and replay watermark SHALL be committed in one durable transaction; sequence allocation occurs inside that transaction and is never reused. A watermark SHALL identify the last contiguous sequence applied by a client. Replay SHALL return events strictly after the requested watermark in sequence order, report a gap when history is unavailable, and require snapshot replacement before further events. A replacement snapshot SHALL include the exact replacement watermark and state revision and SHALL be acknowledged by the client before incremental delivery resumes. Duplicate delivery SHALL be harmless by event ID/sequence, and each mutating RPC SHALL return its authoritative response before its corresponding notification is eligible for delivery. Recovery SHALL either replay the committed event or return a consistent snapshot-plus-watermark; it MUST NOT expose a committed state with an absent event.

#### Scenario: Ordered replay
- **WHEN** a client requests events after watermark sequence 7
- **THEN** the server returns sequence 8 onward in order with no event at or before 7

#### Scenario: Replay gap
- **WHEN** the requested watermark predates retained event history
- **THEN** the server returns a typed `event_gap` response containing the authoritative snapshot and replacement watermark before allowing incremental events

#### Scenario: Duplicate event
- **WHEN** a client receives an event ID or sequence it has already applied
- **THEN** it ignores the duplicate without changing the projection or watermark

#### Scenario: Atomic state and event commit
- **WHEN** a state mutation and event append are committed
- **THEN** both become durable together with one sequence and revision, or neither is visible after recovery

#### Scenario: Snapshot replacement acknowledgment
- **WHEN** a client receives `event_gap`
- **THEN** it replaces its projection with the supplied snapshot, acknowledges the replacement watermark, and receives no incremental event until that acknowledgment

### Requirement: Existing single-agent behavior remains compatible

The system SHALL preserve existing ordinary sessions and task delegation when no autonomous-run command is requested. Existing task arguments, results, child-session links, permission errors, serialized app-server responses, defaults, and depth limits SHALL remain backward compatible.

#### Scenario: Ordinary task delegation
- **WHEN** an existing client invokes the task tool with current arguments and an allowed subagent
- **THEN** it receives the existing result shape and child-session behavior without creating an autonomous-run record

#### Scenario: Existing denial behavior
- **WHEN** an existing client invokes a disallowed agent, exceeds subagent depth, or lacks task context
- **THEN** it receives the existing structured error semantics and no autonomous run is created
