## Purpose

Provide a layered approval decision that eliminates repetitive prompts for clearly safe commands without allowing an uncertain classifier or plugin to override deterministic safety rules.

## ADDED Requirements

### Requirement: Policy decisions have explicit outcomes
The command policy SHALL represent `allow`, `deny`, `sandbox`, and `ask` outcomes, together with a reason and evaluator identity.

#### Scenario: Deterministic analyzer recognizes a safe command
- **WHEN** a command is read-only or matches an explicitly configured safe pattern and its paths remain within the project boundary
- **THEN** the policy SHALL return an allow or sandbox decision with an explanatory reason

#### Scenario: Command is ambiguous
- **WHEN** no deterministic rule can establish that a command is safe
- **THEN** the policy SHALL return ask rather than allow

### Requirement: Optional model analysis is advisory
An optional LLM analyzer MAY classify commands, but its result SHALL be advisory and SHALL be unable to override core deny rules, sandbox startup safeguards, or an explicit human deny. The analyzer SHALL support allow, deny, and ambiguous outcomes and SHALL time out safely.

#### Scenario: LLM analyzer times out
- **WHEN** the configured analyzer does not return within its timeout
- **THEN** the policy SHALL treat the command as ambiguous and request human approval

#### Scenario: LLM says allow for a dangerous command
- **WHEN** the analyzer returns allow for a command rejected by deterministic guardrails
- **THEN** the final policy SHALL preserve the deterministic deny or ask result

### Requirement: Decisions are auditable
Each automated decision SHALL expose the policy mode, evaluator, sandbox state, and reason to the tool UI or structured execution result.

#### Scenario: Automated sandbox approval is shown
- **WHEN** a command runs without an interactive approval prompt
- **THEN** the user-visible result SHALL state that it was automatically approved and whether it ran sandboxed
