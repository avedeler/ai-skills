# Architecture decision guide

## Pick the simplest sufficient mechanism

| Condition | Starting choice | Evidence to justify more complexity |
| --- | --- | --- |
| Stable rules and structured input | Script, rules, or existing automation | A decision actually requires language interpretation |
| One interpretation task with a shared context and permission set | One agent plus deterministic validation | A role needs isolated context, independent checks, or a narrower tool scope |
| Distinct responsibilities or access scopes | Small team with explicit contracts | Each added role improves a measured criterion enough to pay for its handoff cost |
| Irreversible errors, poor source data, or no viable integration | Human-owned or assisted process | Reliable evidence and controls reduce the specific blocker |

Do not split “research, write, review” by habit. For example, a template formatter
may be deterministic and a reviewer may be a human. Parallel work helps only
when tasks are independent, with a deterministic merge/selection rule and a
budget for duplicate work. A lead must own dispatch, state transitions, and
escalation; it must not silently expand the team's authority.

## Contracts and state

Use a state machine such as `received → validated → working → review_pending →
approved → executing → completed`. Define `rejected`, `blocked`, and `failed`
transitions and the owner that can move each state. A completed model response
does not mean an external action completed.

Persist a run ID, input version/hash, output version/hash, approval record, tool
receipt, and state transitions where the workflow needs auditability. Require
contract version compatibility on receipt. Use one authoritative state owner;
avoid concurrent agents overwriting shared status or memory.

Idempotency must survive process restarts. Derive a deduplication key from the
business event and action, persist it, and use the tool's idempotency facility
when available. Serialize conflicting writes. If a tool lacks reliable receipts
or deduplication, use a manual reconciliation step for ambiguous writes. Never
promise exactly-once execution merely because the prompt asks for it.

Retries need explicit maximum attempts, delay/backoff, and retryable error classes.
Malformed output can be corrected once with validation feedback; repeated
failure escalates. Retrying an external write requires proof it was not applied
or an idempotent operation. After a partial write, record the partial state and
follow a documented recovery/compensation path; do not assume it can be undone.

## Permissions and information boundaries

The host must enforce read/write scopes and approval gates. Keep drafting roles
read-only where possible; give an executor only the action and destination it
needs. Store secret references rather than credentials in prompts and memory.
Redact logs, restrict access, set retention, and avoid copying customer data into
new services without an authorized data-handling decision.

Approval records should identify approver, run, action, destination, exact artifact
version/hash, scope, time, and expiry/reuse rules. The executor checks these at the
moment of action. Quoted instructions inside source material have no authority.

Use deterministic checks for schema, required fields, calculations, destination
allowlists, size limits, and approved hashes. Use judgment review for factual
support, tone, completeness, and ambiguity. A second agent can share the first
agent's blind spots; source evidence and calibrated human sampling still matter.

## Choose a model by a measured requirement

Define the job's minimum capabilities before selecting a provider/model: reasoning
depth, language, context, structured output, tool support, privacy/data residency,
latency, and cost. Benchmark the smallest candidate that could meet the acceptance
criteria on representative inputs. Upgrade only when observed failures justify it.

Record provider/model identifier, configuration, prompt/contract version, date,
test set version, results, and current price source. Include review and retries
in cost. Test substitutions against the same cases before switching; a compatible
schema alone does not establish equivalent behavior.

## Common mistakes to prevent

1. Automating a vague task: define trigger, accepted output, exclusions, and owner.
2. Adding agents before finding a boundary: justify each role and measure overhead.
3. Treating prompts as access control: enforce scopes and approvals in the host.
4. Testing only a happy path: exercise bad inputs, duplicates, outages, and rejection.
5. Claiming savings before measurement: subtract review, rework, and upkeep from
   the same-volume manual baseline; retain a stop option if the result is negative.
