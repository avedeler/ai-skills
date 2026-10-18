---
name: openspec-model-router
description: Route OpenSpec development work to scoped subagents by difficulty, model, and reasoning effort. Use when asked to orchestrate agents or apply this routing policy.
---

# OpenSpec model router

Act as the accountable orchestrator. Use a capable planning model for the root session. If an optional `references/model-profile.md` is installed or a profile is supplied by the user, read it to map capability tiers to available models and efforts. Without a profile, choose from verified host capabilities and disclose the selection. This skill explicitly requests scoped subagent delegation when useful; it does not require delegation for every task. Keep working through integration and verification within the user's authorized scope.

## Start

1. Read applicable AGENTS.md instructions and inspect current changes before assigning ownership. Preserve existing work.
2. Identify the user's intended phase: explore, propose/design, apply, verify, or archive. Follow the installed OpenSpec skills and resolved schema; read [OpenSpec coordination](references/openspec.md) for OpenSpec work.
3. Inspect the actual spawn tool, allowed models, effort values, limits, and workspace sharing. Use the live tool schema and any supplied optional host adapter before the first spawn. Never assume a skill changes the root model or enables missing tools.
4. Form a small dependency graph. For each substantial scope record task ID, outcome, dependencies, owner/files, model/effort, and acceptance check. Keep this in the working plan; use a persistent handoff file only for long-running work.

## Route by uncertainty and consequence

| Scope | Required capability | Reasoning depth |
| --- | --- | --- |
| Root orchestration and integration | Strong planning, coordination, evidence synthesis | High |
| Architecture decisions | Strongest available reasoning for system invariants and tradeoffs | High |
| Proposal, specs, design, task decomposition | Strong requirements and design reasoning | High |
| Clear code or apply task | Efficient focused implementation with decisive checks | Medium |
| Ambiguous code or apply task | Strong multi-step implementation | Medium, high for intricate debugging |
| Exploration and source extraction | Efficient bounded retrieval with evidence | Medium |
| Deep research | Strong conflicting-source synthesis and uncertainty analysis | High |
| Mechanical documentation and checks | Efficient bounded execution | Proportionate |
| Independent review | Strong correctness and risk analysis | High |

A task is straightforward only when requirements, pattern, ownership, and acceptance
checks are clear and mistakes are locally reversible. A small diff can still be
difficult. Resolve ambiguous requirements before assigning a focused implementer.
Route actual architectural uncertainty to the strongest reasoning capability;
routine design documentation does not require it merely because its filename is
`design.md`. Reasoning levels are preferences, not comparable compute budgets across
models. Verify support and tune on representative tasks, not model names alone.

This skill selects execution resources; it does not replace the project's development
lifecycle. When used with a dedicated development-team skill, preserve its role
independence, workspace ownership, correction limits, and acceptance gates. Never
reset a correction budget by switching model or agent.

## Delegate economically

- Do tiny tasks directly when the handoff and review would cost more than completion. Avoid spawning another coordinator merely to repeat the root's work.
- Start with at most two independent children; expand only for distinct useful scopes, within the runtime limit. Default to one delegation level. Children return to the root instead of recursively spawning.
- Give each writer exclusive paths. Serialize overlapping files, shared schemas, lockfiles, generated files, OpenSpec task tracking, and integration. Shared filesystem changes are visible immediately; a branch name does not isolate a worktree.
- Prefer fresh context with a compact brief over copying conversation history. Include relevant user constraints, applicable instruction paths, exact OpenSpec artifacts/tasks, interfaces, known findings, allowed files, tests, and completion criteria. Do not omit governing constraints to save tokens.
- Use the [assignment template](references/assignment.md). Normally ask for a short result with evidence; let research be as long as needed to support its recommendation. Agents must flag unknowns and blockers rather than fill them with guesses.
- Reuse an agent for follow-up within its scope. A follow-up does not change its model; to escalate, stop overlapping work and spawn a new agent with a compact evidence handoff.
- When blocked by missing credentials, tools, or data, fix or report that dependency; a bigger model cannot supply it. For reasoning failures, allow one targeted correction with new evidence, then escalate focused implementation → strong multi-step reasoning → strongest architecture reasoning for unresolved architectural issues. Do not loop on identical attempts.
- Treat response lengths as guidance unless the runtime provides enforceable limits. Track actual tokens/cost only when telemetry exists; otherwise label them unavailable. Never claim savings from model names alone.

## Integrate and finish

Review each returned diff and evidence against the task and spec. Resolve conflicts centrally, run the relevant integration checks, and distinguish pre-existing failures from regressions. A child reporting success is not proof. Do not mark an OpenSpec task complete until its acceptance conditions are satisfied; the root owns checkbox updates.

Report the completed result, validation, outstanding limitations, and any material routing substitutions. Continue authorized fixes without repeated approval prompts. Follow existing approval boundaries for actions such as deployment; this skill adds none.
