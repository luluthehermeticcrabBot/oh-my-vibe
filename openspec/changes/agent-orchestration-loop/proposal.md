## Why

Oh My Vibe already has server-owned child sessions, a typed `task` tool, isolated worktree primitives, and documented single-agent-first orchestration principles, but users do not yet have a dependable autonomous development loop. Delegation is currently a one-shot subagent call rather than a bounded workflow that can explore, implement, verify, review, fix valid findings, and stop with auditable evidence. This is the highest-leverage first capability for making the project worthy of the Oh My-* name.

## What Changes

- Add an explicit autonomous development run model with a bounded lifecycle: plan/explore, implement, verify, independent review, and optional fix/reverify.
- Add structured task and review results rather than relying on prose-only coordination.
- Add configurable budgets and stop conditions for wall-clock time, turns, child count, and review iterations.
- Add isolated-worktree execution for parallel writers and review/fix lanes; read-only exploration remains safe without a writer worktree.
- Add stale-head and changed-scope checks so a reviewer result cannot be applied to a different revision silently.
- Add cancellation, failure classification, and resumable run state through the server-owned session boundary.
- Keep the default single-agent path unchanged; autonomous loops are explicit and opt-in.
- Emit user-visible lifecycle events and a concise final evidence report across CLI/TUI and ACP projections.

## Capabilities

### New Capabilities

- `autonomous-development-loops`: Bounded, auditable development workflows that coordinate implementers, verifiers, independent reviewers, and optional fix iterations.
- `structured-agent-orchestration`: Typed child-task contracts, budgets, worktree isolation, stale-state protection, lifecycle events, and result reduction.

### Modified Capabilities

- None. Existing child sessions, task delegation, worktrees, and session persistence are implementation foundations; this change adds the new workflow contract without redefining their existing requirements.

## Impact

- Core: orchestration state machine, typed subagent/task/review contracts, cancellation and budget enforcement, result reduction, and exact-revision checks.
- App server: server-owned autonomous-run lifecycle, child-session links, persistence, event projections, and delivery-neutral APIs.
- CLI/TUI/ACP: explicit start/status/cancel/resume surfaces and structured lifecycle/evidence rendering.
- Git/worktrees: isolated writer/reviewer worktrees, branch and dirty-state safety, and cleanup policy.
- Configuration: opt-in workflow settings with bounded defaults and per-run overrides.
- Tests and evaluation: public-path lifecycle tests, failure/retry tests, stale-head tests, worktree isolation tests, and a small benchmark comparing single-agent and loop configurations.
- No new provider dependency is required; the design remains provider-neutral and uses the existing agent manager and subagent runner.
