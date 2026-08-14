## 1. Contracts and coordinator foundation

- [ ] 1.1 Add versioned typed models for autonomous runs, workflow policy/budgets, child requests/results, lifecycle transitions, evidence records, review findings, scope manifests, workspace identities, and terminal reports; require stable IDs and serialized status/error fields.
- [ ] 1.2 Implement the atomic budget ledger with inclusive limits and the documented terminal-cause precedence; test reservation/commit races, deadline, cancellation, policy denial, stale/scope rejection, child failure, and success outcomes.
- [ ] 1.3 Implement the server-owned coordinator over existing child-session and agent-manager ports; keep the current `task` tool path backward compatible and add regression tests proving existing `TaskArgs`/`TaskResult` behavior and subagent depth/allowlist errors remain unchanged.
- [ ] 1.4 Add structured child-result validation and failure classification for malformed, timed-out, cancelled, failed, blocked, and unavailable results.

## 2. Workspace and safety integration

- [ ] 2.1 Integrate run policies with existing permission, sandbox, and approval resolution so child capabilities cannot exceed the parent policy.
- [ ] 2.2 Add read-only explorer/reviewer execution and single-writer implementer execution using explicit workspace identities.
- [ ] 2.3 Add typed workspace-state detection for dirty/staged/untracked/ignored files, active sessions, live runs, and linked worktrees; implement `reject_dirty`, `isolated_worktree`, and `snapshot` policies, immutable baseline hashes, allocation/restore failure blocking, cancellation retention, and explicit cleanup confirmation tests.
- [ ] 2.4 Add a canonical server-derived diff and `ScopeManifest` matcher covering includes/excludes, create/modify/delete/rename, symlinks, generated files, untracked files, and deterministic `scope_violation` retention behavior.

## 3. Delivery surfaces and persistence

- [ ] 3.1 Add versioned typed app-server contracts for `autonomous-run/start`, `autonomous-run/get`, `autonomous-run/cancel`, `autonomous-run/resume`, and `autonomous-run/evidence`, including required fields, stable error codes, idempotency, authorization, revision checks, ordered event payloads, watermarks, and registration in the method catalogue.
- [ ] 3.2 Persist run metadata and terminal evidence through the session layer with migration/version tests; document in-flight recovery limits.
- [ ] 3.3 Add CLI commands and TUI lifecycle/progress/evidence projections without embedding coordinator logic in clients.
- [ ] 3.4 Add ACP projections and reconnect tests for active and completed runs, asserting authoritative state replacement and linked child projections without client-created runtimes.

## 4. First autonomous loop

- [ ] 4.1 Implement the opt-in explorer/planner → implementer → verifier → independent reviewer state flow.
- [ ] 4.2 Implement bounded fixer → verifier → reviewer repetition for valid blocking findings only.
- [ ] 4.3 Add explicit stop behavior for clean review, exhausted budgets, unavailable checks, cancellation, stale results, and user denial.
- [ ] 4.4 Add end-to-end public-path tests covering success, review finding/fix, timeout, cancellation, stale head, scope violation, dirty/occupied/snapshot workspace policy, cleanup retention, worktree conflict, typed permission outcomes, RPC errors, reconnect/resume, and parent-policy denial.

## 5. Evaluation and documentation

- [ ] 5.1 Add a committed versioned fixture manifest with at least 12 representative tasks (four bug fixes, four features, four refactors), fixed prompts/policies, seeded inputs, pinned environment, and three repetitions for each comparison configuration.
- [ ] 5.2 Define metric formulas, reviewer/human rating rubric, median/p90 reporting, and readiness gates: no worse functional success or regression rate than single-agent, improvement in review precision or usefulness, and no more than 2x median latency or cost proxy; keep the feature opt-in when the gate fails.
- [ ] 5.3 Document explicit configuration, safety boundaries, lifecycle states, recovery limitations, and evidence semantics.
- [ ] 5.4 Update README, CHANGELOG, and project orchestration documentation with the first shipped wedge and its non-goals.
- [ ] 5.5 Run strict OpenSpec validation and the focused/canonical test gates before implementation PR review.
