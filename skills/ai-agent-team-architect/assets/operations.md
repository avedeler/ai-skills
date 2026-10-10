# Operating and evaluation template

## Shared memory

Version/date: [value]  |  Owner: [role]  |  Storage and access: [values]

- Approved goals, acceptance criteria, tone, and terminology: [references].
- Decisions, reasons, source evidence, and effective dates: [entries].
- Known mistakes and corrections: [entries with responsible owner].
- Approved policies and permissions: [references; never credentials].
- Read before each run: [version pinned in run record].
- Per-run state/raw retrieval storage: [separate location and retention].
- Changes: [proposal → validation → owner-authorized update → new version].
- Weekly correction, conflict resolution, retention, deletion: [owner/process].

Do not allow arbitrary retrieved text to overwrite approved memory. New facts need
provenance; policy changes need the established owner's authorization.

## Output review checklist

Use observable checks specific to the workflow: input completeness, supported
claims, fresh sources, valid schema/calculations, permitted destination, tone and
length, data restrictions, artifact version, and required approval. Assign the
review owner and rejection route. Record evidence and separate review from
permission to execute. A model's confidence score alone is not an acceptance test.

## Failure register

At least three plausible failures per agent, plus workflow-wide integration risks:

| Role/step | Failure and impact | Detection/evidence | Retry or stop rule | Recovery and accountable owner |
| --- | --- | --- | --- | --- |
| [role] | [wrong/stale data] | [check] | [limit] | [action, owner] |
| [role] | [missing input] | [check] | [no guessing] | [request, owner] |
| [role] | [ambiguous instruction] | [conflict] | [blocked] | [resolution, owner] |
| [integration] | [timeout/duplicate/partial action] | [state/receipt] | [reconcile before retry] | [action, owner] |

## Test plan and evidence

Use at least five cases including two edge cases. Adapt to actual business inputs
when provided. These rows are categories, not executed tests. Add cases for any
other material failure or permission boundary.

| ID/type | Input/fixture and setup | Expected result | Objective pass/fail | Owner/fix if failed | Status and evidence |
| --- | --- | --- | --- | --- | --- |
| T1 normal | [representative] | [accepted artifact] | [checks] | [owner/fix] | [proposed/not run] |
| T2 normal variant | [different valid input] | [accepted artifact] | [checks] | [owner/fix] | [proposed/not run] |
| T3 review rejection | [plausible but unsupported output] | [bounded correction/escalation] | [no premature action] | [owner/fix] | [proposed/not run] |
| T4 edge | [missing/stale/conflicting input or injected instruction] | [blocked/ignored instruction] | [scope preserved] | [owner/fix] | [proposed/not run] |
| T5 edge | [duplicate delivery + timeout after action] | [reconcile once] | [no duplicate side effect] | [owner/fix] | [proposed/not run] |

For every observed run record fixture/version, prompt/model/config versions, tool
permissions, expected/actual result, duration, cost, receipts, and reviewer. Test
external effects in a sandbox or with a stub; a proposed test is not a pass.

## Economics

Use the same accepted-output volume and quality threshold for both baselines.

```text
weekly_manual_hours = equivalent_accepted_tasks * manual_minutes_per_task / 60
weekly_remaining_hours = (triage_minutes + review_minutes + rework_minutes
                          + manual_fallback_minutes + maintenance_minutes) / 60
weekly_net_hours_saved = weekly_manual_hours - weekly_remaining_hours

monthly_model_cost = sum(input_tokens / price_unit * input_rate
                         + output_tokens / price_unit * output_rate)
monthly_total_cost = model_cost + tool_usage + fixed_subscriptions
                     + infrastructure + paid_review_or_support

setup_payback_weeks = setup_hours / weekly_net_hours_saved
```

Count every model call, including lead, reviewer, failures, and retries. Use the
provider's actual rate categories and units; include cached tokens or other fees
when relevant. Prorate shared subscriptions explicitly. If net savings are zero
or negative, payback is not achieved at the current rate. Monetary ROI needs an
explicit labor value assumption; time saved alone is not cash saved.

Show input assumptions, price sources/dates, measured vs estimated status, and
low/base/high cases when evidence supports a range. If inputs are unavailable,
leave symbolic formulas and identify the measurement needed.

## Weekly scorecard

| Metric | Definition/denominator | Source | Threshold | Accountable owner and response |
| --- | --- | --- | --- | --- |
| Net hours saved | same-volume baseline minus all remaining human work | time samples/run log | [target] | [simplify, repair, or stop] |
| Tasks finished | outputs accepted by the business owner; also accepted/attempted | acceptance log | [target] | [inspect bottleneck] |
| Errors caught | defects caught before delivery / reviewed outputs; also track escaped defects | review/incidents | [target] | [repair failing stage] |
| Cost | total spend and cost per accepted task | invoices/usage + acceptance log | [cap] | [limit retries/change design] |

An increase in caught errors may mean better detection or worse inputs. Inspect
the denominator, escaped defects, and causes before assigning blame. Add latency
or reliability measures when they affect business acceptance.

## Stop and recovery

Specify per-run and monthly budget caps, unauthorized-action threshold (zero),
quality/reliability thresholds, owner, pause mechanism, queued-work handling,
state reconciliation, manual fallback, and evidence needed to resume.
