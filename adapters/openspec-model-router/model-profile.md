# Codex model profile

Optional settings for the portable openspec-model-router skill. Read the installed
core SKILL.md for workflow decisions; this profile supplies model selection only.
Use the live host schema and [runtime adapter](runtime.md) before spawning.

| Scope | Default model | Effort | Boundary |
| --- | --- | --- | --- |
| Root orchestration and final integration | gpt-6.1-sol | high | Own decisions, dependencies, verification, final answer |
| Architecture decision | gpt-6-astra | high | Service boundaries, invariants, consistency, trust boundaries, migration strategy |
| OpenSpec proposal, specs, design, task decomposition | gpt-6.1-sol | high | Turn intent and architecture decisions into implementable artifacts |
| Straightforward code or OpenSpec apply task | gpt-6-luna | medium | Clear behavior, established pattern, bounded ownership, decisive check |
| Ambiguous code or OpenSpec apply task | gpt-6.1-sol | medium | Incomplete local understanding, interacting components, unfamiliar code |
| Complex debugging or implementation | gpt-6.1-sol | high | Subtle state/concurrency, elusive regressions, significant edge cases |
| Exploration, search, source extraction | gpt-6-luna | medium | Read-only, concrete questions, paths or citations required |
| Deep research and evidence synthesis | gpt-6.1-sol | high | Reconcile sources, uncertainty, competing explanations, recommendation |
| Bounded checks and mechanical documentation | gpt-6-luna | medium | Report actual observations; no speculative certification |
| Risk-based independent review | gpt-6.1-sol | high | Behavior, integration, security-sensitive changes, missing scenarios |


Preserve these requested defaults. Consider Luna low for trivial extraction,
Luna high for difficult bounded tracing, and Astra low for constrained architecture
comparisons only after evaluation. Do not silently replace Sol 6.1 with older Sol.
The root should be selected as Sol 6.1 high through supported session controls;
this profile cannot switch the running root. See [research](research.md) for
sources, illustrative API prices, and calibration limits. No live benchmark was run.
