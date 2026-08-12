## Purpose

Provides a deliberate, user-controlled path for moving selected upstream Vibe configuration and state into the isolated Oh My Vibe state namespace without data loss or implicit adoption.

## ADDED Requirements

### Requirement: Migration source and destination are explicit

Migration tooling MUST require the user to identify both the source and destination before copying state and MUST reject ambiguous implicit locations.

#### Scenario: Missing source is rejected

- **WHEN** migration is requested without a source path
- **THEN** the tool rejects the request without reading or writing state

#### Scenario: Missing destination is rejected

- **WHEN** migration is requested without a destination path
- **THEN** the tool rejects the request without modifying the source

### Requirement: Migration performs validation before writing

The migration tool MUST provide a read-only validation or dry-run mode and MUST complete validation before any write operation begins.

#### Scenario: Dry run preserves both locations

- **WHEN** the user runs migration in dry-run mode
- **THEN** the tool reports planned actions and neither location is changed

#### Scenario: Invalid input prevents writes

- **WHEN** validation detects malformed or unsupported input
- **THEN** migration fails before writing any destination data

### Requirement: Migration preserves the source

A successful migration MUST copy selected data without deleting or rewriting the source location and MUST report the destination and copied scope.

#### Scenario: Successful explicit copy

- **WHEN** the user confirms a valid migration from a selected source to a selected destination
- **THEN** the selected destination data is written, the source remains unchanged, and the result identifies both paths
