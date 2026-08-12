# Proposal: Modular plugins and low-friction command safety

## Why

Oh My Vibe currently differentiates itself through durable memory, self-writing skills, isolated state, and safe upstream synchronization. Coding-agent users still face repeated approval prompts for routine terminal work, while allowing automation to make unrestricted shell decisions would be unsafe. A stable extension layer can provide sandbox backends and command-policy integrations without coupling future third-party plugins to the Oh My Vibe fork.

## What Changes

- Add a vendor-neutral plugin contract with manifest metadata, explicit enablement, lifecycle registration, and stable extension points.
- Add a Linux-first sandboxed command runner using an installed backend such as Bubblewrap (with Firejail compatibility), with explicit capability reporting and safe fallback behavior.
- Add command-safety policy evaluation that combines existing deterministic guardrails with sandbox status and optional plugin-provided analysis.
- Add configuration for sandbox mode, fallback mode, and policy mode while preserving existing permission defaults.
- Make sandbox and policy decisions auditable in tool results and logs.

## Capabilities

- `modular-plugins`
- `sandboxed-command-execution`
- `command-approval-policy`

## Impact

The Bash tool and configuration schema gain safety controls. Existing commands remain permission-compatible by default: sandboxing is opt-in until a backend and configuration enable it. Plugins run only when explicitly enabled and cannot silently weaken deny rules or bypass human approval. Vanilla Vibe is unaffected because all metadata, state, and entry points are Oh My Vibe-specific.
