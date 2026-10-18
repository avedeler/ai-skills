# Design

## Context

See proposal.md. The optional router installer already copies the canonical skill
and Codex profile safely. Cloud sessions can start at a previous checkout and
native collaboration does not necessarily load CLI role configuration.

## Goals / Non-Goals

Goals: observable startup prerequisites, preserved user content, portable source
packages, and a tested read-only preflight. Native calls retain host policy.
Non-goals: intercept collaboration tools, change the running root model, invent
effective model identity, initialize other projects, or publish an environment.

## Decisions

- Add `adapters/openspec-model-router/cloud.py` with `install`, `verify` and
  `preflight` commands. Common options name `--workspace`, `--skills-dir`,
  `--openspec-command` and `--openspec-version`. Use a reviewed source checkout;
  Python performs no network installation. Defaults use the current workspace,
  user skill directory and the existing executable, not guessed host credentials.
- Reuse the router installer for its package/profile. Copy the complete canonical
  development-team package only if absent; accept an existing byte-identical
  package, including a compatible pre-existing symlink, without changing it.
  Reject conflicting or broken paths. Preflight all destination conflicts before
  writes; use staged directory/file publication for new content.
- A checked-in `cloud-AGENTS.md` template has exactly one uniquely named managed
  block and substitutes absolute reviewed paths. Append to existing unmanaged
  text without changing it. Identical repeats are no-ops; differing/duplicated or
  malformed managed blocks fail. Require the router/profile before any delegation;
  require development-team discovery and preflight before code changes. Read-only
  noncoding analysis does not need an artificial apply change. Never overwrite
  global model configuration.
- `verify` compares canonical package/profile bytes, the managed block and the
  configured exact CLI version. Avoid passing just because directory names exist.
- `preflight` first verifies the environment, then runs the chosen executable in
  `--project`. Optional `--project-openspec-command` and
  `--project-openspec-version` select a project wrapper independently from the
  installed environment's command/version. Resolve installation commands to a
  stable absolute path and relative project wrappers against the project. It uses
  `context --json`, and for `--phase apply` (default) requires
  `--change`, `status --change ... --json` and `instructions apply --change ...
  --json`. Fail on nonzero exits, malformed JSON, absent root, mismatched selected
  change or non-ready apply state. `--phase explore` needs context only. Subprocess
  calls use argv, timeouts and telemetry disabled, never a shell. A project's
  wrapper can be explicitly selected; unsupported older commands are a reported
  compatibility limit, never silently replaced with another planning root.
- Render managed commands in one substitution pass with shell-quoted arguments
  and separate display values. Reject dangling instruction symlinks and unsafe
  destination parents before writes, and reject unexpected nonregular package
  entries without reading them. Verification must not import unused installers
  or generate source caches. Tests inspect actual subprocess cwd, argv and
  telemetry environment rather than invocation counts alone.
- Source this repository's instructions and OpenSpec plan for the change itself.
  The repository previously had no root; add a minimal spec-driven root without
  generated host commands or any changes to other repositories' workflows.

## Risks / Trade-offs

- Instructions cannot enforce native calls → require explicit routing records,
  verify accepted requests in a live bounded handoff, disclose absent telemetry.
- A setup checkout can be stale → pin the published source commit in the final
  bootstrap script and install from that checkout, preserving the user's checkout.
- Configuration persistence differs from local files → provide a concrete setup
  script for environment review/publication and require fresh-session discovery.
- Existing local customizations → fail instead of replacing differences, and
  test conflict/no-write behavior. No permissions or credentials are modified.

## Migration Plan

Test in temporary roots, install the router and workspace section in this running
workspace, verify a real selected change, and exercise accepted explicit model
requests. Publish source as a draft PR and prepare a pinned bootstrap script.
The environment owner reviews and publishes its setup configuration; a fresh
task validates persistence. Rollback removes only newly managed installations or
the exact managed block after preserving any later edits; existing text remains.
