# Independent review and correction record

Initial candidate file-manifest fingerprint:
`9c83ccd9584c6fad7fea3478a08e51253887408fbf696639b91a6cff3e296a20`.

Both fresh-context review requests were accepted with `gpt-6.1-sol`, `high`.
They did not author the implementation/tests and remained read-only. The host
does not expose independent effective-model identity or usage/cost telemetry.

Initial checks: validator passed, 78 tests passed, strict OpenSpec 1/1 passed;
temporary-root integration with the actual CLI resolved the selected change as
ready. Review demonstrated these checks did not close the following defects:

| ID | Finding | Required closure |
| --- | --- | --- |
| R1 | Workspace values were unquoted in generated shell commands | Single-pass rendering, quoted arguments, spaces/metacharacter/placeholder controls |
| R2 | Project wrapper selection changed the expected global AGENTS block | Separate project command/version; preserve installed policy and observe wrapper execution |
| R3 | Relative install commands were persisted without a stable base | Canonical absolute install command; project-relative wrapper resolution |
| R4 | Subprocess test did not observe cwd/complete argv | Record and assert actual cwd, argv, telemetry and project preservation |
| R5 | Unused dynamic installer import wrote bytecode during verification | Remove import and prove cache-free source snapshot is unchanged |
| R6 | Dangling AGENTS symlink was overwritten | Reject resolving/dangling instruction symlinks and unsafe parents before writes |
| R7 | Unexpected package FIFOs were accepted | Reject source/installed special nodes without blocking on reads |

One grouped correction packet was implemented by the original focused worker;
all 15 focused tests passed. No failed correction round yet. The original
reviewers must inspect closure on the corrected candidate.

Accepted routing requests (fresh context, no inherited-history overrides):

- `cloud_workflow_implementation`: `gpt-6-luna`, `medium`.
- `workflow_code_review`: `gpt-6.1-sol`, `high`.
- `workflow_security_review`: `gpt-6.1-sol`, `high`.

These are accepted request settings, not independently observed execution model
IDs. No model-cost or token-saving claim is made.

Re-review closed R1-R7, including independent source-preservation and argv/cwd
mutation controls. It found R8: default environment execution could select an
unrequested project-local same-name executable. One correction round therefore
failed acceptance. Escalate this bounded resolver repair and its regressions to
`gpt-6.1-sol`, `medium`, then return to the original reviewers. Budget remaining:
one failed correction round; do not reset it for the new worker.

The separate root-owned deployment bootstrap also needs preservation checks for
source/npm/command destinations before mutation, a staged managed versioned tool
prefix, and explicit fresh/repeat/conflict controls. Its publication is not yet
approved by security review. The adapter's original security findings are closed.

## Corrected source acceptance

Final code-review candidate file fingerprint:
`da2e441cbefe44c494e519b6fdb7f17f2ded43c1a031e81268cdcf86ad21c3b1`.
The final stronger worker request `resolver_correction` was accepted with
`gpt-6.1-sol`, `medium`. Three real-subprocess regressions failed before its fix
and passed afterward. The original code reviewer independently reran 18 focused
tests and three mutations restoring those bugs; each mutation was detected.
Original code and security reviewers passed the corrected source. One failed
correction round was used; the budget was not reset during escalation.

Final automated checks: repository validator passed; all 87 tests passed in
20.747 seconds; strict OpenSpec passed 2/2; whitespace check passed. Canonical and
delta requirement bodies were compared exactly and the second sync was a no-op.
Source semantic claims above are unchanged by later mechanical receipt/task edits.

The bootstrap now stages a separate versioned tool prefix, audits it, records a
full-tree digest and reuses only identical managed content. Security review
passed that preservation design; root added a pre-read special-node check and
13 no-network preservation controls, all passing. Its actual audit, fresh/repeat
installation, environment publication and fresh-task discovery are separate
acceptance steps. The setup template remains outside this public source tree.
