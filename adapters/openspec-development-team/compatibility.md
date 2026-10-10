# Native contracts and verification

The adapters use a small subset of native configuration. No upstream runtime
implementation or documentation is copied into their generated bindings.

| Host | Contract used | Source checked |
| --- | --- | --- |
| Codex CLI 0.159.2 | `agents.<name>.description/config_file`, `agents.enabled`, `model`, `model_reasoning_effort`, role `developer_instructions`, CLI `-c` and `--cd` | [Versioned config schema](https://github.com/openai/codex/blob/rust-v0.159.2/codex-rs/core/config.schema.json) |
| Codex role application | Model/reasoning/instructions overrides; live parent permissions and provider are retained | [Role override implementation](https://github.com/openai/codex/blob/rust-v0.159.2/codex-rs/core/src/agent/role.rs) and [child configuration](https://github.com/openai/codex/blob/rust-v0.159.2/codex-rs/core/src/agent/child_config.rs) |
| OpenCode 1.18.35 | `agent`, primary/subagent `mode`, per-agent `model`/`variant`, `{file:...}` prompts, `permission.task/edit/bash`, inline config and `--agent` | [Agent documentation](https://opencode.ai/docs/agents/) and [configuration documentation](https://opencode.ai/docs/config/) |

OpenCode documentation was inspected at source revision
`7b3d4ce3a7dbd2a6d3637722a0d5f22a7d086937`; native loading is checked against the
released binary, since documentation and development branches can move ahead.
These are verified versions, not a promise that every older or later build works.

Repository tests exercise independent models for all roles, inheritance, native
configuration serialization, shared prompt references, configuration preservation,
literal argument passing, and refusal to overwrite edited files. They run without
model calls or CLI installations.

Native checks performed during implementation:

- Codex 0.159.2 loaded the generated coordinator settings and seven registered
  role paths through its configuration loader (`features list`). Per-role model
  files were parsed in repository tests and checked against the versioned role
  implementation. No subagent inference was invoked.
- OpenCode 1.18.35 loaded the generated overlay through `--pure debug config` in
  a temporary project with isolated configuration/data directories. All eight
  distinct synthetic model IDs and variants survived loading, and all role files
  expanded into the native prompts. These synthetic IDs test configuration
  transport; they are not claims that those models exist or can execute tasks.

For adoption, verify native agent discovery and effective model settings, then run
one small authorized change with a seeded defect through review, correction and
spec/doc synchronization. Record the actual model used by each specialist and
the session's real permission/workspace behavior. A configuration load is not a
model-assisted pilot. The adapter does not silently fall back to sequential
impersonation when native delegation or a configured model is unavailable.
