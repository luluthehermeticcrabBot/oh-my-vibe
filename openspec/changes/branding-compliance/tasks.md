## 1. Specification and inventory

- [ ] 1.1 Review the repository-wide branding/state/distribution inventory and define the final canonical-name compatibility policy.
- [ ] 1.2 Add the branding OpenSpec capability documents and invariant fixture contract.

## 2. Executable identity and state

- [ ] 2.1 Change package metadata and canonical entry points to `oh-my-vibe`, `omv`, `omv-acp`, and `omv-app-server`.
- [ ] 2.2 Change global state resolution and all dependent logs, caches, skills, agents, and ACP paths to the `~/.omv` / `OMV_HOME` contract.
- [ ] 2.3 Add explicit migration tooling and documentation with dry-run, validation, source preservation, and explicit-write tests.

## 3. User-facing branding and distribution

- [ ] 3.1 Update README, AGENTS.md, CHANGELOG.md, onboarding, updater, installer, and relevant documentation with Oh My Vibe identity and disclaimer.
- [ ] 3.2 Replace product-facing upstream logos, icons, labels, URLs, and Zed integration metadata while retaining factual attribution where appropriate.
- [ ] 3.3 Update Nix, release scripts, packaging specs, archive names, and CI/release commands to use the canonical downstream identity.

## 4. Verification and compatibility

- [ ] 4.1 Implement the repository compatibility checker and fixture tests for package, executable, state, updater, installer, and distribution invariants.
- [ ] 4.2 Add wheel metadata inspection and `--help` smoke tests for all canonical executables.
- [ ] 4.3 Add CI and release gates for compatibility, lockfile, lint, type, focused, and full-suite validation.
- [ ] 4.4 Run the complete test suite and perform a final repository scan for accidental product-branding regressions.

## 5. Release and follow-up

- [ ] 5.1 Document the migration window, deprecated aliases if retained, rollback behavior, and upgrade notes.
- [ ] 5.2 Open a focused pull request and update issue #2 with the implementation status.
