## Context

The repository already has server-owned child sessions, a typed `task` tool, an agent manager, worktree preparation/cleanup, durable session metadata, and an event-driven app-server boundary. The current task path is one-shot delegation: it can run a subagent and return prose, but it does not own a multi-stage development lifecycle, revision identity, budget ledger, or review/fix reducer. See `docs/ORCHESTRATION.md` and ADRs 0003, 0006, 0007, and 0009.

## Goals / Non-Goals

**Goals:**

- Add a delivery-neutral autonomous-run state machine over existing child-session primitives.
- Make delegation typed, budgeted, cancellable, revision-bound, and observable.
- Support the first useful loop: explorer/planner → implementer → verifier → independent reviewer → bounded fixer/reviewer repeat.
- Preserve single-agent-first defaults and existing explicit approval/safety rules.
- Make results resumable as server-owned projections and measurable for later evaluation.

**Non-Goals:**

- No default multi-agent council or automatic parallel implementation selection in the first wedge.
- No provider-specific routing or new model dependency.
- No automatic merge, release, or destructive cleanup without explicit policy.
- No project/global memory or automatic skill writing in this change; those are later roadmap phases built on the run evidence contract.

## Decisions

### 1. Server-owned run coordinator

Introduce a coordinator owned by the app server/runtime layer. It owns the run state machine, child-session links, budgets, cancellation, and public projections. The TUI, CLI, and ACP clients send commands and consume events; they do not construct live child loops.

Alternative rejected: implementing the loop separately in the TUI and CLI. That would duplicate lifecycle and persistence semantics and make ACP behavior diverge.

### 2. Explicit state transitions with durable evidence

Represent transitions and evidence as typed models with stable run, child, revision, and event identifiers. Persist terminal summaries and resumable active state through the existing session boundary, while treating in-flight process recovery as a separate limitation.

Alternative rejected: infer state from free-form child messages or transcript text. That makes cancellation, stale review detection, and automation unreliable.

Budget accounting uses an atomic ledger with reserved and committed units for turns, child count, review iterations, and wall-clock deadline. Limits are inclusive; a unit cannot be reserved after the limit. When terminal causes race, precedence is: explicit user cancellation, deterministic policy denial, budget/deadline exhaustion, stale/scope rejection, child execution failure, then successful completion. The winning cause is the first atomically recorded cause at the coordinator boundary; later causes are evidence, not state changes.

### 2a. Workspace identity and scope are first-class inputs

At run start, the coordinator records the repository commit, index/worktree dirty state, workspace path/identity, and a scope manifest. A write-capable run refuses a dirty primary workspace unless an explicit isolated-worktree or snapshot policy is selected. Every child result carries changed paths and source revision; reducers reject out-of-scope changes even when the revision is current. Cleanup is non-destructive by default and retains a changed workspace for explicit user disposition.

Alternative rejected: treating an exact commit hash as sufficient. A clean commit does not describe staged/uncommitted content or whether a child modified files outside the task boundary.

Workspace snapshots use the existing repository/worktree mechanism plus a run-owned immutable manifest of file content hashes and index state; they are not presented as crash recovery. The coordinator distinguishes baseline changes from run-owned changes by comparing hashes against the captured baseline. Allocation failure, restore failure, or cleanup ambiguity becomes `blocked` with the workspace retained and an explicit disposition request.

### 3. One writer by default; isolated parallelism as a guarded extension

The first loop uses one implementer workspace and read-only parallel exploration/review where safe. Write-capable parallel children require independently prepared worktrees and a reducer that checks overlapping paths and exact revisions before applying a result.

Alternative rejected: allowing concurrent writers in the primary workspace. It is faster only when coordination is perfect and creates unacceptable silent overwrite risk.

### 4. Verification and review are gates, not decoration

Each loop iteration records commands and outcomes. A valid blocking review finding enters a bounded fix/reverify cycle; timeouts, malformed output, unavailable checks, and stale revisions never become implicit approval.

Alternative rejected: treating reviewer prose or a green subset as merge readiness. The final evidence must identify skipped or unavailable validation explicitly.

### 5. Policy is inherited, never expanded

Child capabilities are the intersection of the run policy, parent permissions, and child role declaration. Deterministic safety rules and explicit human denial remain authoritative. The orchestration layer cannot bypass tool approval or sandbox policy.

Escalation is only available for a capability the parent policy permits but the child role omitted. A deterministic or parent-denied capability fails closed and cannot become allowed through a child or user approval prompt.

The app-server contract uses versioned typed request/response models and ordered event payloads. `start` is idempotent by client key; `get` and `evidence` are read-only; `cancel` requires the current run revision; `resume` requires an explicit new policy when budgets or workspace identity changed. Clients consume projections and watermarks rather than constructing child runtimes.

## Risks / Trade-offs

- **[Risk]** A state machine can become ceremony for small tasks → Keep the feature opt-in and provide a minimal one-implementer policy with low overhead.
- **[Risk]** Durable run state may be mistaken for crash recovery → Label in-flight process recovery separately and preserve the existing session limitation.
- **[Risk]** Independent review adds latency and cost → Bound reviewer count/turns/time and measure against a single-agent baseline.
- **[Risk]** Worktree cleanup can discard user work → Reuse existing dirty-state inspection and require explicit policy before destructive cleanup.
- **[Risk]** Typed schemas evolve → Version public contracts and use tolerant persistence migrations.
- **[Risk]** Benchmarks can reward cherry-picked orchestration wins → Use a committed fixture manifest, fixed environment, repeated runs, and explicit readiness thresholds rather than best-of-N results.

## Migration Plan

1. Ship typed models and coordinator behind an explicit feature/config flag; leave the existing `task` tool behavior unchanged.
2. Add app-server projections and CLI/TUI/ACP commands for start/status/cancel before enabling any automatic fixer loop.
3. Enable the single-writer implementer → verifier → reviewer loop for opt-in runs.
4. Add isolated parallel exploration and then guarded parallel writers only after conflict and cleanup tests pass.
5. Measure representative tasks against the single-agent baseline before recommending defaults.

Rollback is disabling the autonomous-run feature flag and leaving existing sessions, task calls, and worktrees available through their current paths. No existing transcript format is rewritten during initial rollout.

The initial benchmark gate uses at least 12 representative, versioned tasks (four each for bug fix, feature, and refactor), three repetitions per configuration in a pinned environment, and median plus p90 results. The loop is recommended only if it is no worse than single-agent on functional success and regression rate, and improves either review precision or human-rated usefulness without exceeding 2x median latency or cost proxy. If the gate is not met, the feature remains opt-in and the report records the failing dimension.
