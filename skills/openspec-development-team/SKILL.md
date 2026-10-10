---
name: openspec-development-team
description: Coordinate dedicated development agents from idea and high-level architecture through OpenSpec planning, implementation, automated tests, code review, risk-based security review, and documentation/spec synchronization. Use to run or configure a development team with bounded correction and evidence-backed delivery. Do not treat installing this skill as deploying a runtime or granting merge or production authority.
---

# OpenSpec Development Team

Turn an idea into reviewed, tested, documented code using the repository's existing
OpenSpec workflow. Use the eight [role definitions](assets/team.json) as bounded
assignments. They are portable system prompts, not host-specific agent registrations.
Only the coordinator dispatches work; specialists do not create more specialists.
Use the host's existing scheduler and permission controls. If delegation is absent,
produce the artifacts sequentially and report that independent review remains
unperformed; do not impersonate separate agents or invent their receipts.

Read [the lifecycle](references/lifecycle.md),
[testing and correction](references/testing-and-correction.md), and
[documentation and security gates](references/documentation-and-security.md).
Use [the setup guide](references/setup.md) to install roles or map an existing team.

## 1. Establish context and authority

Read repository instructions, current architecture, OpenSpec config and generated
workflows, test/CI definitions, local skills, approved execution helpers, and the
relevant code. Record what exists versus what is merely proposed. Prefer installed
QA, review, architecture, browser, scanning, and documentation tools over new ones.
Do not copy private repository details into a public package or report.

Reuse the user's idea, constraints, acceptance criteria, and authorization. Ask
only for material omissions. Start a brief with [the intake template](assets/intake.md).
Identify the target code repository, planning root/store, owner, selected branch
or worktree, requested endpoint, available capabilities, and per-task budget.
The default endpoint is a review-ready change; merge, deployment, and archive
follow their own established authority. Preserve scoped authority already given.

Use a repository-pinned OpenSpec wrapper when present. Discover the installed CLI
version, active schema, artifact graph, roots, and available workflow skills;
never assume every repository has the same generated commands. Do not install
dependencies or access secrets merely because a skill mentions them.

## 2. Idea → high-level architecture

Assign the [architect](assets/agents/architect.md) to clarify the problem, examine
the current system, compare the smallest viable options, and write
[the architecture brief](assets/architecture.md). Separate current architecture
from the proposed design. Include system boundaries, data flow, interfaces,
constraints, risks, non-goals, alternatives, and measurable acceptance criteria.
Record decisions and the user's existing approval scope before implementation.
Material changes in product intent return to the user; routine design refinements
within that scope do not require repeated permission.

## 3. Architecture → OpenSpec plan and test design

Assign the [planner](assets/agents/planner.md) to translate the architecture into
the active OpenSpec schema's artifacts. Reuse the governing change when one exists.
Read runtime-provided artifact instructions and dependency order. The usual
proposal/spec-deltas/design/tasks layout is an example, not a hard-coded contract.
Keep OpenSpec tasks as the only task backlog.

Bring in the [test engineer](assets/agents/test-engineer.md) before coding to turn
requirements and scenarios into [a test plan](assets/test-plan.md). Map every
changed behavior to an observable test or an explicit acceptance check. Include
failure, boundary, regression, integration, and relevant security scenarios.
Run structural spec validation; it does not prove semantic correctness.

Choose a reviewed check policy using [policy.example.json](assets/policy.example.json).
Required checks and scenarios are controlled inputs; an agent must not remove a
failing gate or weaken a test to manufacture success. Record justified exceptions
through the existing project policy, with owner and expiry where appropriate.

## 4. Implement and verify in bounded slices

Assign the [implementer](assets/agents/implementer.md) one coherent task slice.
Allow one writer per branch/worktree at a time. The test engineer may author tests
in a separate, serialized test-writing phase; the code reviewer checks those tests
as well. Use a fresh verification context after implementation. Run code only in
the authorized execution environment; prefer approved named verification jobs.

Implement behavior, regression tests, and explanatory documentation together.
Useful comments explain invariants, tradeoffs, or surprising behavior; avoid
line-by-line narration. Do not tick tasks complete until their criteria are met.
Preserve scope and existing work. Pass prerequisite failures between roles so
every worker does not retry the same unavailable dependency.

Capture the exact candidate identity: source/config/tests, spec and documentation
revisions, and substantive delivery claims. HEAD alone is insufficient for dirty
work or a separate spec store. Freeze that candidate during verification/review.
Bind all test and review receipts to it. A content change invalidates affected
evidence; a mechanical receipt append does not require an endless review loop.

## 5. Review, then correct

After functional verification, assign the [code reviewer](assets/agents/code-reviewer.md)
a fresh context with the approved requirements, implementation, tests, and raw
evidence. It must not be the implementation session. Require concrete findings
with location, impact, reproduction or reasoning, and an acceptance criterion.

Always triage security impact. Invoke the dedicated
[security reviewer](assets/agents/security-reviewer.md) for authorization,
sensitive data, untrusted inputs, dependencies, network/filesystem boundaries,
cryptography, migrations with sensitive data, infrastructure, or CI permissions.
Unknown impact is unresolved, not an exemption. A low-risk skip needs a recorded
reason tied to the candidate. The role examines reachability and semantics;
scanner output alone is not a security review.

Group actionable findings into one correction packet. The implementer fixes
within approved scope; the test engineer adds a reproduction/regression test
where meaningful; the original independent reviewer verifies closure. Use at
most two failed correction rounds by default, or the project's stricter limit.
Stop earlier for no progress, changed intent, exhausted cost/time, or an unavailable
required capability. Persist findings and counters in the existing change's
evidence area. Do not create a competing scheduler state file.

## 6. Documentation and spec coherence

Assign the [documentation/spec steward](assets/agents/documentation-steward.md)
to compare intent, implementation, tests, change artifacts, canonical specs,
architecture, API/CLI docs, setup instructions, and operational runbooks.
It may edit documentation and approved spec artifacts, not product behavior.
If behavior and intent disagree, return the decision to planner/architect; never
rewrite requirements merely to excuse a defect.

Synchronize approved delta specs in the selected planning root on the authorized
change branch or separately controlled spec-store branch. Use the installed sync
workflow; preserve unrelated requirements and nested capability paths. Validate,
compare every selected delta against its canonical result, and verify a second
comparison leaves no pending changes. Resolve omissions before delivery.

Final review includes documentation and substantive evidence/PR claims. Archive
only after the requested completion point, verified synchronization, and any
required merge acceptance. Run sync to completion before archive; never race them.
Keep implemented, merged, deployed, and archived statuses distinct.

## 7. Deliver and measure

Use [the handoff template](assets/handoff.md) and
[review report](assets/review-report.md). The optional bundled
[readiness checker](scripts/check_readiness.py) validates the structure, freshness,
and consistency of a supplied evidence packet. It does not run tests, authenticate
receipts, enforce permissions, or authorize a merge. The host must supply trusted
policy, candidate identities, and actual evidence. See [its contract](references/evidence-contract.md).

Deliver the requested branch/PR with tests and findings, security disposition,
documentation/spec changes, remaining limitations, and one next action. Inspect
published checks for the actual delivered head. Report pending/missing checks
honestly. Preserve all unresolved blockers and rejected scope expansions.

Measure accepted changes, elapsed cycle time, human review/rework time, escaped
defects, correction rounds, flaky-test rate, spec drift, and cost per accepted
change. Start with one small feature or bug fix. Expand only after a representative
pilot demonstrates useful quality and manageable review overhead.
