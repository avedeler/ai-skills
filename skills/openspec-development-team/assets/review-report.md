# Development review and correction packet

Change: [id] | Candidate: [trusted identity] | Reviewer/session: [actual value]
Scope: [code / security / documentation/specs]
Verdict: [pass / changes required / blocked]
Evidence level: [source inspection / sandbox test / live observation]

| Finding ID/severity | Requirement and location | Evidence/reproduction | Impact | Smallest fix | Closure check |
| --- | --- | --- | --- | --- | --- |
| [id] | [scenario + file:line] | [raw reference] | [effect] | [bounded action] | [observable result] |

Required tests and actual results: [candidate-bound references]
Security triggers and disposition: [required/not required/unknown + reason]
Docs/spec coherence and sync comparison: [evidence or missing]
Remaining findings, capability gaps and limitations: [values]

Correction round: [persistent count; default max two failed rounds]
Previous finding closure: [ID → fix → regression evidence → reviewer conclusion]
Next owner/action: [value]

A suggestion is not a blocker unless it affects an agreed acceptance criterion
or material defect. A pass covers only the named candidate and does not authorize
merge, deployment, scope expansion, or archive.
