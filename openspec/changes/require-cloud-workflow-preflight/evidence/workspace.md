# Workspace and routing record

- Code and planning root: this linked worktree, branch
  `codex/enforce-cloud-skill-startup`, base
  `fb4d662c9fa8e140a59f74755c656eb9b9267bd3`.
- Manual external worktree reuses the session's authorized isolated-checkout
  workflow; no native worktree allocator is exposed. The original checkout is
  preserved. Root owns retention through delivery.
- Baseline: repository validator passed; all 69 standard-library tests passed.
- OpenSpec: existing environment CLI 1.14.3; no previous planning root in this
  repository. Initialized spec-driven artifacts with tools=none for this change.
- Root owns proposal/spec/design/tasks, integration and final evidence. A focused
  implementer will own adapter/template/tests/docs in a serialized writer phase.
- Model profile: Luna medium for the bounded implementation, Sol 6.1 high for
  independent correctness and security review. Fresh-context native spawns must
  explicitly request both model and effort. Runtime model identity telemetry is
  unavailable unless returned by the host; accepted requests are reported as such.
- Security triage: installer filesystem writes, path handling and subprocess
  boundaries require independent security review. No secret, production, billing
  or automatic project migration changes are authorized by this increment.
