# Automated testing and bounded correction

## Select tests by changed behavior

Inspect current commands, fixtures, CI, architecture boundaries, and baseline
failures. Reuse the project's runner. Establish a known failing reproduction for
a bug when feasible; explain when the old state cannot be reproduced safely.
Write assertions about observable results and failure behavior, not copies of
the implementation or only mocked internal calls.

| Change | Useful checks |
| --- | --- |
| Pure logic | Unit/boundary tests, invariants or property tests where valuable |
| API or module boundary | Contract/schema tests, authorization and error behavior |
| Database/storage | Integration tests with disposable state, migration and rollback/forward recovery |
| UI or user journey | Focused browser/end-to-end tests, interaction/error/accessibility checks |
| Concurrency or retries | Duplicate delivery, races, timeouts, partial side effects and restart recovery |
| Dependencies/build/CI | Lock integrity, reproducible build, dependency advisories and permission changes |
| Docs/spec-only | Structural/semantic spec validation, links, examples and affected commands |

Start with fast deterministic checks on each slice, then relevant integration
checks and critical user flows. Avoid brittle full-stack tests for behavior a
lower layer proves more reliably. Use representative smoke/end-to-end coverage
for the boundaries that lower-level tests cannot establish.

Coverage is a diagnostic and risk indicator, not proof of correctness. Set
changed-code/branch thresholds only where appropriate to the repo's baseline.
Do not adopt an arbitrary universal percentage or weaken an existing gate in
the same change to hide failures. Consider targeted mutation tests for critical
logic when assertion quality is uncertain and a supported tool exists.

## Test execution and evidence

- Run in a disposable or otherwise approved environment with synthetic/redacted
  fixtures and bounded time/resources. Live credentials and production mutations
  are not required for ordinary checks.
- Prefer reviewed named jobs when the host supplies them. Capture the returned
  job ID and poll/reuse it; do not resubmit an already queued job.
- Record candidate identity, command/job, environment/dependency fingerprint,
  start/end or duration, exit status, counts, and raw evidence reference.
- Separate passed, failed, blocked, skipped/not applicable, and not run. A missing
  runner is a blocked check. Source inspection is not test execution.
- A simulator/stub proves its modeled behavior only. Add actual integration
  evidence for required live-service semantics in a safe authorized environment.
- Check that verification did not change the candidate. Generated outputs belong
  in allowed scratch/artifact locations; changed source invalidates the result.

## Requirement traceability

Give changed requirements/scenarios stable IDs in the evidence mapping without
rewriting the project's naming convention. For each scenario identify test/check
ID, fixture, expected behavior, observed result, and documentation path or a
specific not-applicable reason. Planner supplies the required set from OpenSpec;
QA cannot omit a difficult scenario from the receipt to claim complete coverage.

Every public behavior change should have an observable acceptance path. Purely
editorial changes need proportionate checks, not invented executable tests.
Record any manual acceptance as a named required check with actual evidence.

## Self-correction protocol

1. Classify the failure: product defect, bad test, stale evidence, environment
   blocker, flaky behavior, or changed requirement. Preserve the failing evidence.
2. Group related actionable findings, assign IDs, and state closure criteria.
   Ask the implementer to repair one bounded slice; do not alternate unbounded
   suggestions between agents.
3. For a defect, add a reproducing regression test where meaningful, fix the root
   cause, and rerun affected checks. A broken test needs an independently reviewed
   correction demonstrating that the approved contract remains covered.
4. Refresh the candidate and required evidence. Resume the original independent
   reviewer to check closure and affected behavior. A writer cannot close its
   own finding by assertion.
5. Persist outcome and correction count in the existing OpenSpec evidence area.
   Default to two failed correction rounds for the whole change, not two per
   role. Apply a stricter runtime cap when present. New sessions do not reset it.
6. Stop on repeated unchanged findings/no progress, missing capabilities, changed
   product intent, or budget exhaustion. Return exact context, remaining findings,
   attempts, and the smallest owner decision or environment repair needed.

A suspected flaky test gets at most one diagnostic rerun on unchanged inputs.
Keep both outcomes and investigate. A green rerun alone does not erase the failure.
Quarantine or threshold changes require the project's explicit owner-approved
policy, with scope and expiry; never silently skip the case. Do not retry known
dependency failures until the environment changes.

## Pilot scenarios

Before enabling unattended execution, exercise: a normal small feature, a bug
requiring a regression test, an authorization-sensitive change, a docs-only change,
a missing test prerequisite, a stale review after a code edit, and a failure that
reaches the correction limit. Include spec rename/removal and interrupted sync.
Measure acceptance and human effort; do not call the team reliable from one run.
