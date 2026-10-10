# Portable setup and later runtime integration

## What is ready to use

Copy this complete skill package to the host's supported skill location. Load
`SKILL.md` as the coordinator workflow. Each Markdown file listed in
[team.json](../assets/team.json) contains a copyable system prompt and boundary
examples. The manifest is a role inventory, not an executable scheduler config.

Register the roles using the chosen host's native agent mechanism. Keep provider,
model, credentials, and deployment paths in that host's configuration. Choose
models by tested capability: architecture/planning needs coherent reasoning,
implementation needs code/tool competence, review needs independent evidence
analysis, and the steward needs accurate cross-artifact reconciliation. Different
model families can add useful diversity but are not required and do not prove
independent correctness.

Eight roles may be loaded on demand. Do not reserve eight concurrent processes.
Use one writer per worktree; allow parallel read-only reviews only when the host
and snapshot isolation support them. Only the coordinator dispatches. If the host
does not support those boundaries, use the prompts manually and mark automation
and independent review uncommissioned.

## Capability mapping

| Role | Minimal capabilities | Writes | Explicit exclusions |
| --- | --- | --- | --- |
| Coordinator | Context, dispatch, status, approved Git/PR delivery | Evidence; requested delivery | Granting new authority or approving its own review |
| Architect | Read source/docs and approved reference lookup | Design/decision docs | Application implementation or deployment |
| Planner | Repository-pinned OpenSpec workflows | Assigned planning artifacts | Product code and silent intent changes |
| Implementer | Source editing and approved test execution | Assigned code/tests/docs | Review approval, policy weakening, live operations |
| Test engineer | Test tooling, sandbox jobs and evidence | Tests/fixtures in authoring phase | Product fixes and retry-until-green behavior |
| Code reviewer | Read candidate and verification evidence | Review result only | Source edits or authorship of reviewed implementation/tests |
| Security reviewer | Read reachable paths and approved scanner evidence | Security result only | Live exploitation, secrets retrieval, self-waived findings |
| Documentation/spec steward | Documentation and selected sync workflow | Docs and authorized spec branch | Product behavior and unauthorized archive |

These desired scopes must be enforced by the host; Markdown alone cannot impose
permissions. Existing tool/skill allowlists, prepared environments, runtime budgets,
and registration requirements continue to apply.

## Reuse an existing development platform

Map current planner, implementer, QA, reviewer, architect and orchestrator roles
before introducing duplicates. Add missing security and documentation ownership
as narrow roles or bounded invocations. Preserve the platform's established state
machine, claim protocol, recovery counters, and branch/merge rules. Use its isolated
test runner, dependency scanner, architecture/reference checker, and spec validation
when they exist. A tool mentioned in a repository is not proof it is installed or
commissioned; verify availability during adoption.

Record per-host registration, permission mappings, exact commands, check policy,
and candidate/evidence adapters in the target private project when appropriate.
This public package deliberately contains no organization-specific infrastructure,
repository snapshots, or private configuration.

## Suggested pilot sequence

| Phase | Work | Exit evidence |
| --- | --- | --- |
| First setup | Map roles to host, register prompts, confirm tools and permissions | Actual discovery and denied-action checks |
| First plan | Choose one small change and produce architecture/OpenSpec/test plan | Owner-approved scope and coherent artifacts |
| First implementation | Run bounded implementation and tests | Actual reproducible results on the candidate |
| Review loop | Exercise independent review and one seeded defect | Defect detected, corrected, and verified within limits |
| Coherence/delivery | Verify docs, sync, final candidate checks and requested delivery | Matching artifacts and no stale evidence |
| Measure | Assess quality, human time, correction count and costs | Decision to continue, simplify, or stop |

This can fit a seven-day pilot when prerequisites and setup hours permit; calendar
dates never waive gates. Time/cost estimates require actual volume, host/model
usage and review effort. Track net time saved after review, rework, and maintenance;
do not promise savings before measurement.

Next automation after a stable pilot: recurring dependency or maintenance changes
using the same checks and constrained authority. Keep the first deployment small.

## Common mistakes

1. Registering roles without tool restrictions: verify the host's actual scopes.
2. Creating a second task database: keep OpenSpec tasks and existing runtime state.
3. Accepting stale green checks: bind receipts to the delivered content.
4. Letting correction loops redefine success: preserve scenarios and bound attempts.
5. Archiving before docs/spec convergence: verify sync and acceptance first.

## START HERE FIRST

Select one small development change and fill the intake and architecture templates;
record the target host as unconfigured until role registration is actually verified.
