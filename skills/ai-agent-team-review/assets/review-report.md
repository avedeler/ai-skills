# Review report template

Workflow/revision: [value]  |  Reviewer/date: [value]
Requested stage: [implementation / supervised pilot / broader automation]
Verdict: [ready for named stage / not ready / insufficient evidence]
Reason and practical limit: [brief explanation; what was and was not verified]

## Findings

| ID / severity | Evidence and location | Failure/impact | Smallest fix | Owner | Closure test/evidence |
| --- | --- | --- | --- | --- | --- |
| [F1 / blocker] | [artifact revision, section, result] | [consequence] | [concrete change] | [owner or needs assignment] | [observable result] |

## Evidence coverage

| Dimension | Pass/fail/unverified/N/A | Stage and basis | Missing evidence |
| --- | --- | --- | --- |
| [rubric dimension] | [status] | [source + observed/reported/assumed] | [specific gap or none] |

Distinguish static inspection, simulated test, sandbox test, and live observation.
List tests actually run, versions, outcomes, and evidence references. Mark proposed
or unrun tests explicitly. Do not equate a described gate with enforcement.

## Economics and complexity

- Smallest sufficient architecture and removable roles: [reason].
- Comparable manual baseline and accepted-output volume: [values/source].
- Review/rework/fallback/maintenance effort: [values/source].
- Net weekly savings: [calculation, range, or unknown].
- Full recurring cost and cost per accepted task: [basis, including retries].
- Setup effort and payback: [calculation or not established].

## Repair and retest order

1. [Blocker → fix → owner → safe retest → evidence required.]
2. [Next material gap and dependencies.]
3. [Monitoring/change follow-up.]

## What can proceed

[Specific next-stage work within existing authority, residual limitations, and
conditions required before a later stage. A review is not deployment approval.]

## Next action

[One concrete action with an owner and expected evidence.]
