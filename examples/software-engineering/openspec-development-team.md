# Development team blueprint

This is a portable team design and implementation package. The role prompts and
readiness-checker code and [native host adapters](../../adapters/openspec-development-team/README.md)
exist; no agent runtime has been deployed or model-assisted pilot run.
All sample evidence is synthetic. No business savings or model performance has
been measured.

## 1. First workflow and architecture

Use one development change as the unit of work:

**Idea → high-level architecture → OpenSpec plan and test design → implementation
→ automated verification → independent code review → applicable security review
→ documentation/spec coherence → final checks → review-ready delivery.**

Self-correction returns confirmed findings to implementation with a reproducing
test and a bounded retest/review cycle. Merge/deployment follow existing owner
authority. Archive waits for the actual completion gate and verified spec sync.

Keep OpenSpec as the planning/task source and the existing host as the scheduler.
Do not introduce a second queue, autonomous merge controller, or new cloud service
for the first pilot. See the [full lifecycle](../../skills/openspec-development-team/references/lifecycle.md).

## 2. Dedicated roles

| Role | Responsibility | Why separate |
| --- | --- | --- |
| Coordinator | Scope, assignments, evidence, correction budget and delivery | One owner for transitions and a complete handoff |
| Architect | Idea, current-system analysis, high-level design and decisions | Preserve intent before implementation details |
| OpenSpec planner | Proposal, scenarios, design and actionable tasks | Keep the artifact graph and acceptance criteria coherent |
| Implementer | Bounded source change, regression fixes and inline docs | One product-code writer |
| Test engineer / QA | Test design/fixtures, then independent execution | Check behavior beyond the writer's assumptions |
| Code reviewer | Defects, test quality, conformance and delivery claims | Independent of implementation/test authors |
| Security reviewer | Risk-triggered semantic security review | Focused trust-boundary analysis when applicable |
| Documentation/spec steward | Docs, architecture and canonical-spec coherence | Explicit ownership of drift prevention |

These are eight on-demand roles, not eight concurrent workers. Each has different
inputs or authority; no lead is added beyond the coordinator. A small docs change
uses a shorter path. One writer at a time avoids conflicting changes.

The coordinator establishes workspace ownership before repository writes. Roles
share the change's worktree across serialized authoring phases; read-only reviews
use a frozen candidate. Native workspace tools take priority, and a separate
planning store gets its own branch/ownership mapping. Baseline evidence and later
candidate checks stay distinct. See [worktree integration](../../skills/openspec-development-team/references/worktrees.md)
and [the attributed upstream skill](../../skills/openspec-development-team/third_party/using-git-worktrees/README.md).

## 3. Prompts and reusable assignments

[The role manifest](../../skills/openspec-development-team/assets/team.json) lists
eight bundled prompts, each under 300 words in its system-prompt section. Use
[the handoff template](../../skills/openspec-development-team/assets/handoff.md)
for assignments and returned evidence. Model choice is an external capability
decision; the package names no required model or AI vendor.

## 4. Contracts and failure handling

The candidate identity covers source, tests, config, spec/doc revisions, and
substantive delivery claims. All required results name that identity. Handoffs
carry exact scope, prerequisites, criteria, evidence location, and remaining budget.
No role can grant itself new tools, replace the user's intent, or self-approve a
consequential action.

| Role | Three likely failure modes | Detection and response |
| --- | --- | --- |
| Coordinator | Lost scope, stale receipts, unbounded loops | Check assignment scope and candidate IDs; persist counters; stop/escalate |
| Architect | Invented current state, excess complexity, ambiguous outcome | Require source evidence, alternatives and measurable acceptance |
| Planner | Missing artifact dependency, wrong planning root, weak scenarios | Discover schema/roots, validate and review requirement coverage |
| Implementer | Regression, test weakening, unrecorded design change | Reproduce/test, review diffs, route intent changes to planner/owner |
| Test engineer | Mock-only confidence, flaky pass, missing prerequisite | Verify boundaries, preserve reruns, mark blocked and continue independent checks |
| Code reviewer | Summary-only approval, stale scope, endless style churn | Read raw diff/results, bind candidate, prioritize material findings |
| Security reviewer | Missed reachability, scanner-only verdict, false waiver | Trace actual boundaries, independent review, owner-governed exceptions |
| Steward | Stale docs, overwritten unrelated specs, legitimized bug | Semantic comparison, scoped/idempotent sync, preserve approved intent |

## 5. Tool stack and setup

Reuse the target repository's OpenSpec wrapper/workflows, test runners, CI,
architecture/reference checks, approved sandbox, dependency/static scanners,
and review/reporting tools. Add a browser runner only when user flows need it.
Use manual evidence collection until a host adapter exists; do not pretend the
readiness checker collects results itself.

Host setup consists of role registration, least-privilege capability mapping,
candidate/receipt collection, reviewed check policy, and actual pilot tests.
[Setup guidance](../../skills/openspec-development-team/references/setup.md)
includes the capability matrix. Current price, available models and runner cost
are unknown until measured in the chosen environment.

## 6. Test plan and review gates

Tests are driven by requirements and risk: fast unit/boundary checks, integration
and contract tests at changed interfaces, regression tests for fixes, and focused
end-to-end checks for critical flows. Coverage supports judgment; it is not a
substitute for meaningful assertions.

Exercise at least these pilot cases: normal feature, regression repair,
authorization-sensitive change, docs-only update, missing prerequisite, stale
candidate, exhausted correction loop, and spec-sync interruption. Expected outcomes
are in the [behavioral scenarios](../../evals/openspec-development-team.json);
they are proposed evaluations, not executed model tests.

The bundled readiness checker has automated regression tests for missing/stale
evidence, incomplete scenarios, independent review, security applicability, spec
sync, and correction limits. It checks supplied packet consistency only; actual
host enforcement and agent behavior remain unverified.

## 7. Pilot plan

Days 1–2, if available: choose one small change, map roles, prepare access, architecture,
OpenSpec artifacts and test plan. Days 3–4: implement and run checks in a sandbox.
Days 5–6: exercise review/correction, docs/spec sync and requested delivery with
human supervision. Day 7: inspect quality, human effort, cost and blockers.

If the runtime is not configured, begin with the portable documents and setup
checklist. Dates move when prerequisites fail; evidence gates remain in place.

## 8. Economics and scorecard

Savings are unknown. Measure same-scope manual development/review effort against
remaining planning, supervision, review, rework and maintenance effort. Count
all model sessions, failed attempts, runner time and subscriptions. A faster
implementation that increases review or escaped defects may be a loss.

Track accepted changes, net human hours saved, time to review-ready, escaped
defects, errors caught, failed correction rounds, flaky tests, spec/doc drift,
and cost per accepted change. Investigate the failing stage instead of adding
agents automatically.

## 9. Next workflow

After a stable feature/bug-fix pilot, reuse the same contracts for small maintenance
or dependency updates. Automatic merge/deployment is a separate capability and
requires its own evidence and authority.

## 10. Mistakes to prevent

1. Treating prompts as permissions: verify host enforcement.
2. Treating green checks as conformance: map scenarios to observable results.
3. Self-reviewing the implementation: preserve separate reviewer contexts.
4. Repairing forever or lowering the bar: stop at the correction cap.
5. Archiving stale specs: finish semantic sync and verify the result first.

## Design review

Ready as a portable package for runtime integration. It provides roles, contracts,
templates and tested evidence-consistency code. Independent live-agent behavior,
host registration, permission enforcement, actual test adapters and economics
still need a supervised pilot; this is not a claim of production readiness.

## START HERE FIRST

Pick one small feature or bug fix and fill the
[intake](../../skills/openspec-development-team/assets/intake.md) and
[architecture](../../skills/openspec-development-team/assets/architecture.md)
templates before choosing the runtime implementation.
