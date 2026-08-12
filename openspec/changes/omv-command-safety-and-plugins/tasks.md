## 1. Specification and public contracts

- [x] 1.1 Validate the proposal, capability specs, design, and task graph with strict OpenSpec validation.
- [x] 1.2 Add typed plugin manifest, registry, capability declarations, and isolated discovery tests.
- [x] 1.3 Add public safety decision, execution plan, analyzer, and sandbox backend protocols.

## 2. Configuration

- [x] 2.1 Add the `tools.bash.safety` schema with compatibility-preserving defaults.
- [x] 2.2 Add config round-trip and invalid-value tests.
- [x] 2.3 Document plugin installation, enablement, capabilities, and safety modes.

## 3. Sandboxed execution

- [x] 3.1 Implement capability-detected Bubblewrap execution with Firejail fallback and argv construction without executing commands during detection.
- [x] 3.2 Implement local sandbox execution with timeout, output limits, cancellation, and distinct startup-failure reporting.
- [x] 3.3 Integrate sandbox execution into Bash while preserving tool I/O transports and existing permission guardrails.
- [x] 3.4 Add tests for sandbox command construction, unavailable backend behavior, fallback policy, and denial precedence.

## 4. Command approval policy

- [x] 4.1 Implement deterministic policy composition over existing Bash guardrails.
- [x] 4.2 Implement the advisory analyzer plugin protocol with timeout and fail-to-ask behavior.
- [x] 4.3 Add an optional LLM analyzer adapter boundary without embedding provider credentials or unsafe auto-allow behavior.
- [x] 4.4 Include evaluator, sandbox, and fallback information in structured tool results and UI data.
- [x] 4.5 Add regression tests for safe, dangerous, ambiguous, timeout, and explicit-human-deny scenarios.
- [x] 4.6 Ensure advisory results cannot bypass core permissions or managed-terminal safety policy.

## 5. Verification and release gates

- [x] 5.1 Add focused tests for plugin API and safety namespace contracts.
- [x] 5.2 Run focused safety/plugin tests, lint, formatting, type checks, CLI smoke checks, and lockfile validation.
- [x] 5.3 Update CI to run safety and plugin tests before release without assuming the separate branding migration is present.
