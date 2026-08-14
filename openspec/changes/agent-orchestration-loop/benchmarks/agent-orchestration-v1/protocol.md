# Agent Orchestration v1 benchmark protocol

## Execution

- Run every manifest fixture in each listed configuration for three repetitions.
- Use the fixture repository revision, prompt, policy, seed, and acceptance-test command exactly as recorded.
- Pin the environment to the recorded Python/lock/provider configuration; record the resolved commit, model identifier, tool policy, wall time, token/cost proxy, and all command results.
- A repetition is valid only when setup, agent execution, and required acceptance tests all produce attributable results. Invalid repetitions are reported and never silently substituted.

## Metrics

- `success_rate`: valid repetitions whose complete acceptance-test set passes / valid repetitions.
- `regression_rate`: repetitions with a failure absent in the single-agent baseline / valid repetitions.
- `review_precision`: valid blocking findings / all reported blocking findings, with zero reported findings treated as undefined rather than perfect.
- `usefulness`: mean of two independent human ratings on a documented 1–5 rubric covering correctness, evidence quality, and operator effort.
- Report median and p90 latency and cost proxy for each configuration; report sample counts and invalid repetitions.

## Readiness gates

The loop is recommended only when compared with single-agent on the same valid fixtures and repetitions it has:

1. no lower functional success rate;
2. no higher regression rate;
3. either higher review precision or at least 0.25 higher mean usefulness;
4. no more than 2x median latency or cost proxy.

If any gate fails, the machine-readable report marks the failed dimension and the feature remains explicitly opt-in. A missing baseline, fewer than two valid repetitions for a fixture/configuration, or an unpinned environment makes the comparison inconclusive rather than green.
