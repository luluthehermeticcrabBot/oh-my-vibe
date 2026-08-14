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

The system SHALL capture the starting commit, index state, worktree identity, and declared scope before starting a write-capable run. A dirty or occupied workspace MUST be rejected by default unless the user explicitly selects a non-destructive policy such as an isolated worktree or an approved snapshot. Run cleanup MUST NOT delete or overwrite user changes without explicit confirmation.

#### Scenario: Dirty primary workspace
- **WHEN** a user starts a write-capable run in a workspace with uncommitted or staged changes and no isolation policy
- **THEN** the run is rejected before child work starts and reports the conflicting workspace state

#### Scenario: Isolated workspace policy
- **WHEN** a user explicitly selects an isolated worktree for a dirty primary workspace
- **THEN** the run records both workspace identities, performs writes only in the isolated worktree, and leaves the primary changes untouched

#### Scenario: Cancellation with changes
- **WHEN** a run is cancelled or fails after producing workspace changes
- **THEN** cleanup preserves those changes or requires explicit confirmation before removal, and the final evidence names the retained workspace

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

The system SHALL enforce configured limits for wall-clock duration, total turns, child runs, and review/fix iterations. A user MUST be able to cancel a live run, and cancellation MUST stop or detach child work without silently applying unverified changes.

#### Scenario: Policy budget exhaustion
- **WHEN** any configured run budget is exhausted
- **THEN** the run becomes `blocked`, records the exhausted budget and stop reason, remains resumable only through an explicit new budget policy, and schedules no further child work

#### Scenario: Internal execution failure
- **WHEN** a child or coordinator encounters an unrecoverable internal execution error unrelated to a configured budget
- **THEN** the run becomes `failed`, records the error classification and stop reason, and schedules no further child work

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
