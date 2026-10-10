# Workspace record

Store this with the existing change evidence and link it from assignments. The
host remains authoritative for claims, session binding, permissions and lifecycle.
Use actual observations; leave unavailable values explicit.

- Change, coordinator and authorized stages: [values]
- Existing worktree preference/authority and source: [user/project/host decision]
- Code repository root and assigned working directory: [absolute paths]
- Isolation kind: [native isolated checkout / linked Git worktree / permitted in-place]
- Git directory, common directory, superproject and registered worktree: [observed]
- Native workspace ID, bound session and owner/helper: [verified / not applicable]
- Branch or detached HEAD, base ref and resolved base commit: [values]
- Pre-existing tracked/untracked changes and ownership: [values]
- Creation/reuse route and selected destination ignore check: [evidence / not applicable]
- Separate planning/spec store, workspace, branch and writer owner: [mapping / none]
- Setup and baseline commands/jobs, candidate, environment, exits and results: [evidence]
- Failed/unavailable baseline checks and owner/project disposition: [evidence / none]
- Workspace readiness: [ready / blocked with reason; never infer a test pass]
- Current writer role/session, allowed paths and handoff point: [host claim reference]
- Frozen review candidate and permitted readers: [values / not frozen yet]
- Test resource isolation: [approved runner/resources / known collisions or blockers]
- Final branch/checkpoint, candidate and delivered PR/artifact: [actual values]
- Retention/cleanup owner, authority and outcome: [retained / removed with evidence]

Baseline evidence and final candidate verification are separate. Do not claim
native binding, exclusive access, independent review or cleanup from this template
alone. Keep host-specific paths and private state in the target project's evidence.
