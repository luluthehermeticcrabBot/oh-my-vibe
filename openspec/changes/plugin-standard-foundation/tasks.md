## 1. Contract inventory

- [ ] 1.1 Inventory the merged registry, analyzer, sandbox, and safety boundaries against the proposed standard.
- [ ] 1.2 Record the initial manifest fields, capability vocabulary, API version policy, and trust levels.

## 2. Current-host conformance

- [ ] 2.1 Add manifest validation tests for required fields, duplicate names, unsupported versions, and invalid capabilities.
- [ ] 2.2 Add conformance tests for advisory authority, deterministic deny precedence, sandbox preservation, timeout, exception, malformed output, and lifecycle behavior.
- [ ] 2.3 Add explicit structured diagnostics for trust level, evaluator, failure, timeout, and isolation status where missing.

## 3. Isolation and adapter prerequisites

- [ ] 3.1 Document the boundary between trusted in-process plugins and process-isolated plugins.
- [ ] 3.2 Define process-isolation requirements and refusal behavior for untrusted plugins before implementation.
- [ ] 3.3 Draft Hermes Agent and OpenCode adapter mappings for manifests, decisions, permissions, sandbox state, errors, timeouts, and lifecycle.

## 4. SDK readiness gate

- [ ] 4.1 Add a conformance checklist and review evidence format.
- [ ] 4.2 Record SDK extraction exit criteria and explicitly defer standalone package publication until they pass.
- [ ] 4.3 Open a separate SDK implementation proposal only after at least one adapter mapping and isolation design are reviewed.
