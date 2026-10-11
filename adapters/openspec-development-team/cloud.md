# Cloud workspace integration

Observations below are dated **2026-10-11**. They describe this tested hosted
surface and do not guarantee that another host/session exposes the same tools.
Start with [project onboarding](onboarding.md). Manually integrate the generated
fragments into existing instructions, ignores and CI. In the dashboard, manually
set the setup script to `bash scripts/team_setup.sh`, then restart/recreate the
workspace as required. No dashboard configuration was applied by these checks.

Run:

```sh
bash scripts/team_setup.sh
python3 scripts/team_install.py verify --project . --config .team/install.json
```

A hosted session does not necessarily load local Codex CLI role files. Its native
collaboration interface was observed as `collaboration.spawn_agent` with
`task_name`, `message`, `fork_turns`, `model` and `reasoning_effort`. There is no
custom `agent_type` argument on this surface. For an explicitly configured native
model override, use `fork_turns="none"` and supply the bounded role handoff and
canonical prompt path in `message`. Full-history forks inherit the parent model
and reject overrides. Native permission and task authorization still govern calls.

The dated model/tool discovery advertised `gpt-6.1-sol`, `gpt-6-astra` and
`gpt-6-luna`, including the requested `medium`/`high` efforts. Requested model
override calls were accepted in the observed team work. The actual execution model
was not independently observed. Discovery and accepted calls do not establish
account entitlement, billing route, inference quality or model identity. No API
billing fallback is configured. A preset cannot reconfigure an active root session;
choose its root model through the host's own supported setup.

Agents on this surface share a filesystem. Native delegation supplies neither
per-agent filesystem isolation nor writer locks. Reuse the assigned native
workspace, serialize all writers, and freeze the complete candidate before
independent review. Avoid allocating a new worktree merely for each role. Use
host-managed restrictions when enforced reviewer permissions are required.

The optional local CLI adapter was checked with **Codex CLI 0.159.2**. Its native
role configuration and `features list` loader observation are separate from the
hosted collaboration surface. Neither static checks nor a loader acceptance is a
live team pilot. OpenCode verification in this change is static; the existing adapter also
supports launching OpenCode.

Discover and preserve the existing project's pinned OpenSpec wrapper, active
schema and planning store before architecture/planning/sync. The optional wrapper
observation checks only an exact version line and an existing project-relative
root. It does not prove those are the actual CLI context or infer sync commands.
External planning stores need the repository's manual integration. For fresh
initialization, explicitly select a reviewed current version, follow its upstream
help and audit it; no initialization or package installation happens in setup.

After filling the project facts, give a concrete feature prompt:

> Use the shared development team for the approved feature. Inspect architecture
> and our existing OpenSpec workflow first. Reuse the assigned workspace, implement
> within scope, run the required checks, obtain independent code/security review,
> and synchronize documentation/specs. Deliver a review-ready PR. Merge and
> deployment remain mine.

Record actual checks, role handoffs and unresolved gaps for that exact candidate.
Setup completion, native loader acceptance and live pilot results are distinct.
