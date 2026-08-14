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

Budget accounting uses an atomic ledger with reserved and committed units for turns, child count, review iterations, and wall-clock deadline. Limits are inclusive; a unit cannot be reserved after the limit. The terminal algorithm is: (1) acquire the run revision lock; (2) record a cause cutoff containing all causes and budget reservations visible at that lock; (3) evaluate the deadline at the cutoff time; (4) select the highest-priority visible cause using cancellation, deterministic policy denial, budget/deadline exhaustion, stale/scope rejection, child failure, success; (5) append the terminal evidence and increment the run revision in one transaction; (6) release the lock. A reservation is committed only if its child result is accepted, otherwise rolled back before step 2. A worker arriving after the cutoff retries against the finalized revision and can append only secondary evidence. The transaction commit is the linearization point.

### 2a. Workspace identity and scope are first-class inputs

At run start, the coordinator records the repository commit, index/worktree dirty state, workspace path/identity, and a scope manifest. A write-capable run refuses a dirty primary workspace unless an explicit isolated-worktree or snapshot policy is selected. Every child result carries changed paths and source revision; reducers reject out-of-scope changes even when the revision is current. Cleanup is non-destructive by default and retains a changed workspace for explicit user disposition.

Alternative rejected: treating an exact commit hash as sufficient. A clean commit does not describe staged/uncommitted content or whether a child modified files outside the task boundary.

Workspace snapshots use a run-owned immutable manifest containing repository identity, HEAD, index tree, tracked file hashes, untracked file hashes and contents, ignored-file path/type/content digests, symlink targets, and snapshot format version. They are not presented as crash recovery. The coordinator distinguishes baseline changes from run-owned changes by comparing sorted `(path, kind, digest, target)` tuples. Restore/remove compares the current tuple set to the expected baseline-plus-run-owned tuple set; any user edit, new path, deleted baseline path, ignored-file divergence, or concurrent change returns `workspace_conflict`. A disposition is an immutable record with `disposition_id`, expected tuple-set digest, operation (`retain`, `export`, `discard`, `restore`), changed paths, confirmation identity, and status. Its atomic transitions are `pending → confirmed → applied` or `pending → cancelled`; failed application becomes `blocked` and retains the workspace. Allocation, snapshot, or cleanup failure becomes `blocked` with an explicit disposition request.

Each workspace generation stores one nullable `active_disposition_claim` containing a unique fenced token, owner process epoch, and lease expiry. Applying a disposition executes one atomic compare-and-set over `(workspace_id, generation, expected_tuple_digest, active_disposition_claim=NULL)` to set the claim and transition the disposition to `confirmed`. All filesystem mutations run through a server-owned serialized mutation executor with a durable per-workspace mutation lock. Lease validation, intent acquisition, the filesystem call, and recording `applied`/`unknown` are one executor critical section; lease renewal and expiry reconciliation cannot supersede the fence until that section exits. A stale worker is rejected with `fence_lost` before entering the section. A process crash during the call leaves `unknown`, which startup reconciliation marks `blocked` after tuple inspection. Retries with the same token are idempotent, while any other token receives `disposition_conflict`. A failed application transitions `confirmed → blocked` and atomically clears the claim while retaining the workspace; a retry must create a new disposition ID and revalidate the generation/digest. On startup, or when a lease expires, the server reconciles the journal transactionally: `applied` is finalized, while `unknown` is marked `blocked` with `coordinator_lost` and the workspace is retained for tuple inspection. The claim is cleared only when the operation reaches `applied`, `cancelled`, `blocked`, or crash-reconciled `blocked`.

Autonomous-run persistence is a server-owned ledger separate from the ordinary session event projection. It stores the run projection, revision, event envelope, terminal evidence, and replay watermark in one transaction, with versioned migrations and retention metadata. ADR 0006's limitation remains: committed run state and events can be recovered in a new process, but live child processes and open callbacks cannot. Event retention truncation creates `event_gap` with a snapshot whose watermark was committed in the same ledger transaction.

### 3. One writer by default; isolated parallelism as a guarded extension

The first loop uses one implementer workspace and read-only parallel exploration/review where safe. Write-capable parallel children require independently prepared worktrees and a reducer that checks overlapping paths and exact revisions before applying a result.

Alternative rejected: allowing concurrent writers in the primary workspace. It is faster only when coordination is perfect and creates unacceptable silent overwrite risk.

### 4. Verification and review are gates, not decoration

Each loop iteration records commands and outcomes. A valid blocking review finding enters a bounded fix/reverify cycle; timeouts, malformed output, unavailable checks, and stale revisions never become implicit approval.

Alternative rejected: treating reviewer prose or a green subset as merge readiness. The final evidence must identify skipped or unavailable validation explicitly.

### 5. Policy is inherited, never expanded

Child capabilities are the intersection of the run policy, parent permissions, and child role declaration. Deterministic safety rules and explicit human denial remain authoritative. The orchestration layer cannot bypass tool approval or sandbox policy.

Escalation is only available for a capability the parent policy permits but the child role omitted. A deterministic or parent-denied capability fails closed and cannot become allowed through a child or user approval prompt.

The app-server contract uses versioned typed request/response models and ordered event payloads. `start` is idempotent by client key; `get` and `evidence` are read-only; `cancel` requires the current run revision; `resume` requires an explicit new policy when budgets or workspace identity changed. Each event envelope has a per-run sequence and event ID; replay after a watermark is contiguous or returns `event_gap` with a replacement snapshot. A mutating response is committed before its notification is published. Clients consume projections and watermarks rather than constructing child runtimes.

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

The benchmark protocol is a future implementation artifact, not a runnable benchmark in this planning PR. Task 5.1 MUST replace the current schema with an immutable fixture manifest whose every task has an exact repository commit, prompt/policy file digest, executable acceptance command, model/provider identifier, lockfile digest, runtime image, and seed; the implementation PR MUST fail validation if any referenced artifact is missing. Paired comparison requires the same fixture and repetition ID across configurations; invalid pairs are excluded from all configurations and reported, and fewer than two valid repetitions makes a fixture inconclusive. `success_rate` and `regression_rate` use paired valid repetitions; `review_precision` is undefined when no blocking findings exist and cannot satisfy an improvement gate; cost proxy is total model input/output tokens plus tool wall-time seconds, reported in fixed units; human usefulness uses two independent 1–5 ratings anchored in the protocol. Reports contain median and p90 latency/cost. Recommendation requires no worse functional success or regression rate, improvement in review precision or mean usefulness by at least 0.25, and no more than 2x median latency or cost; otherwise the feature remains opt-in with machine-readable failed dimensions.
