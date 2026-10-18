# Proposal

## Why

Installing a CLI and symlinking a skill catalog does not make hosted sessions
load the routing policy or inspect the project's OpenSpec workflow. A workspace
can start from an older source revision and silently omit a newly added skill.

## What Changes

- Install or verify the model router with its optional Codex profile and the
  canonical development-team package from a reviewed checkout.
- Add a managed workspace AGENTS.md section requiring skill loading, explicit
  supported model/effort assignments and project-specific OpenSpec discovery.
- Provide read-only installation verification and project preflight commands
  that fail clearly on missing tools, conflicting installs or missing apply
  context, without initializing or migrating a project.
- Document pinned setup, environment publishing and fresh-session acceptance;
  distinguish instructions and accepted calls from runtime enforcement.

## Capabilities

### New Capabilities

- `cloud-workflow-startup`: Reviewed skill installation, workspace instructions
  and read-only workflow readiness checks for hosted development sessions.

### Modified Capabilities

None. Existing projects retain their own wrappers, schemas and planning stores.

## Impact

Optional Codex adapter, tests and setup documentation. Standard-library Python
only. No global model configuration rewrite, credentials, production changes,
automatic project initialization or environment publication.
