# Behavioral evaluations

Each `evals/<skill-name>.json` file contains synthetic acceptance scenarios for
one skill. They are test specifications, not recorded results. They can be run
with any compatible host and model; no vendor-specific evaluation SDK is required.

For a manual evaluation:

1. Install the named skill and its bundled files in the target host.
2. Start a fresh conversation and send the scenario's `prompt`. Do not copy its
   expected/forbidden behaviors into the user's message.
3. If the skill asks relevant questions, answer using only scenario facts. Where
   a fact is intentionally missing, say it is unknown and request a provisional
   result. Keep that fact unknown when grading.
4. Save the prompt, skill revision, host/model/config, response, follow-up turns,
   and any actual tool evidence in a local evaluation record.
5. Mark each expected behavior pass/fail/unverified. Any forbidden behavior is
   a failure. For authority or evidence claims, inspect tool logs as well as prose.

Do not infer model quality from static checks. A single successful response is
not proof of consistent performance; repeat relevant cases across model changes
and use real, redacted task inputs before live use. Never introduce real
send/payment credentials to a synthetic scenario.

New skills use the [evaluation starter](../templates/evaluation.json). Give each
scenario a globally unique ID and ensure its `skill` matches the filename and
catalog. Include normal, boundary, and failure behavior relevant to the domain.

Suggested evaluation record:

```text
Scenario / skill revision / date:
Host / model / config:
Response and tool evidence location:
Expected checks: pass / fail / unverified with evidence
Forbidden behavior observed: yes / no with evidence
Outcome and follow-up:
```

Keep local results under ignored `eval-results/`; commit only sanitized evidence
when explicitly intended for the repository. Static validation requires no
provider credentials, paid requests, or external service access.

Recorded, sanitized evidence: [2026-10-17 bounded development-team pilot](reports/2026-10-17-development-team.md).
It includes real hosted role execution and reproducible synthetic controls, with
native OpenSpec and CLI-adapter limitations recorded separately.
