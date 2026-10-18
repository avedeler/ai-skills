# Codex adapter for OpenSpec Model Router

The [portable skill](../../skills/openspec-model-router/SKILL.md) decides when and
how to delegate. This optional adapter supplies the requested [model profile](model-profile.md),
[live runtime mapping](runtime.md), and [research and calibration](research.md).
It does not duplicate the core workflow or replace the existing development team's
roles, independent review, correction limits, or worktree controls.

## Install in a cloud environment

From a reviewed checkout pinned to the accepted source commit, use its absolute
path in the environment setup configuration:

```sh
python3 /path/to/pinned/ai-skills-environment/adapters/openspec-model-router/install.py
```

This copies the canonical package into
`~/.agents/skills/openspec-model-router` and adds the three optional profile
references. The core loads the profile when installed. The installer uses only
Python's standard library, performs no network calls, leaves identical installs
unchanged, and refuses to overwrite a differing installation. Back up and merge
an older installation deliberately before updating. For a staging destination:

```sh
python3 /path/to/pinned/ai-skills-environment/adapters/openspec-model-router/install.py --skills-dir /tmp/router-skills
```

For persistent Codex Cloud use, run this during the environment setup workflow,
then publish or republish that environment. A copy in a running task's filesystem
does not change the starting point for future tasks. Verify discovery in a fresh
task. Account-wide plugin installation and environment publishing are not performed
by this installer. See [cloud environment documentation](https://learn.chatgpt.com/docs/environments/cloud-environments).

For a complete startup setup, use the absolute `cloud.py` path from that same
pinned checkout. It
installs or verifies both reviewed skill packages, adds one managed block to the
workspace `AGENTS.md`, and checks the selected OpenSpec version before writing:

```sh
python3 /path/to/pinned/ai-skills-environment/adapters/openspec-model-router/cloud.py install \
  --workspace "$PWD" --skills-dir "$HOME/.agents/skills" \
  --openspec-command openspec --openspec-version 1.14.3
python3 /path/to/pinned/ai-skills-environment/adapters/openspec-model-router/cloud.py verify \
  --workspace "$PWD" --skills-dir "$HOME/.agents/skills" \
  --openspec-command openspec --openspec-version 1.14.3
python3 /path/to/pinned/ai-skills-environment/adapters/openspec-model-router/cloud.py preflight \
  --workspace "$PWD" --skills-dir "$HOME/.agents/skills" \
  --openspec-command openspec --openspec-version 1.14.3 \
  --project-openspec-command /path/to/selected/project/openspec \
  --project-openspec-version PROJECT_OPENSPEC_VERSION \
  --project /path/to/selected/project --phase apply --change CHANGE_ID
```

Use the source revision chosen by the environment owner in its setup configuration;
the adapter itself does not fetch or select source revisions. Install and verify
must run during the environment setup workflow, then the owner must publish or
republish the environment. A fresh task must confirm the startup block and both
skill packages are discovered before relying on them. For exploration, pass
`--phase explore` and omit `--change`; preflight checks context only. Apply mode
checks context, status, and ready apply instructions in the selected project cwd.
When a project uses its environment-wide OpenSpec executable/version, omit the
project-specific flags; preflight reuses the exact verified environment executable.
Otherwise set both flags to the project's wrapper and expected version. Relative
wrapper paths resolve against the project. An explicit bare wrapper name selects
a same-name project entry when present, otherwise searches PATH; it does not
search the caller's directory independently of PATH.
Load the model router and its profile/runtime before every
delegation, including read-only analysis. For software changes, load the
development-team skill and discover the selected project's OpenSpec workflow
before code changes. Generic noncoding or read-only analysis does not require an
OpenSpec change or apply preflight; trivial documentation can follow a
repository-defined exception.
All project checks are read-only; unsupported older CLI commands are reported as
a compatibility failure. No project is initialized or migrated.

Record task routing with the requested model and effort, task scope, and host
response showing the accepted settings. The profile requests explicit supported
model and effort values and fresh-context delegation when required by the host.
These instructions cannot force a tool call, change the active root model, or
prove actual model identity from a request alone. A local installation does not
publish an environment, and a running task does not prove future-session
persistence.

Select Sol 6.1 high through supported session controls, then invoke:

```text
$openspec-model-router Apply the existing OpenSpec change <change-id>.
Use scoped subagents where useful and complete integration and verification.
```

No nested CLI, API credentials, or global configuration rewrite is required.
Model overrides require actual host support; otherwise the skill reports the
limitation and continues sequentially where feasible.

## Validation limits

The adapter was authored against the live collaboration tool contract and
Codex CLI 0.159.2 documentation context. Static packaging checks are not proof
that a hosted session supports all controls. The [evaluation scenarios](../../evals/openspec-model-router.json)
are test specifications; no model benchmark or hosted end-to-end pilot has run.
