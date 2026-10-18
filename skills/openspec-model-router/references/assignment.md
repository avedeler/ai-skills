# Assignment and handoff

Send only relevant information, but enough for a child without conversation history:

```text
Task ID / OpenSpec task IDs:
Outcome and current phase:
Model/effort rationale:
Repository/worktree and applicable instruction paths:
User constraints and authorized scope:
Read these artifacts and interfaces:
Known evidence and prior failed attempts:
Dependencies already satisfied:
Owned writable paths (or READ-ONLY):
Paths/resources reserved by others:
Acceptance criteria and relevant checks:
Return: result; changed paths; checks run and actual outcomes;
        evidence/citations; unresolved risks or blockers.
Do not spawn children. Do not edit global OpenSpec task checkboxes.
If scope or an interface must change, report it before editing outside ownership.
```

The root maintains the global plan, spec decisions, task checkboxes, and integration. A child can own a specific spec artifact if explicitly assigned; no second writer may edit it concurrently.

Example split: the focused worker maps existing expiry handling; the strong design worker resolves session semantics in the proposal/specs; the architecture specialist evaluates a cross-service revocation architecture only if required; the design worker writes design/tasks from the selected decision. Once interfaces are stable, the focused worker implements a conventional validation helper while the strong implementation worker implements session middleware in separate paths. The root integrates and verifies expiry/revocation scenarios. Do not spawn all these roles for a one-file change.

For escalation, hand over the spec requirement, observed behavior, exact failure, changed paths, hypotheses eliminated, and remaining question. Stop the original writer before transferring ownership.
