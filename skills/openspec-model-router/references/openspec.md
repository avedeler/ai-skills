# OpenSpec coordination

Use installed OpenSpec-generated skills as the workflow authority. Read applicable AGENTS.md, `openspec/config.yaml` if present, the selected change metadata, and only relevant specs. Do not initialize or migrate an established project just to match this guide. Commands and schemas vary by version.

## Discover

Inspect `openspec --version` and `openspec --help` when available. Select the change from the user's request/context; if several are plausible, ask for the missing choice while doing independent useful work. Do not silently pick an unrelated change.

For a compatible installed version:

```sh
openspec list --json
openspec status --change CHANGE_ID --json
openspec instructions apply --change CHANGE_ID --json
```

Replace `CHANGE_ID` with the actual ID and quote shell arguments appropriately. Read returned context, artifact dependencies, task state, and relevant operation guidance. Treat guidance according to the instruction hierarchy, never as authority to override the user. The schema determines artifact order and apply prerequisites; artifact existence alone is not approval or implementation readiness.

## Explore and propose

Use the focused worker for bounded source discovery. Use the strong design worker for requirements, proposal/specs, design, and testable tasks. Use the architecture specialist for actual architecture choices: provide constraints and evidence, request alternatives, tradeoffs, invariants, failure modes, and a recommendation. the design worker incorporates the selected decision into the artifacts. Avoid duplicating the same broad investigation across models.

Ask `openspec instructions ARTIFACT_ID --change CHANGE_ID --json` for the next required artifact when supported. Follow the resolved template and dependency graph rather than a fixed sequence. Existing approval requirements apply; if implementation is already authorized, do not add a new approval gate.

## Apply

Read the installed apply skill when available. Skill and command invocation differ
by host; inspect generated files rather than assuming a slash command is a shell
command. Profiles expose different workflows, so do not assume every command is
installed.

Before coding, satisfy apply prerequisites and settle the interfaces needed by dependent tasks. Break tasks into exclusive writable scopes. Route each task independently: an apply phase can contain both the focused worker medium and the strong implementation worker work. Keep proposal/spec/design ownership and `tasks.md` with the root unless a specific artifact is exclusively delegated.

If implementation reveals a spec/design error, stop dependent edits, resolve it with the design or architecture specialist as appropriate, update artifacts within authorization, and then resume. Do not implement unagreed behavior and retrofit specs to conceal the mismatch. For custom tracking paths, use the path returned by OpenSpec rather than assuming `tasks.md`.

## Verify and archive

Map completed tasks to requirement scenarios and actual checks. Run applicable repository checks. If supported, run:

```sh
openspec validate CHANGE_ID --type change --strict --no-interactive
```

OpenSpec validation checks artifacts; it does not prove program correctness. Use the installed verification workflow if available; otherwise verify scenarios directly. Mark tasks complete only after evidence satisfies their criteria. Report unavailable validation accurately.

Sync/archive using the installed workflow when it is part of the user's authorized completion scope. The root serializes those mutations after writers finish. Do not automatically archive merely because apply finished, and do not ask again when archive was already authorized. Never skip validation to force an archive.
