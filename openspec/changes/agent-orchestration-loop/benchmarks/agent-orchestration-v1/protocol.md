# Agent Orchestration v1 benchmark protocol schema

This planning document defines the contract for task 5.1; it is not an executable benchmark and MUST NOT produce readiness claims. The implementation PR must replace the planning manifest with immutable fixture artifacts and fail validation if any required field or referenced artifact is missing.

## Required fixture contract

Each fixture must provide the exact repository commit, SHA-256 digests for prompt and policy files, an executable acceptance command, model/provider identifier, dependency-lock digest, runtime image identifier, deterministic seed, and three paired repetition IDs for each configuration. The committed planning manifest lists the required 12 fixture IDs and category counts.

## Execution protocol

Run the same fixture and repetition ID in every configuration. Pin repository, prompt, policy, provider, lockfile, runtime image, and seed. A repetition is valid only when setup, agent execution, and acceptance tests produce attributable results. Invalid repetitions invalidate the pair across all configurations and are reported; fewer than two valid repetitions makes that fixture inconclusive.

## Metrics

- `success_rate`: paired valid repetitions whose full acceptance-test set passes divided by paired valid repetitions.
- `regression_rate`: paired valid repetitions with a failure absent in the single-agent baseline divided by paired valid repetitions.
- `review_precision`: valid blocking findings divided by all reported blocking findings; undefined when no blocking findings exist and never eligible to satisfy an improvement gate.
- `usefulness`: mean of two independent ratings using anchored 1–5 criteria for correctness, evidence quality, and operator effort.
- `cost_proxy`: model input tokens + model output tokens + tool wall-time seconds, reported in fixed units.
- Report median and p90 latency and cost, sample counts, paired IDs, and invalid repetitions.

## Readiness gates

The loop is recommended only if it has no lower functional success rate, no higher regression rate, either higher review precision or at least 0.25 higher mean usefulness, and no more than 2x median latency or cost proxy versus single-agent on the same paired fixtures. Missing baselines, missing artifacts, fewer than two valid repetitions, or an unpinned environment produce an inconclusive result; they do not pass. If a gate fails or is inconclusive, the feature remains explicitly opt-in and the machine-readable report records the failed dimension.
