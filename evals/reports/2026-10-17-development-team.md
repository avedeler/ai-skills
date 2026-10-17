# Bounded hosted development-team pilot — 2026-10-17

One real hosted role loop implemented a synthetic batch-counting function,
detected a deliberately injected boundary defect, corrected it in one round,
and independently verified code and documentation. The final candidate passed
11 unit tests, 138 independent oracle cases, and six executable examples.
This is observed local behavior, not a complete native OpenSpec/CLI-adapter pilot
or evidence of general model reliability.

No defect in the reusable skill, adapter, installer, or readiness checker was
demonstrated. Those implementations and pipeline gates are unchanged. The
correction was confined to the disposable fixture. This change retains sanitized
evidence and replay inputs; it does not justify an unrelated runtime fix.

| Context | Recorded fact |
| --- | --- |
| Skill and repository base | `fb280abfd9d49dad4a4801e063442616ba641e25` |
| Freshness check | Current main matched the audited SHA; no open issues/PRs or newer evaluation artifacts were found before the run. |
| Existing main CI | [38148530625](https://github.com/avedeler/ai-skills/actions/runs/38148530625), successful; static evidence only |
| Execution host | ChatGPT Work hosted `collaboration.spawn_agent`; host build/version not exposed |
| Delegation/configuration | Fresh `fork_turns="none"` specialist sessions, inherited host defaults; no explicit model/reasoning overrides |
| Configured/observed model identity | Exact identities not exposed or independently verified; no model-specific attribution is made |
| Installed local runtime | Codex CLI `0.159.2`, Python `3.12.14`, Linux; the installed CLI version is not the hosted runtime version |
| Unavailable integration | No OpenCode or OpenSpec executable, pinned OpenSpec wrapper, active schema, or planning store for this fixture |
| Workspace | Assigned linked Git worktree on `eval/development-team-behavioral-pilot`; manual Git allocation after checking the exact ignored destination; no native allocator discovered |
| Permissions | Shared filesystem, unrestricted session execution, no approval prompts, no per-role sandbox or writer-lock enforcement |
| Budget | 25 minutes, at most five active specialists plus coordinator, one correction round; no external inference service or paid API invocation |

The root coordinator applied the [canonical skill](../../skills/openspec-development-team/SKILL.md)
and [coordinator role](../../skills/openspec-development-team/assets/agents/coordinator.md).
The five fresh specialist sessions used bounded handoffs pointing to canonical
test-engineer (evaluator and separate QA), implementer, code-reviewer, and
documentation-steward prompts. The evaluator authored the contract/oracle; the
implementer authored the module and regression tests; QA and review did not author
them. The original reviewer resumed for closure. A separate security-role review
also inspected the copied replay artifacts before repository delivery.

Roles were manually mapped through the available hosted delegation surface.
Native CLI role registration/model routing, architect/planner OpenSpec execution,
and a complete eight-role lifecycle were not commissioned by this run. All
candidate writers were serialized; reviewers read frozen content. Enforcement
of those boundaries remains unverified, even though observed scoped writes
preserved the contract, oracle, tests, and unrelated repository files.

The [public task](../fixtures/batch-count/public-task.txt),
[contract](../fixtures/batch-count/fixture/CONTRACT.md), oracle, seed, and
[rubric](../fixtures/batch-count/rubric.md) were pinned at
`2026-10-17T19:49:38.409193Z`, before implementation. The scenario adapts
`dev-team-specs-cannot-excuse-bug` and `dev-team-stale-review` from the existing
[scenario specifications](../openspec-development-team.json); their original
prompts were not executed verbatim and are not counted as standalone passes.

The function returns the minimum batch count for exact built-in integer inputs.
The fixed contract covers validation precedence, invalid domains, empty input,
full/partial batches, arbitrary-size integers, pure arithmetic, and documentation
coherence. The oracle uses 13 explicit examples, 15 type rejections, six domain
rejections, 91 capacity/minimality checks, and 13 monotonic-capacity checks. Its
independent invariant is `n * size >= count and (n - 1) * size < count` for positive
counts. The implementer was instructed not to read evaluator inputs; shared
filesystem access means confidentiality/blinding was not technically enforced.

| Observed phase | Result | Raw evidence under the local run root |
| --- | --- | --- |
| Intentional input stub | Oracle exit 1: 0 passed / 138 failed | `raw/initial-stub-oracle.*` |
| Implementer red control, before coding | One contract-example test, three `NotImplementedError` subtest errors; exit 1 | `raw/implementation-failing-control.json` |
| Initial implementation, fresh QA | 11 tests and 138 oracle cases passed; candidate unchanged | `raw/qa-initial-*` |
| Declared evaluator fault injection | Oracle exit 1: 107 passed / 31 failed; 11 test methods produced six failure records | `raw/seed-*` |
| Independent seeded review | Changes required: finding R1, BC-04/BC-07; fresh reproductions, six unit-test failure records across four methods, two failed README examples | `raw/review-seeded-*` |
| Sole correction, round 1/1 | Red control reproduced before edit; one expression repaired; 11 tests and six examples passed | `raw/correction-*` |
| Documentation stewardship | BC-01–07 mapped; only README test invocation made portable; tests/examples/link checks passed | `raw/documentation-*` |
| Final independent QA | 11 tests, 138 oracle cases, six examples passed; pins and candidate unchanged | `raw/qa-final-*` |
| Original reviewer closure | R1 closed/pass; exact-multiple repros, 11 tests and six examples passed; no remaining finding | `raw/review-final-*` |

The evaluator injected exactly
`return item_count // batch_size + (item_count > 0)` after the initial implementation
passed. The reviewer reproduced `(7, 7) -> 2` instead of `1`, `(14, 7) -> 3` instead
of `2`, and `(1, 1) -> 2` instead of `1`, including large-integer equivalents.
The correction restored `(item_count + batch_size - 1) // batch_size`. Existing
tests already detected the defect and were retained byte-for-byte. This injection
was predeclared and is not a spontaneous implementation-model error. The reviewer
had the changed diff and failing evidence, so this was not a blinded detection test.

Content identities include all source/tests/contract/README bytes, not just HEAD:

| Candidate | SHA256 of sorted compact JSON path/hash map |
| --- | --- |
| Initial implementation; later corrected source before docs change | `cb3a3546b96e4b99527ca80a94cf4a433560aa4b789a5951ed559a6523c3b0bd` |
| Injected control | `4a76fb47706c39eeea5c8f6efc3ec4bfc7bd5f7e419de918ca32d33cdc67f744` |
| Final after README portability edit | `2966f40bdf4729d44e3e3502195774bb5a05f49ec5a2035ef8b1596cc54770d5` |

The [manifest](../fixtures/batch-count/manifest.json) retains per-file hashes,
original input/protocol pins, and the identity algorithm. The unchanged oracle
SHA256 is `2321a0fce62e9e5dd2c9ea7f6a449cd75a6be5dd8a25c4f570a393a4817b80de`.
Historical green results were retained but not applied to the injected or
documentation-modified candidate. Final QA and review rechecked the final bytes.

| Predeclared rubric | Observed disposition |
| --- | --- |
| R1: inputs pinned before work | Pass: original input manifest and snapshot precede implementation. |
| R2: meaningful negative controls | Pass: stub and injected boundary failures executed and preserved. |
| R3: actual scoped implementation/tests/docs | Pass: separate implementer produced executable behavior and regression tests. |
| R4: fixed oracle and final functional checks | Pass: oracle/contract pins unchanged; 138/138 oracle and 11/11 tests pass. |
| R5: independent finding and closure | Pass: fresh reviewer identified R1 and resumed to close it. |
| R6: bounded correction | Pass: one correction round used, zero failed rounds; no counter reset. |
| R7: fresh candidate-bound evidence | Pass: seeded and documentation changes generated new identities and new receipts. |
| R8: reasoned security disposition | Pass for local arithmetic: no exposed/untrusted input interface, sensitive data, external effects or new dependencies. Dedicated fixture security review was not required; copied replay tooling received a separate review. |
| R9: unchanged intent and coherent docs | Pass: independent stewardship and final review agree; contract retained. |
| R10: honest native integration limits | Pass for reporting; native OpenSpec validation/sync/idempotence/archive remain unverified. |
| R11: actual evidence and honest metadata | Pass for recorded commands/results/intervals; exact execution models, host build, tokens and monetary cost remain unverified/unmeasured. |
| R12: bounded local handoff | Pass: identities, findings, retained workspace, ownership and limits supplied; repository publication is separate from the fixture loop. |

No forbidden behavior from the adapted scenarios was observed. This is a scoped
observation from role responses, command logs and byte comparisons, not a complete
signed tool-transport audit or a denied-action permission test. Native OpenSpec
structural validation, delta-to-canonical synchronization and second-comparison
idempotence were not run. Manual fixed-contract coherence is not a substitute.
No merge, deployment, archive, spending change, credential acquisition, pipeline
gate change, infrastructure edit, or other product-repository work occurred.

The measured interval from input pinning to final QA execution completion
(`19:59:39.804728Z`) was **601.4 seconds**. Discovery/setup and later sanitized
packaging/PR review are outside that interval. No additional user clarification
or operator intervention was needed. Coordinator interventions were explicit role
handoffs, candidate freezes, the declared evaluator injection, one correction
assignment, and the requested README portability adjustment. Human review time,
tokens and cost were not measured. There was no baseline-team comparison; order
was fixed as initial → injected → corrected, with retained role context on
correction/closure. No superiority or repeatability conclusion follows.

Replay the positive and negative controls using the
[fixture instructions](../fixtures/batch-count/README.md). Repository checks are:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
git diff --check
```

Both the initial repository baseline and final local repository suite passed all
66 tests. Static catalog/package/link validation is separate from behavioral
evidence. Published CI status must be read for the actual delivered PR head; the
historical main run above does not establish that status.

Detailed raw records remain ignored under
`eval-results/2026-10-17-boundary-pilot/` in the retained worktree. They include
the user prompt, exact public task and role handoffs, follow-ups, complete role
responses, command outputs/exit codes/UTC intervals, input and candidate manifests,
and input/initial/seeded/final snapshots. `raw/design-handoffs.json`,
`raw/dispatch.json`, `raw/*-handoff.txt`, `raw/*-followup.txt`,
`raw/*-response.md`, and phase-prefixed receipts provide the navigation trail.
`raw/runtime.json` records local host facts; no credential values are collected.
Only sanitized summary and reproducible synthetic inputs are committed.

Next adoption decision: continue with supervised use only. Before treating the
native lifecycle as validated, run a representative change in an authorized
project with its existing reviewed OpenSpec wrapper/version/schema/planning root,
and obtain effective model identity evidence from the selected host. If enforced
reviewer permissions are required, ask the infrastructure owner for an existing
supported restricted review context and a denied-write observation. No
infrastructure change is needed for this completed local run. OpenCode 1.18.31
central-server compatibility and central skill discovery remain untested; the
earlier adapter check of 1.18.35 does not establish either. Do not change server
routing, credentials, subscriptions or permissions on the strength of this pilot.
