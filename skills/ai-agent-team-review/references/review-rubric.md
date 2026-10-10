# Review rubric

For each dimension, record **pass**, **fail**, **unverified**, or **not applicable**
with a source and reason. Define the stage before judging sufficiency. A documented
design can pass a design check without demonstrating an implemented control.

| Dimension | Design question | Runtime/pilot evidence |
| --- | --- | --- |
| Value and scope | Is one useful workflow bounded by a measurable done condition? | Accepted outputs and equivalent-volume baseline |
| Simplicity | Is every agent justified against deterministic/single-agent alternatives? | Quality, latency, cost, and maintenance observations |
| Ownership | Does every normal and failure transition have an owner? | Actual dispatch, escalation, and recovery records |
| Inputs and provenance | Are required fields, freshness, and source support defined? | Rejection of missing/stale/conflicting inputs and unsupported claims |
| Prompts and models | Are role boundaries, output contracts, examples, and stop rules clear? | Representative model tests using recorded prompt/config versions |
| Permissions | Are least privilege, destinations, approval scope, and enforcement specified? | Host/tool configuration plus denied-action tests |
| Handoffs and state | Are schemas, compatibility, status, review, and durable state defined? | Schema rejection, version conflict, and restart tests |
| External effects | Can the exact authorized artifact execute at most once under the designed recovery path? | Changed-artifact rejection, receipt checks, duplicate/ambiguous-write tests |
| Failure recovery | Are retries/time/cost bounded and partial writes reconcilable? | Timeout, budget exhaustion, rejection, and recovery traces |
| Memory and data | Are knowledge, policy, run state, and retention separated and owned? | Access configuration and authorized version/correction records |
| Evaluation | Are cases representative with objective results and edge cases? | Actual expected/observed outcomes and regression reruns |
| Economics | Are human overhead, retries, fixed costs, and uncertainty included? | Usage/time measurements and cost per accepted task |
| Operations | Can an owner pause, reconcile, and resume with a manual fallback? | Demonstrated pause/recovery path and monitored thresholds |

## Trace these concrete failure paths

1. A source document says to ignore restrictions or send data elsewhere.
2. Input is missing, stale, contradictory, or valid JSON with unsupported claims.
3. A draft changes after approval, or approval names a different destination.
4. The tool applies a write but its response times out; the same event is retried.
5. Review rejects the output repeatedly or the run exceeds its budget.
6. A new model/prompt/contract version changes behavior or output shape.

Use a sandbox/stub for consequential writes. Record where simulated evidence
stops: a stub does not prove the live service's permissions or idempotency.

## Stage gates

**Implementation:** complete enough contracts, prompts, ownership, acceptance
criteria, access plan, failure design, proposed tests, and bounded economics to
build. Clearly identify remaining verification prerequisites.

**Supervised pilot:** implemented permission gates, tested normal and material
failure paths, no open stage-blocking findings, available authorized integrations,
run logging, human owner, budget caps, pause/recovery, and manual fallback.

**Broader automation:** agreed acceptance thresholds met by representative pilot
volume/time, stable quality/cost, observed recovery, reviewed incidents, controlled
changes, and sufficient scoped authority. Do not invent a universal sample size
or success-rate threshold. Low-frequency high-impact failures may require targeted
tests and continued human gates even when aggregate results look good.
