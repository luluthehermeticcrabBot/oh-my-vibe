# Agent Orchestration v1 benchmark protocol schema

This planning document defines the contract for task 5.1; it is not an executable benchmark and MUST NOT produce readiness claims. The implementation PR must replace the planning manifest with immutable fixture artifacts and fail validation if any required field or referenced artifact is missing.

## Required fixture contract

Each fixture must provide the exact repository commit, SHA-256 digests for prompt and policy files, an executable acceptance command, model/provider identifier, dependency-lock digest, runtime image identifier, deterministic seed, and three paired repetition IDs for each configuration. The committed planning manifest lists the required 12 fixture IDs and category counts.

The replacement manifest SHALL use this canonical flat record shape for every fixture:

```yaml
id: string
category: bug_fix|feature|refactor
repository_commit: 40-hex SHA
prompt_file_path: string
prompt_file_sha256: 64-hex SHA
policy_file_path: string
policy_file_sha256: 64-hex SHA
acceptance_command: string
acceptance_cwd: string
acceptance_timeout_seconds: integer
model_provider_id: string
model_id: string
lockfile_sha256: 64-hex SHA
runtime_image_id: string
seed: integer
repetition_ids:
  - {configuration: string, repetition_id: string, result_path: string}
```

Artifact paths SHALL be repository-relative or immutable content-addressed
URIs; absolute paths and floating branch/tag references are invalid. The
validator SHALL resolve every path, verify every digest, require exactly three
repetition records per configuration, and reject duplicate pairing keys. The
The planning manifest is the schema declaration; task 5.1 must populate all fields
and all 12 fixture records before execution is permitted.

The fixture identity field set is exactly: `id`, `category`,
`repository_commit`, `prompt_file_path`, `prompt_file_sha256`,
`policy_file_path`, `policy_file_sha256`, `acceptance_command`,
`acceptance_cwd`, `acceptance_timeout_seconds`, `model_provider_id`, `model_id`,
`lockfile_sha256`, `runtime_image_id`, and `seed`. Suite-level `artifact_root`,
`result_schema`, and `repetition_ids` are excluded from the fixture identity.
`fixture_fingerprint` is the lowercase SHA-256 of canonical UTF-8 JSON of that
exact field set: keys are sorted lexicographically, every string is NFC-normalized,
numbers use JSON shortest decimal form, booleans/null use JSON literals, arrays
preserve manifest order, separators are `,` and `:`, and no trailing newline is
hashed. This same canonicalization is used by manifest and result validators.

## Execution protocol

Run the same fixture and repetition ID in every configuration. Pin repository, prompt, policy, provider, lockfile, runtime image, and seed. A repetition is valid only when setup, agent execution, and acceptance tests produce attributable results. Invalid repetitions invalidate the pair across all configurations and are reported; fewer than two valid repetitions makes that fixture inconclusive.

## Metrics

- `success_rate`: paired valid repetitions whose full acceptance-test set passes divided by paired valid repetitions.
- `regression_rate`: paired valid repetitions with a failure absent in the single-agent baseline divided by paired valid repetitions.
- `review_precision`: valid blocking findings divided by all reported blocking findings; undefined when no blocking findings exist and never eligible to satisfy an improvement gate.
- `usefulness`: mean of two independent ratings using anchored 1–5 criteria for correctness, evidence quality, and operator effort.
- `cost_proxy`: model input tokens + model output tokens + tool wall-time seconds, reported in fixed units.
- Report median and p90 latency and cost, sample counts, paired IDs, and invalid repetitions.

Each result file SHALL use `benchmark-result-v1` with `fixture_id`,
`configuration`, `repetition_id`, `valid`, `failure_reason`,
`fixture_fingerprint`, `repository_commit`, `prompt_file_path`,
`prompt_file_sha256`, `policy_file_path`, `policy_file_sha256`,
`acceptance_command`, `acceptance_cwd`, `acceptance_timeout_seconds`,
`model_provider_id`, `model_id`, `lockfile_sha256`, `runtime_image_id`, `seed`,
`acceptance_passed`, `review_findings` (a list of `{severity, valid, category}`
records), `latency_seconds`, `input_tokens`, `output_tokens`, `tool_seconds`,
and `human_ratings` (exactly two `{rater_id, correctness, evidence_quality,
operator_effort}` records, each score 1–5) fields. `fixture_fingerprint` is the
lowercase SHA-256 of canonical UTF-8 JSON containing every fixture identity
field except repetition and result fields, with object keys sorted and no
whitespace. The validator SHALL reject a result whose identity does not match
the fixture record or whose acceptance command, environment, or artifact digest
differs from the manifest.

## Readiness gates

The loop is recommended only if it has no lower functional success rate, no higher regression rate, either higher review precision or at least 0.25 higher mean usefulness, and no more than 2x median latency or cost proxy versus single-agent on the same paired fixtures. Missing baselines, missing artifacts, fewer than two valid repetitions, or an unpinned environment produce an inconclusive result; they do not pass. If a gate fails or is inconclusive, the feature remains explicitly opt-in and the machine-readable report records the failed dimension.
