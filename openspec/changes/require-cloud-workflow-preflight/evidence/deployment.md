# Source-pinned workspace acceptance

Reviewed implementation commit:
`c1b33afbbd08dc319c716a62b81c59dccb008b0f`.
Draft delivery: [PR #7](https://github.com/avedeler/ai-skills/pull/7).

## Actual checks on 2026-10-18

- The concrete setup script pins that full commit and clones into a versioned
  tools directory, preserving the existing source checkout and command link.
- Fresh OpenSpec 1.14.3 installation into a staged versioned prefix succeeded:
  57 packages installed; dependency audit reported zero vulnerabilities. A
  full-tree receipt was checked before reusing the published tool prefix.
- Router/profile installation, development-team content verification and managed
  workspace AGENTS installation passed. Existing development-team instructions
  were retained after matching reviewed content; only generated Python caches
  were excluded from that content comparison.
- Real CLI preflight used the installed adapter/executable and selected this
  project/change. It returned the actual planning root, selected change and
  `state: ready` before the final tracked tasks were marked complete.
- The same pinned setup ran again successfully without reinstalling packages;
  dependency audit again reported zero vulnerabilities. All eight captured
  managed instruction/router/receipt file hashes remained unchanged.
- Thirteen no-network bootstrap controls passed, preserving customized prefixes,
  special metadata nodes, live/dangling ancestor/source/prefix/AGENTS/command
  links and custom commands. Git/npm stubs proved network phases were not reached.
- Bash syntax passed. ShellCheck was unavailable. Dedicated security review
  passed the bootstrap including special-node checks before metadata reads.
- The running session's executor skill-list API returned no entries. Explicit
  installed paths in AGENTS are therefore essential; neither that current-session
  observation nor file installation proves a fresh hosted task discovers policy.

The concrete setup script was prepared in the selected workspace for the owner
to copy into the environment setup configuration. Its SHA-256 was
`d296b2afa3c1c0c42acd6013ee93e33f9508cf44d6bea42b265f5e04289a0676`.
The original setup script was preserved separately. These local files do not
update the server's saved environment configuration.

## Remaining environment acceptance

1. Review the concrete pinned setup script in the environment configuration
   workflow and publish/republish the environment. The available environment
   connector is read-only; no configuration publication occurred in this session.
2. Start a fresh task in the published environment. Select the preferred root
   model/effort through supported session controls (the supplied profile requests
   Sol 6.1 high); installed files cannot switch an active root model.
3. Without explicitly invoking the router in the prompt, request a small scoped
   code change. Confirm startup loads AGENTS, router/profile and development-team;
   actual OpenSpec context/apply prerequisites are inspected before code changes;
   useful delegation sends explicit supported model/effort with fresh context;
   and unavailable capabilities produce an explicit fallback or blocker.
4. Check installed verification and selected-project preflight again. Keep actual
   request acceptance separate from effective model identity when not exposed.

Instructions make the workflow required and inspectable. They do not intercept
all native tool calls or provide filesystem isolation. No environment publication,
merge, production change or archive has occurred. The final source follow-up only
records acceptance/task receipts; it does not change the pinned adapter packages.
