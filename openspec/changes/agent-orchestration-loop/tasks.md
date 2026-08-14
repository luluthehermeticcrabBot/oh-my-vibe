## 1. Contracts and coordinator foundation

- [ ] 1.1 Add versioned typed models for autonomous runs, workflow policy/budgets, child requests/results, lifecycle transitions, evidence records, review findings, scope manifests, workspace identities, and terminal reports; require stable IDs and serialized status/error fields.
- [ ] 1.2 Implement transition validation, deterministic `blocked` versus `failed` budget/error mapping, budget accounting, cancellation semantics, and stale-revision checks with focused unit tests for every terminal state.
- [ ] 1.3 Implement the server-owned coordinator over existing child-session and agent-manager ports; keep the current `task` tool path backward compatible and add regression tests proving existing `TaskArgs`/`TaskResult` behavior and subagent depth/allowlist errors remain unchanged.
- [ ] 1.4 Add structured child-result validation and failure classification for malformed, timed-out, cancelled, failed, blocked, and unavailable results.

## 2. Workspace and safety integration

- [ ] 2.1 Integrate run policies with existing permission, sandbox, and approval resolution so child capabilities cannot exceed the parent policy.
- [ ] 2.2 Add read-only explorer/reviewer execution and single-writer implementer execution using explicit workspace identities.
- [ ] 2.3 Add isolated worktree allocation/reuse/cleanup for write-capable parallel children, including dirty/staged-state, occupied-worktree, cancellation-retention, and conflicting-path tests; prohibit destructive cleanup without explicit policy.
- [ ] 2.4 Add exact-head checks and scope-manifest checks before accepting review findings or applying fixer results, including same-head out-of-scope tests.

## 3. Delivery surfaces and persistence

- [ ] 3.1 Add named app-server commands/resources/events for `autonomous-run/start`, `autonomous-run/get`, `autonomous-run/cancel`, `autonomous-run/resume`, and `autonomous-run/evidence`, with typed request/response models, stable run IDs, structured invalid-transition errors, and child lifecycle events.
- [ ] 3.2 Persist run metadata and terminal evidence through the session layer with migration/version tests; document in-flight recovery limits.
- [ ] 3.3 Add CLI commands and TUI lifecycle/progress/evidence projections without embedding coordinator logic in clients.
- [ ] 3.4 Add ACP projections and reconnect tests for active and completed runs, asserting authoritative state replacement and linked child projections without client-created runtimes.

## 4. First autonomous loop

- [ ] 4.1 Implement the opt-in explorer/planner → implementer → verifier → independent reviewer state flow.
- [ ] 4.2 Implement bounded fixer → verifier → reviewer repetition for valid blocking findings only.
- [ ] 4.3 Add explicit stop behavior for clean review, exhausted budgets, unavailable checks, cancellation, stale results, and user denial.
- [ ] 4.4 Add end-to-end public-path tests covering success, review finding/fix, timeout, cancellation, stale head, worktree conflict, and policy denial.

## 5. Evaluation and documentation

- [ ] 5.1 Add a versioned replayable benchmark fixture with representative repository tasks, fixed prompts/policies, seeded inputs, and comparison runs for single-agent, explorer→implementer, and implementer→reviewer configurations.
- [ ] 5.2 Define metric formulas and report success rate, regression rate, review precision/recall, latency, tool calls, token/cost proxy, and human usefulness from a documented rating rubric; report median and tail results.
- [ ] 5.3 Document explicit configuration, safety boundaries, lifecycle states, recovery limitations, and evidence semantics.
- [ ] 5.4 Update README, CHANGELOG, and project orchestration documentation with the first shipped wedge and its non-goals.
- [ ] 5.5 Run strict OpenSpec validation and the focused/canonical test gates before implementation PR review.
