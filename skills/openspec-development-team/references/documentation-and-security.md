# Documentation, conformance, and security gates

## Documentation and spec obligations

Assign documentation ownership in the plan. The implementer updates behavior-level
docs with the code; the steward checks coherence across the delivered package;
the code reviewer verifies material claims. Review at least:

- Public API/CLI contracts, configuration defaults, errors, and compatibility.
- Setup/dependency instructions and runnable examples for changed workflows.
- Architecture boundaries, data flow, decision rationale, and invariants.
- Operational failure modes, migration/recovery steps, and observability.
- OpenSpec proposal/design/task consistency and scenario-to-test mapping.
- Delta-to-canonical-spec synchronization and post-sync semantic comparison.

Comments should explain why, constraints, or surprising behavior. Avoid duplicating
obvious code and avoid prose that goes stale on every refactor. Use appropriate
docstrings/types for exposed interfaces. Do not require boilerplate on trivial
helpers; prioritize the contract a future maintainer needs.

An advisory drift script is a signal, not sufficient proof of conformance. Missing
or contradictory required documentation/specs blocks completion until reconciled.
Validate file references, generated docs, and examples where tooling exists.
Never alter approved requirements only to fit accidental implementation behavior.

“All task boxes checked,” “spec files parse,” “CI is green,” and “the change is
archived” are separate facts. None alone proves the code meets its specification.
Do not describe deployed behavior without deployment evidence.

## Security applicability

Every change receives triage. Require a dedicated review when it touches:

- Authentication, authorization, identity, session or tenant boundaries.
- Sensitive data collection, storage, exposure, redaction, retention or logging.
- Untrusted input, parsing, templating, queries, file paths or serialization.
- Network requests, remote callbacks, exposed endpoints or execution boundaries.
- Cryptography, credentials, permissions, deployment or CI configuration.
- Dependencies, install/build hooks, privileged code, or sensitive migrations.

Unclear impact is `unknown` and remains unresolved. A narrow typo/docs change can
be `not_required` with a reason and reviewed scope. A security reviewer or an
independent code reviewer can challenge a skip. Assess again if the diff changes.

Use existing approved static, dependency, and secret scanners when applicable.
No one tool covers all risks; semantic review follows relevant data flows and
authorization paths. Missing mandatory scanners or stale dependency evidence
blocks that check. Do not disable enforcement or retrieve credentials to continue.

Findings need evidence, reachability, impact, severity, and a closure test. Treat
automated output as evidence to assess, not unquestionable truth. A confidence
number cannot substitute for reasoning, and an outer access layer cannot dismiss
a flaw exploitable by an authenticated or compromised client. Record accepted
exceptions through the accountable owner's existing policy.

## Completion checklist

- Approved scope is implemented; required scenarios are accounted for.
- Required checks pass for the candidate, with actual evidence and provenance.
- Independent code review passes; applicable security review passes.
- No unresolved material findings; attempted corrections are within budget.
- Documentation and specs match the approved behavior, including negative paths.
- Selected deltas are synchronized and a second comparison is clean.
- The intended delivery claims match results; final CI matches the delivered head.
- Merge/deployment/archive authority is separate from readiness evidence.
