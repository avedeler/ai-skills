# Project onboarding

Use a reviewed **clean, complete local checkout** of this repository. The scaffold
records its actual `HEAD` and `origin`; it does not fetch or resolve a moving branch.
An attached source branch is supported. The reviewed source and its Git config are
trusted. Cleanliness is checked with Git status; every consumed file is also
compared byte for byte with its tracked HEAD blob. Ignored extras are not consumed.
Fetched installation caches use the stronger independent integrity checks in the
[pinned installer](installation.md).

From the reviewed checkout:

```sh
python3 adapters/openspec-development-team/scaffold.py --project /path/to/project
```

The default host is Codex and the default preset is `inherit`, with no model
selection imposed. `--host opencode` also inherits. Codex users may explicitly
select `--preset codex-default` or `--preset codex-experimental`; see the reviewed
[preset settings](presets/codex-default.json) and
[experimental settings](presets/codex-experimental.json). Experimental changes
only the implementer to `gpt-6-luna` with `high` effort. These are optional requested
model settings, not core prompts, availability promises or quality guarantees.

The scaffold creates `scripts/team_install.py` as an exact canonical byte copy,
`scripts/team_setup.sh`, tracked install/model/provenance inputs, `.team/README.md`
and inert integration fragments under `.team/templates/`. It checks every
potential destination before writing, allows identical repeats, and refuses
conflicting files, symlinks, special files or blocked ancestors. It preserves
existing project instructions, CI, ignores, manifests and OpenSpec integration.
Hard I/O failures are not an atomic filesystem transaction; serialize writers.

Review the generated guide, fill its project facts and manually integrate the
instruction/ignore/CI fragments. Preserve the project's existing OpenSpec wrapper,
version, schema and planning store. The wrapper fragment uses only a locally pinned
`node_modules/.bin/openspec`, disables telemetry, and keeps its config project-local;
it does not install dependencies, initialize specs or edit global configuration.
If a fresh initialization is needed, explicitly choose a reviewed version, inspect
its upstream help and current security audit, then perform setup within the user's existing authorization. No fixed vulnerable version or audit waiver is supplied here.

After integration, run in the project:

```sh
bash scripts/team_setup.sh
python3 scripts/team_install.py verify --project . --config .team/install.json
```

Setup completion means the pinned checkout, skill registration and static bindings
are available. It does not activate a cloud dashboard workflow or establish a live
pilot. Track config/model/provenance and the copied installer; ignore `.tools/`,
`.team/installation.json` and the generated absolute skill registration link.

Optional `provenance` in the installer config points to a schema-1 record with
`upstream` URL/revision, canonical `source_path`, project `installed_path` and
`sha256`. Default verification checks installed bytes against this reviewed trust
input. It is not publisher authentication. When provenance and current source pin
match, verification also compares canonical pinned installer bytes. A later pin
update can keep old installer provenance without retaining its old checkout;
upgrading the installer itself requires separately reviewed bytes and provenance.

Static verification authenticates checkout objects/notices, validates model
settings and shared prompt references, and compares rendered bindings exactly.
Codex bindings are valid TOML; OpenCode bindings are generated JSON. To observe
native Codex configuration loading without requesting inference:

```sh
python3 scripts/team_install.py verify --project . --config .team/install.json --native-codex
```

This invokes `codex --cd ... -c ... features list` using the canonical adapter's
TOML assignments. It establishes loader acceptance, not agent discovery, account
entitlement or executed model identity. OpenCode has static checks here; a native
observation is not claimed.

For an existing pinned executable project wrapper, optional config can include:

```json
{
  "openspec": {
    "command": ["scripts/openspec.sh"],
    "root": "openspec",
    "version": "YOUR_REVIEWED_EXACT_VERSION"
  }
}
```

Add this field to the existing install object, then explicitly use
`verify --project . --config .team/install.json --check-openspec`. It passes literal
arguments plus `--version`, compares the exact returned line and checks that the
configured project-relative root exists. It does not infer the wrapper's actual
planning context, schema or synchronization operations. Separate external planning
stores need manual integration through the repository's existing workflow.
Default verification is offline and writes nothing in the project; these opt-in
diagnostics run trusted project/native tools that may have their own side effects.

For a local native CLI session, derive the current adapter and output paths from
config rather than hardcoding a revision:

```sh
python3 - <<'PY'
import json, subprocess, sys
from pathlib import Path
root = Path.cwd()
config = json.loads((root / '.team/install.json').read_text())
runtime = config['runtimes'][0]
cache = root / config['cache'] / config['upstream']['revision']
args = [sys.executable, str(cache / 'adapters/openspec-development-team/adapter.py'),
        'run', '--host', runtime['host'], '--output', str(root / runtime['output']),
        '--project', str(root), '--task',
        'Use the shared team for the approved feature. Inspect architecture and existing OpenSpec first; implement, test, review and synchronize docs/specs. Deliver a review-ready PR; merge and deployment remain mine.']
if 'models' in runtime:
    args += ['--models', str(root / runtime['models'])]
subprocess.run(args, check=True)
PY
```

Run static verification first. Inspect required project checks before the first
feature. See [cloud integration](cloud.md) for hosted-session limits and manual
dashboard setup.
