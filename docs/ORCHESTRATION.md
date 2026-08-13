# Oh My Vibe orchestration principles

Oh My Vibe is single-agent-first. Extra agents are an explicit, evidence-driven optimization rather than a default requirement.

## Product decisions

- **Implementer:** owns the working tree and remains the default execution path.
- **Explorer/researcher:** read-only repository, history, and documentation discovery. Parallel exploration is preferred when it does not mutate shared state.
- **Reviewer:** an independent subagent with a fresh context window. It inspects the complete diff and relevant tests, runs focused validation, and reports only actionable findings with severity and evidence. The implementer must not pre-digest the review into its context.
- **Planner:** opt-in for large refactors, migrations, cross-platform changes, and tasks with multiple acceptance criteria. Small tasks skip planning ceremony.
- **Verifier/fixer loop:** validation is a workflow state: run checks, classify failures, fix confirmed regressions, and rerun. Tests, builds, and explicit acceptance criteria outrank agent consensus.

There is deliberately no default council, oracle, or observer agent. A council creates communication overhead unless independent proposals have a bounded decision rubric. An oracle is only meaningful when a reducer can select among independently generated candidates. Observability belongs in structured telemetry, not an LLM role.

## On-the-fly subagents

Prompt-generated subagents are useful when the task reveals a genuinely independent lane, but they must be bounded by runtime policy:

1. The parent states the goal, scope, inputs, output schema, timeout, and write permissions.
2. Read-only workers default to isolated or no-write execution.
3. Parallel writers require isolated worktrees and an explicit merge/reducer step.
4. Results are typed or structured where possible; prose-only coordination is a fallback.
5. The parent verifies claims against repository state and test output before presenting completion.
6. Fan-out is budgeted by concurrency, tokens, and wall-clock time.

This adopts the useful part of Claude Code's prompt-created subagents—dynamic specialization—without making arbitrary role creation an uncontrolled source of cost or state collisions.

## Reviewer modes

The initial reviewer implementation should support two explicit modes:

- **Post-change review:** inspect a branch, commit, or working tree and return blocking/non-blocking findings.
- **Advisory review:** observe an active agent through a separate context and inject concise concerns, but never silently modify files or override the implementer.

Post-change review is the first implementation target because it has a clear boundary and deterministic evidence. Advisory review should follow only after lifecycle, cancellation, privacy, and cost behavior are tested.

## What to learn from Oh My Pi

The strongest ideas to borrow are typed subagent results, isolated worktrees, a reviewer with an independent context/model, structured task batching, persistent sessions/branch summaries, and extension hooks that can enforce policy around tool calls. Hash-anchored edits and strong stale-state detection are also attractive for reducing accidental overwrites.

Oh My Vibe should not copy every tool or role. It should preserve its Python/Textual architecture, provider neutrality, explicit approval semantics, and simpler default surface. New orchestration features must beat a single-agent baseline on success, regression rate, latency, or cost on a measured task set before becoming recommended defaults.

## Evaluation plan

Compare these configurations on representative Oh My Vibe maintenance tasks:

1. single implementer;
2. explorer → implementer;
3. implementer → independent reviewer;
4. planner → implementer → independent reviewer;
5. parallel isolated implementations plus deterministic selection.

Record functional success, regression rate, review precision, wall-clock time, token cost, number of tool calls, and human-rated usefulness. Report median and tail behavior, not only best-of-N results.
