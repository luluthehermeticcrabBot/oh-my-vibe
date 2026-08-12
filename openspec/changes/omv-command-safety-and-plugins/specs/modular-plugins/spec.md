## Purpose

Provide a stable, vendor-neutral extension contract so sandbox backends, command analyzers, approval providers, and future integrations can be developed independently and potentially adopted by vanilla Vibe later.

## ADDED Requirements

### Requirement: Plugins use explicit manifests and enablement
Oh My Vibe SHALL discover plugins through the `omv.plugins` entry-point group and SHALL require a valid manifest plus explicit enablement before loading a plugin.

#### Scenario: Disabled plugin is installed
- **WHEN** a package exposes an `omv.plugins` entry point but is not enabled in Oh My Vibe configuration
- **THEN** Oh My Vibe SHALL NOT import or execute the plugin registration function

#### Scenario: Enabled plugin has an invalid manifest
- **WHEN** an enabled plugin does not provide a valid name, version, API version, and kind
- **THEN** Oh My Vibe SHALL reject the plugin, report the validation reason, and continue without it

### Requirement: Plugin capabilities are constrained
A plugin SHALL declare capabilities and SHALL NOT change core deny rules, disable sandbox fallback safeguards, or grant itself permission to bypass human approval.

#### Scenario: Plugin attempts to weaken a deny decision
- **WHEN** a plugin returns an allow decision for a command rejected by a core deny rule
- **THEN** the core policy SHALL preserve the deny decision

### Requirement: Plugin failures are isolated
A plugin load or callback failure SHALL be logged with the plugin identity and SHALL not prevent the core CLI or built-in tools from starting.

#### Scenario: Plugin registration raises
- **WHEN** an enabled plugin raises during registration
- **THEN** Oh My Vibe SHALL skip that plugin and continue loading other plugins and built-in tools
