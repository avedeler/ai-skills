# Codex and OpenCode adapters

These optional adapters register the [shared development team](../../skills/openspec-development-team/SKILL.md)
with native host agents. The interactive session is the coordinator; the seven
specialist roles run on demand. Every role, including the coordinator, can select
its own model. The core skill remains vendor- and model-agnostic.

There is one small standard-library renderer/launcher, one model settings file,
and no copied role prompts, scheduler, plugin, background service, or new task
database. Codex role files point agents to the canonical Markdown. OpenCode uses
native `{file:...}` inclusion of that same Markdown. Core prompts, handoffs,
testing/correction rules and OpenSpec/worktree guidance are maintained only under
`skills/openspec-development-team/`.

## Requirements

- Python **3.11+** for the adapter and repository tests. The standalone core
  readiness checker still supports Python 3.10+.
- A local clone of this repository, kept at a reviewed revision during a run.
- Codex CLI or OpenCode, already configured with the desired models/providers.
- The target project's OpenSpec integration, test tools and authorized execution
  environment. Rendering does not install them or supply credentials.

Native configuration loading was checked with **Codex CLI 0.159.2** and
**OpenCode 1.18.35**. See [compatibility and verification](compatibility.md).
Hosted Codex sessions may use a different agent API and may not load local CLI
configuration. These adapters target the native CLIs; they do not reconfigure an
already-running hosted chat session.

## Choose models

Copy [models.example.json](models.example.json) to a local settings file. It lists
all eight roles for both hosts. Empty objects inherit the host's normal defaults;
no model or provider is imposed. Set overrides only where needed, for example:

```json
{
  "schema_version": 1,
  "codex": {
    "coordinator": {"model": "your-coordinator-model"},
    "architect": {"model": "your-design-model", "model_reasoning_effort": "high"},
    "implementer": {"model": "your-coding-model"},
    "code-reviewer": {"model": "your-review-model"}
  },
  "opencode": {
    "coordinator": {"model": "provider-a/coordinator-model"},
    "architect": {"model": "provider-b/design-model", "variant": "high"},
    "implementer": {"model": "provider-a/coding-model"},
    "code-reviewer": {"model": "provider-c/review-model"}
  }
}
```

These IDs are illustrative placeholders. Replace them with models available in
your host; only use reasoning levels or variants that the selected model supports.
The other roles are `planner`, `test-engineer`, `security-reviewer`, and
`documentation-steward`. Omitted roles/settings inherit; empty strings and unknown
fields are errors. Models are never silently substituted by the adapter.

Codex supports `model` and `model_reasoning_effort` per role. Its native subagents
share the session's provider; `model_provider` is deliberately unsupported here
because the checked host version does not apply it as a role override. OpenCode
supports different `provider/model-id` values and an optional `variant` per role.
Provider connections, credentials and model compatibility stay in native host
configuration. No credentials belong in this file.

## Render for inspection

From this repository's root, choose a dedicated output directory **outside the
canonical skill package**. Use separate directories for each host:

```sh
python3 adapters/openspec-development-team/adapter.py render \
  --host codex --models /path/to/team-models.json --output /path/to/team-runtime/codex

python3 adapters/openspec-development-team/adapter.py render \
  --host opencode --models /path/to/team-models.json --output /path/to/team-runtime/opencode
```

Omit `--models` to inherit all model settings. `--skill` can select another local
copy of the complete canonical package. Rendering creates a bootstrap instruction,
native config, Codex role bindings where applicable, and an ownership manifest.
It does not launch models, change Git state, or edit project/global host configs.

The output is generated: edit the model settings or core sources, then rerender.
An edited generated file, unrelated existing file, or symlink causes a refusal
instead of an overwrite. Use a fresh output directory if preserving local changes.
Keep the output directory and canonical checkout available while sessions can
resume. Absolute paths are intentional; rerender after moving either directory.

## Run the team

Start in the assigned repository or worktree and give a concrete authorized task:

```sh
python3 adapters/openspec-development-team/adapter.py run \
  --host codex --models /path/to/team-models.json --output /path/to/team-runtime/codex \
  --project /path/to/assigned-worktree \
  --task "Take the approved export feature through architecture, OpenSpec, implementation, tests, independent review, docs/spec sync and a PR. Leave merge and deployment to me."
```

Use `--host opencode` and its output directory for OpenCode. `run` rerenders the
bindings before invoking the installed CLI and returns its exit status. The
coordinator is the interactive root session, using its configured model; its
native specialist names are `ai-team-<role-id>`. The default endpoint and detailed
workflow come from the shared skill. A narrower task limits the authorized stages.

`--executable /path/to/cli` selects a non-default binary. Explicit native CLI
options can follow `--`, for example `-- --no-alt-screen` for Codex. Native options
can override generated settings; use them deliberately and inspect effective
configuration when troubleshooting. Choose the actual host's native workspace
route when creating isolation; reuse an already assigned worktree. No worktree is
created simply by rendering or launching this adapter.

Codex receives session-scoped `-c` role/model settings and a bootstrap task; the
adapter does not replace root developer instructions or built-in model prompts.
Specialists use their native role developer instructions to read the shared role
file and receive a bounded handoff in a fresh context. Full-history forks can
ignore or reject role/model selection, so the dispatch binding disables that mode.

OpenCode receives a primary coordinator and seven subagents through a process-local
`OPENCODE_CONFIG_CONTENT` overlay, with explicit `--agent` selection. Existing
provider/project config and `OPENCODE_CONFIG` remain in use. Existing inline JSON
is preserved; colliding agent names or inline JSONC are rejected rather than
silently replaced. Reserve `ai-team-*` for this adapter across host config layers.
No default agent is changed for other sessions.

Core prompt changes become available on the next fresh launch without copying
them into adapters. Restart between updates; do not change the shared checkout
under active runs. Model changes require rerendering, which `run` performs.

## Permissions and evidence

The core's role boundaries remain authoritative. OpenCode task permissions allow
the coordinator to dispatch only these specialists and deny specialist delegation.
Code/security reviewers also deny native edits and Bash; supply runner/scanner
evidence through their handoff. Other tool integrations retain their host policy.

Codex's checked role implementation inherits the live session's permissions and
only applies a bounded set of overrides. A role TOML `sandbox_mode` does not
establish an independent reviewer sandbox in that version. Accordingly, the
adapter emits no misleading sandbox/provider/approval overrides. Reviewer scope
and coordinator-only delegation are instructions under the session's host policy.
For enforced per-role permissions, use host-managed restricted execution contexts
or separately sandboxed review sessions. Keep the initial run supervised.

Neither adapter supplies a writer lock, tamper-proof evidence collector or CI
runner. The coordinator uses the project's tools and the core handoff/evidence
contracts. The optional readiness checker still validates supplied evidence only.
Native configuration checks establish discovery and model bindings, not model
availability, correct behavior, test coverage, or an end-to-end pilot pass.

The [OpenSpec and Superpowers notices](../../THIRD_PARTY_NOTICES.md) stay in the
canonical package. Preserve the complete package and those notices when moving
it; do not distribute a binding without its referenced core instructions.
