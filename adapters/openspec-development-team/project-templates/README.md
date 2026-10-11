# Project team setup

Review and integrate the inert fragments in `.team/templates/` into the existing
project instructions, ignore rules and CI. Review the OpenSpec wrapper example
against the project's existing pinned wrapper; discover and preserve its version,
schema and planning store. No fragment is activated automatically. Fill project
facts in the instructions; no build/test commands are guessed.

Keep `scripts/team_install.py`, `.team/install.json`, `.team/models.json`, and
`.team/installer-provenance.json` tracked. Ignore generated `.tools/` state,
`.team/installation.json`, and the absolute machine-specific skill registration
link as described by the ignore fragment. Then run:

```sh
bash scripts/team_setup.sh
python3 scripts/team_install.py verify --project . --config .team/install.json
```

Setup verifies a full pinned checkout, registers the skill and renders bindings.
Default verification is offline and writes nothing in the project. It checks
source objects/notices, model settings, shared prompt references, installer
provenance and exact native bindings; it does not run a live agent team.

Native Codex CLI users can explicitly add `--native-codex` to verify configuration
loading without inference. For an existing project wrapper, optionally add
`"openspec": {"command": ["scripts/openspec.sh"], "root": "openspec", "version": "YOUR_REVIEWED_EXACT_VERSION"}`
to the install config (the reviewed wrapper must be executable) and verify with `--check-openspec`. This invokes the trusted
wrapper with `--version` and checks its existing root. It does not infer the schema
or synchronize/initialize specs. Separate planning stores need manual integration.
These opt-in diagnostics can run project/native tools and may have their own side effects.

The installer copy and provenance are reviewed trust inputs, not publisher
signatures. Change `upstream.revision` only to a reviewed full commit; a pin update
keeps the earlier installer provenance until its separate reviewed upgrade. Never
execute an automatically fetched installer. Preserve old caches while sessions
can resume. Review and copy updated installer bytes/provenance explicitly.

After filling project facts, start a supervised feature run:

> Use the shared development team for this approved feature. Inspect architecture
> and our existing OpenSpec workflow first; implement within the assigned
> workspace, run required checks, obtain independent code/security review, and
> synchronize documentation/specs. Deliver a review-ready PR. Merge and deployment
> remain mine.


For a local native CLI launch after verification, derive the pin and runtime from
config:

```sh
python3 - <<'PYTHON'
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
PYTHON
```

In a cloud dashboard, manually configure `bash scripts/team_setup.sh` as the setup
script and restart/recreate the workspace as the host requires. Setup does not
activate a dashboard workflow or reconfigure an already running root model.
