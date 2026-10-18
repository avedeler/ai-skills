# Codex adapter for OpenSpec Model Router

The [portable skill](../../skills/openspec-model-router/SKILL.md) decides when and
how to delegate. This optional adapter supplies the requested [model profile](model-profile.md),
[live runtime mapping](runtime.md), and [research and calibration](research.md).
It does not duplicate the core workflow or replace the existing development team's
roles, independent review, correction limits, or worktree controls.

## Install once in a cloud environment

From a reviewed checkout of this repository, run:

```sh
python3 adapters/openspec-model-router/install.py
```

This copies the canonical package into
`~/.agents/skills/openspec-model-router` and adds the three optional profile
references. The core loads the profile when installed. The installer uses only
Python's standard library, performs no network calls, leaves identical installs
unchanged, and refuses to overwrite a differing installation. Back up and merge
an older installation deliberately before updating. For a staging destination:

```sh
python3 adapters/openspec-model-router/install.py --skills-dir /tmp/router-skills
```

For persistent Codex Cloud use, run this during the environment setup workflow,
then publish or republish that environment. A copy in a running task's filesystem
does not change the starting point for future tasks. Verify discovery in a fresh
task. Account-wide plugin installation and environment publishing are not performed
by this installer. See [cloud environment documentation](https://learn.chatgpt.com/docs/environments/cloud-environments).

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
