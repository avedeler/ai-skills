# Requirement-driven test plan

Change and candidate: [values] | Test owner: [role] | Policy revision: [value]
Execution environment and known prerequisites: [actual/unknown]

| Requirement/scenario | Fixture | Expected behavior | Check ID/test location | Level | Failure/edge case | Status/evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [IDs from specs] | [input] | [observable assertion] | [command/job + test] | [unit/etc.] | [case] | [proposed/not run] |

Include representative normal behavior, a boundary/failure case, a regression,
relevant integration behavior, and the highest-risk security/side-effect boundary.
Use fewer tests for trivial documentation changes when those categories do not
apply; give reasons. Add more tests when five examples would miss material risk.

Required command/job IDs: [reviewed set]
Optional diagnostic checks: [set and reasons]
Coverage/assertion-quality strategy: [risk-based, baseline-aware]
Baseline failures and authorized disposition: [evidence]
Timeout, resource and correction limits: [values]
Safe fixture isolation and cleanup: [procedure]
Missing capabilities: [blocked checks; no implicit fallbacks]

Observed evidence records command/job, exit, counts, environment and candidate.
Mark proposed cases separately. A skipped or unexecuted required check is not a pass.
