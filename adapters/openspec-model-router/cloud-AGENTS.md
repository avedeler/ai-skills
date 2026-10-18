<!-- BEGIN MANAGED OPENSPEC CLOUD WORKFLOW -->
## OpenSpec workflow startup

Before any delegation, including read-only or cross-repository analysis, read `{{MODEL_ROUTER_SKILL}}` and its installed model profile/runtime references.

For software-change workflows, also read `{{DEVELOPMENT_TEAM_SKILL}}` and its lifecycle, testing, security, and worktree references. Before code changes, run the environment verification and selected-project preflight commands below:

```sh
python3 {{CLOUD_SCRIPT}} verify --workspace {{WORKSPACE_ARG}} --skills-dir {{SKILLS_DIR}} --openspec-command {{OPENSPEC_COMMAND}} --openspec-version {{OPENSPEC_VERSION}}
python3 {{CLOUD_SCRIPT}} preflight --workspace {{WORKSPACE_ARG}} --skills-dir {{SKILLS_DIR}} --openspec-command {{OPENSPEC_COMMAND}} --openspec-version {{OPENSPEC_VERSION}} --project /path/to/selected/project --phase apply --change CHANGE_ID
```

Replace project and change with the actual selected project and change. When that project uses a separate wrapper or CLI version, add `--project-openspec-command` and `--project-openspec-version`; these checks run after verifying the installed environment CLI. Explore-only software work may use `--phase explore` and omit `--change`. Generic noncoding or read-only analysis does not require selecting an OpenSpec change or running apply preflight. Trivial documentation work may follow the repository's documented exception. Discover the software project's actual OpenSpec root, wrapper, schema, change, and generated workflow instructions before code changes. Preserve its selected planning store; never initialize or migrate a project as a startup shortcut. Delegate only when a scoped worker adds value, give each delegated task an explicitly supported model and reasoning effort, use fresh-context delegation (`fork_turns: none`) when the host requires it, and record requested settings and the host's returned settings. If the requested model or effort is unsupported, explicitly record the supported fallback or report the task blocked; never silently inherit settings. Keep independent review separate from implementation. Do not claim a model ran unless the host confirms it. Instructions cannot enforce tool calls or change the active root model.

Workspace: {{WORKSPACE_DISPLAY}}
<!-- END MANAGED OPENSPEC CLOUD WORKFLOW -->
