# Runtime adapters

The live tool schema and governing instructions override examples here. Model availability is account- and runtime-specific. A CLI installation alone does not prove the hosted session loads CLI configuration.

## Native collaboration tools (preferred)

If `collaboration.spawn_agent` exposes `model` and `reasoning_effort`, pass both explicitly. In runtimes where full-history forks inherit settings and forbid overrides, use `fork_turns: "none"`. This skill explicitly requests the model overrides in its routing table. A fresh-context child needs a self-contained assignment and instruction paths.

Example for that exact tool shape (replace the message with a real brief):

```json
{
  "task_name": "map_auth",
  "fork_turns": "none",
  "model": "gpt-6-luna",
  "reasoning_effort": "medium",
  "message": "Read applicable AGENTS.md. Read-only: locate authentication entry points and tests for change add-session-expiry. Scope src/auth and tests/auth. Return paths, symbols, evidence, and unknowns. Do not edit or spawn children."
}
```

Call collaboration tools directly when the runtime requires it; do not assume they are callable through shell or JavaScript orchestration tools. Capture the returned agent ID, track it in the plan, use the provided message/follow-up tools, and collect every assigned result. Prefer available close/release tools for completed agents; if unavailable, reuse idle agents only for compatible scopes. Never assume interrupting frees a slot. Respect active and total thread limits.

Do not claim a model ran unless the spawn was accepted; report effective settings if exposed. If tools inherit the parent model without an override, say that routing is unavailable and perform the work with the available model. Do not fabricate model switching by writing a role prompt.

## CLI/custom-agent support (optional)

Only use this if the running client documents and loads standalone `.codex/agents/*.toml` files. Current official documentation supports this form:

```toml
name = "openspec_explorer"
description = "Gather bounded code evidence for OpenSpec work."
model = "gpt-6-luna"
model_reasoning_effort = "medium"
developer_instructions = """
Read applicable AGENTS.md. Work only on the parent's assigned scope.
Stay read-only. Return paths, symbols, evidence, and unknowns.
Do not spawn children. Do not change OpenSpec artifacts or task checkboxes.
"""
```

Create other roles using the routing table only if reusable named agents help. A custom agent file can override explicit spawn model settings, so inspect it before relying on an override. Do not overwrite existing config or install a complete global config for this skill. The root's model/effort must be selected through its supported UI or session configuration; this skill cannot switch a running root.

## Missing capability

- Preferred model absent: for Luna work, use available Sol medium or the current parent; for Astra work, use Sol high with an explicit limitation and stronger evidence checks. For unavailable Sol, use Astra if available and appropriate; never silently give high-risk ambiguous work to Luna.
- Effort unsupported: choose the closest supported level suitable for the task and disclose the change. If no adequate model is available, do independent safe work and report the affected scope blocked.
- No spawn tool: execute sequentially as the current model, preserving the scope and verification plan. State that no subagents ran. Do not launch nested `codex exec` processes or direct API clients merely to bypass unavailable delegation, authentication, or policy.
- No OpenSpec CLI: follow existing artifacts/generated skills when sufficient, record CLI validation as unavailable, and do not invent successful status output. Use repository installation instructions if setup is authorized and practical.
