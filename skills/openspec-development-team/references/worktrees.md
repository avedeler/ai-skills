# Worktree integration for the development team

Apply this guide before the first repository write. Establish workspace ownership
before authoring architecture, OpenSpec or implementation artifacts. The scoped
ignore-rule preparation below is an explicit setup exception. Read the bundled
[using-git-worktrees skill](../third_party/using-git-worktrees/SKILL.md) with these
integration rules. The skill is by **Jesse Vincent (obra)**, from **Superpowers**,
under the [MIT License](../third_party/using-git-worktrees/LICENSE). Its
[provenance](../third_party/using-git-worktrees/README.md) travels with this package.

The upstream text is unchanged. This guide defines how the team applies it to
host-managed workspaces, serialized role handoffs, and evidence. User instructions
and host policy govern both. Tool names in the source are optional examples;
require no particular assistant, provider, or model. Announce use of the skill.

## 1. Detect and reuse isolation

The coordinator owns workspace selection and the writer assignment. Inspect the
host's current workspace binding and repository instructions first. Then inspect
Git, using read-only commands from the intended code repository:

```sh
git rev-parse --show-toplevel
git rev-parse --path-format=absolute --git-dir --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git rev-parse HEAD
git status --short
git worktree list --porcelain
```

On older Git, resolve `--git-dir` and `--git-common-dir` to physical absolute paths
before comparing; relative spelling alone is insufficient. Different Git and
common directories indicate a linked worktree; inspect the superproject result
and registered worktree list to distinguish submodule layouts. Do not mistake a
submodule's Git metadata for evidence that the containing checkout is isolated.
Never create a new worktree blindly inside a submodule; resolve its owning change
and the project's submodule policy first.

Reuse an existing linked worktree or host-confirmed isolated checkout **when it
belongs to this change and session**. A linked worktree for another task is not
permission to overwrite it. Preserve dirty and untracked work. Resolve ambiguous
ownership before dependent writes. Do not create nested worktrees because a new
specialist starts or because native isolation uses a normal Git directory layout.

A detached HEAD is not proof of a broken workspace. Record it, preserve the host's
lifecycle, and establish an authorized branch or durable checkpoint/export before
handoff or disposal. Do not attach a host-managed checkout to a guessed branch.

Honor existing worktree preferences and authorization without asking again. If
neither the user nor project/host policy has established a preference, apply the
upstream consent step. A permitted in-place choice must be explicit in the record;
never label it isolated. Read-only discovery can continue while selection is open.

## 2. Prepare the workspace using its owner

**Native route first.** Discover the host's approved workspace tool or helper.
Use it for allocation, session binding, branch selection and lifecycle. Verify the
returned path, branch/change identity, and current session binding before dispatch.
Changing directories alone may not bind the agent to a managed workspace. Do not
create a second queue, invent a native API, or bypass a helper that rejects a request.

**Manual Git fallback only when no native mechanism exists and policy permits it.**
Choose an explicitly configured location first, then an existing `.worktrees/`,
then an existing `worktrees/`, then `.worktrees/` at the repository root. Verify the
**actual chosen destination** is ignored if it lies inside the repository:

```sh
# Example destination after checking the chosen location and branch are unused:
git check-ignore -v -- .worktrees/change-example
```

Require a successful match for that destination. An ignore rule for `worktrees/`
does not protect `.worktrees/`. For a new project-local directory, add its anchored
rule to `.gitignore` and commit only that rule under the existing authorization,
as upstream requires, before creation. If that preparation cannot be performed
within scope, stop the dependent setup or use an already authorized external
location. Do not stage unrelated work. External locations need no repository
ignore rule but still require ownership and collision checks.

Check existing paths and branches, record a verified base ref and full commit,
then create the chosen worktree with `git worktree add` and a new change branch.
Use explicit reviewed arguments; do not infer a base from a stale default branch.
For an existing branch, verify ownership and whether it is already checked out;
reuse its correct worktree rather than forcing a second checkout. Do not overwrite
directories, delete branches, or use force to bypass Git's branch protection.

If native allocation fails, preserve the failure; do not switch to manual Git.
If manual creation is denied, report the blocker. The upstream in-place fallback
is allowed here only if host policy and the user's established scope permit it;
otherwise keep dependent writes blocked. Never turn an isolation failure into an
unannounced write to the main checkout.

## 3. Establish setup and baseline evidence

Use repository-documented, approved setup and verification commands. Respect
lockfiles and existing prepared environments. Upstream's package-manager snippets
are examples, not authority to install dependencies, rewrite locks, execute hooks,
or choose a package manager from one filename. Run only the relevant baseline
checks and record actual commands, candidate/base, environment, exits, counts,
and raw evidence. A skipped or unavailable check is not a pass.

Baseline failures remain visible. Investigate or repair them only within existing
authority; continue with a known failure only under a recorded owner/project
disposition naming its impact. If no such decision exists, ask whether to investigate
or proceed and leave affected writes blocked. Do not silently exempt required
delivery checks. Reuse established prerequisite results so each agent does not
repeat a failed setup. Carry the baseline forward without treating it as evidence
that the later implementation passes.

Record this information using [the workspace record](../assets/workspace.md) in
the existing change evidence area. It is a handoff artifact, not another scheduler
database. Every specialist receives the exact workspace identity and assigned
working directory via [the handoff](../assets/handoff.md).

## 4. Share a change safely across roles

- Use one worktree per coherent change by default. Architecture, planning,
  implementation, test authoring, and documentation/spec edits are serialized
  writer phases. The coordinator transfers ownership through the host's existing
  claim mechanism; specialists do not create or switch worktrees themselves.
- Read-only reviewers may run together against the same frozen candidate when
  the host supports it. Reviewers do not write source or reset the checkout. Use
  host-provided snapshots/test environments when execution needs isolation.
- Additional worktrees are for independent changes or an explicitly isolated
  verification need, with separate branches, file scope and integration ownership.
  More roles alone do not justify more worktrees. Reconcile parallel changes
  through reviewed integration; rerun affected checks on the combined candidate.
- If the planning/spec store is separate, assign its own authorized workspace,
  branch and writer ownership, and preserve the code-to-store mapping at every
  OpenSpec operation. A lock in the code worktree does not protect a shared store.
- Worktrees share Git refs, configuration and often credentials. They do not
  isolate processes, ports, databases, caches, containers or secrets. Allocate
  test resources through approved tooling and enforce permissions in the host.
- Freeze the candidate during verification/review. A content change, branch move,
  rebase, merge or cherry-pick requires a fresh candidate identity and applicable
  evidence. Neither the worktree path nor unchanged HEAD proves unchanged content.

## 5. Delivery, retention and cleanup

Return path, branch or detached status, base and final candidate, baseline and
final checks, remaining work, and native workspace identity when applicable.
Retain the workspace through corrections and the requested delivery endpoint.
Record who owns later cleanup; opening a PR does not itself authorize deletion.

Use the native owner for cleanup of native workspaces. For a manually created
worktree, remove it only under the established lifecycle and authority after
confirming no agent/job uses it, all commits are durably retained as intended,
and tracked, untracked and valuable ignored artifacts have been accounted for.
Preserve separate spec-store work. Leave ambiguous or dirty workspaces intact
and report them. Do not use force removal, blanket pruning or branch deletion
to manufacture a clean handoff. Ordinary authorized cleanup needs no repeated
permission prompt; unresolved loss of work does.

The portable package describes these gates; it does not allocate or enforce them.
The evidence checker does not inspect live Git or validate workspace ownership.
Verify native binding, writer exclusion, snapshot fidelity and cleanup behavior
when adopting the package in a runtime.
