#!/usr/bin/env python3
"""Copy reviewed team setup into a project without modifying its integration files."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import subprocess
import sys

SOURCE = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('trusted_team_install', HERE / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def json_bytes(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def source_pin(source):
    """The operator-reviewed local source is trusted; fetched caches are not."""
    source = installer.safe_path(source)
    def git(*args):
        return installer.command(['git', '-c', 'core.fsmonitor=false', '-C', str(source), *args])
    if git('rev-parse', '--show-toplevel').decode().strip() != str(source):
        raise ValueError('source must be the complete checkout root')
    if git('status', '--porcelain', '--untracked-files=all'):
        raise ValueError('reviewed source checkout must be clean')
    pin = {'url': git('remote', 'get-url', 'origin').decode().strip(),
           'revision': git('rev-parse', 'HEAD').decode().strip()}
    installer.validate_pin(pin)
    # Consume only tracked, byte-identical HEAD files, including ignored files.
    def tracked(relative):
        path = installer.relative(source, relative)
        if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
            raise ValueError('source input must be a regular tracked file')
        data = path.read_bytes()
        if data != git('show', pin['revision'] + ':' + relative):
            raise ValueError('source input differs from reviewed HEAD')
        return data
    for required in (installer.ADAPTER, installer.PACKAGE + '/SKILL.md',
                     installer.PACKAGE + '/assets/handoff.md', 'THIRD_PARTY_NOTICES.md'):
        tracked(required)
    for dependency in ('openspec', 'using-git-worktrees'):
        for name in ('README.md', 'LICENSE', 'UPSTREAM.json'):
            tracked(installer.PACKAGE + '/third_party/' + dependency + '/' + name)
    tracked(installer.PACKAGE + '/third_party/using-git-worktrees/SKILL.md')
    return pin, tracked


def scaffold(project, *, source=SOURCE, host='codex', preset='inherit'):
    project = installer.safe_path(project)
    if not project.is_dir():
        raise ValueError('project must be an existing directory')
    if host not in ('codex', 'opencode') or preset not in ('inherit', 'codex-default', 'codex-experimental'):
        raise ValueError('invalid host or preset')
    if host != 'codex' and preset != 'inherit':
        raise ValueError('Codex presets require host codex')
    pin, tracked = source_pin(Path(source))
    code = tracked(installer.INSTALLER)
    base = 'adapters/openspec-development-team/'
    models = (tracked(base + 'presets/' + preset + '.json') if preset != 'inherit'
              else json_bytes({'schema_version': 1}))
    record = {'schema_version': 1, 'upstream': pin, 'source_path': installer.INSTALLER,
              'installed_path': 'scripts/team_install.py', 'sha256': hashlib.sha256(code).hexdigest()}
    config = {'schema_version': 1, 'upstream': pin, 'cache': '.tools/ai-skills',
              'registration': '.agents/skills/openspec-development-team',
              'provenance': '.team/installer-provenance.json',
              'runtimes': [{'name': 'default', 'host': host, 'models': '.team/models.json',
                            'output': '.tools/team-runtime/default'}]}
    setup = b'''#!/usr/bin/env bash
set -euo pipefail
team_project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$team_project_root/scripts/team_install.py" install --project "$team_project_root" --config .team/install.json "$@"
'''
    files = {'scripts/team_install.py': (code, 0o644), 'scripts/team_setup.sh': (setup, 0o755),
             '.team/install.json': (json_bytes(config), 0o644),
             '.team/installer-provenance.json': (json_bytes(record), 0o644),
             '.team/models.json': (models, 0o644)}
    for name in ('AGENTS.md', 'gitignore', 'ci.yml', 'openspec.sh', 'README.md'):
        target = '.team/README.md' if name == 'README.md' else '.team/templates/' + name
        files[target] = (tracked(base + 'project-templates/' + name), 0o644)
    # Preflight every destination before creating any parent or writing bytes.
    for name, (data, mode) in files.items():
        path = installer.relative(project, name)
        if any(p.exists() and not p.is_dir() for p in path.parents):
            raise ValueError(f'non-directory destination ancestor: {name}')
        if path.exists():
            if not stat.S_ISREG(path.stat().st_mode) or path.read_bytes() != data or stat.S_IMODE(path.stat().st_mode) != mode:
                raise ValueError(f'conflicting scaffold destination: {name}')
    for name, (data, mode) in files.items():
        path = project / name
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            path.chmod(mode)
    return pin


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--host', choices=('codex', 'opencode'), default='codex')
    parser.add_argument('--preset', choices=('inherit', 'codex-default', 'codex-experimental'), default='inherit')
    args = parser.parse_args(argv)
    try:
        pin = scaffold(args.project, host=args.host, preset=args.preset)
        print(f'Scaffolded reviewed source {pin["revision"]}. Manual integration required:')
        print('Review .team/README.md and integrate .team/templates into existing instructions, ignores and CI.')
        print('Preserve/discover the existing OpenSpec wrapper, schema and store; then run bash scripts/team_setup.sh.')
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
