# Handoff contract template

Complete one contract per boundary. This is a specification to implement in the
chosen runtime; the Markdown itself provides no validation or access control.

## Identity and schema

- Contract name/version: [name and version].
- Producer → consumer; business owner: [values].
- Allowed workflow state transition: [from → to, authorized transition owner].
- Transport and authoritative storage: [queue/file/API/database and owner].
- Required fields, types, limits, and enumerations: [list or schema].
- Unknown-field and version-mismatch policy: [reject or explicit compatibility].
- Data classification, redaction, access, retention/deletion: [rules and owner].

Illustrative JSON envelope; replace placeholders and define the payload schema:

```json
{
  "contract_version": "1.0",
  "run_id": "synthetic-run-001",
  "business_event_id": "synthetic-event-001",
  "idempotency_key": "synthetic-event-001:draft:v1",
  "producer": "drafting-role",
  "recipient": "review-role",
  "input_ref": "inputs/synthetic-brief-v1.json",
  "input_version": "v1",
  "artifact_ref": "outputs/synthetic-draft-v1.json",
  "artifact_version": "v1",
  "status": "review_pending",
  "evidence": [{"source_ref": "synthetic-brief-v1", "locator": "item-1"}],
  "assumptions": [],
  "errors": [],
  "approval_ref": null,
  "tool_receipt_ref": null
}
```

## Acceptance

- Required validation: [schema, provenance, freshness, calculations, destination].
- Semantic checks: [claim support, tone, completeness, confidence limitations].
- Acceptance/rejection owner: [role with actual authority].
- Valid example / invalid example and reason: [concrete payloads].
- Incomplete or unsupported evidence: [blocked status and resolution owner].
- External execution requires: [exact action, destination, artifact version/hash,
  current approval record and scope, preconditions, executor permission].
- Completion requires: [verified receipt/state and where it is recorded].

## Recovery and delivery

- Timeout and per-run budget: [limits].
- Retryable errors / maximum attempts / delay: [explicit rules].
- Non-retryable errors and escalation: [conditions, owner, next action].
- Deduplication key, persistence, and lifetime: [rule that survives restart].
- Conflicting/late/out-of-order event behavior: [version and ordering rule].
- Review rejection route and maximum revision cycles: [rule].
- Ambiguous or partial external action: [lookup receipt/state, reconcile, stop].
- Rollback or compensation: [specific supported action, or manual recovery when
  rollback is impossible; never claim a sent message can be unsent].
- Logs: [redacted transitions, timestamps, prompt/model versions, error class,
  reviewer/approval refs; no credentials or unnecessary customer data].
