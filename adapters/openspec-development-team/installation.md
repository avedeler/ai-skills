# Pinned project installation

The [onboarding scaffold](onboarding.md) can generate a reviewed installer copy,
provenance, configuration and inert integration fragments.

The optional [installer](install.py) keeps a complete reviewed checkout and uses
its canonical adapter to render native bindings. It adds no orchestration and does
not initialize OpenSpec, launch agents, or configure credentials.

From a reviewed local checkout, copy `install.py` **byte for byte** into your
project (for example `scripts/install_team.py`). Track that copy, its source URL,
reviewed commit and SHA-256 provenance, and your configuration in version control.
The copied installer and config are the trust root. Never automatically execute an
installer fetched from upstream. Updating the installer requires reviewing and
copying it again; changing the source pin alone does not update this trusted copy.

Copy [install.example.json](install.example.json) to `.team/install.json`. Replace
the all-zero placeholder with a reviewed full lowercase 40-character Git commit
that includes the installer-compatible adapter. Copy [models.example.json](models.example.json)
to `.team/models.json` and choose available models, or omit each runtime's `models`
field to inherit host defaults. There are no provider or model defaults here.

```sh
python3 scripts/install_team.py install --project . --config .team/install.json
python3 scripts/install_team.py verify --project . --config .team/install.json
```

Optional `provenance` and `openspec` fields enable installer provenance checks
and explicit version/root observations; see [their contract](onboarding.md).

Schema version 1 requires `upstream`, `cache`, and `runtimes`. `registration` is
optional. Upstream has exactly `url` and `revision`; URLs support `https://`,
`ssh://` and local absolute `file://` fixtures (no scp spelling or ext transport).
A runtime has a unique lowercase `name`, `host` (`codex` or `opencode`), `output`,
and optional `models`. All paths are relative to `--project`, without traversal
or symlink ancestors. Cache, outputs, registration, configuration and model inputs
must not overlap; runtimes may share a model input. Unknown fields are errors.
The project itself can be a linked Git worktree; the cache must be a full detached
checkout with a real `.git` directory, no submodules or tracked symlinks.

The cache path is `<cache>/<revision>`. A fresh clone is staged, verified and then
published; an existing cache is verified offline without fetching or repairing.
The checks authenticate objects with `git fsck --full --strict` in an independent
Git directory, then compare exact tree bytes, executable modes, index entries and
flags, and all working-tree files and directories, including ignored files.
Symlinks, special files, alternates, grafts, shallow and partial stores are refused
before content reads. Cached hooks, filters, fsmonitor, config includes and fsck
severity overrides are never used. Inherited `GIT_*` variables are cleared.
Clone uses trusted Git/network transports; OS, Python, Git, SSH and host credentials
remain trusted components, and this is not a hostile-process sandbox.

Add the configured cache, generated outputs, optional generated registration link,
and `.team/installation.json`
(or `installation.json` beside a differently located config), to project ignores.
The registration link points at an absolute machine-specific cache path.
Track the installer/config/model inputs and provenance. The small generated
receipt records the registration target this installation owns. Installation
refuses foreign registrations or edited generated outputs. Change the pin to
update A to B: all runtime settings and ownership checks must pass before any
runtime write or link movement; the owned link then points at B and A is retained.
Do not update while sessions use the old checkout. Retain old caches while sessions
can resume and choose fresh output paths when preserving local edits.

`verify` checks the current cache, owned registration and exact generated bindings;
it writes nothing in the project, performs no network request, and does not repair
anything. Object verification uses temporary storage outside the project. An
invalid cache is preserved for inspection. Hard I/O failures during output writes
can leave partial writes: installation is not an atomic filesystem transaction.
Serialize writers; concurrent hostile mutation is outside this contract.

Tests use real offline Git fixtures and the canonical adapter on Linux, Python
3.12 and Git 2.52. Python 3.11+ is required. These checks do not establish universal
platform or filesystem support, model availability, native-host permissions, or
an end-to-end team pilot. See [adapter compatibility](compatibility.md).
