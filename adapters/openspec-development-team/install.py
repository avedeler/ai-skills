#!/usr/bin/env python3
"""Install or verify a reviewed, pinned full checkout. Python 3.11+, stdlib only."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
from urllib.parse import urlsplit

PACKAGE = 'skills/openspec-development-team'
ADAPTER = 'adapters/openspec-development-team/adapter.py'
INSTALLER = 'adapters/openspec-development-team/install.py'


def command(args, *, cwd=None, env=None):
    environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0', GIT_NO_REPLACE_OBJECTS='1')
    if env:
        environment.update(env)
    return subprocess.run(args, cwd=cwd, env=environment, check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120).stdout


def git(directory, *args, index=None):
    return command(['git', '--no-replace-objects', '--git-dir', str(directory),
                    '-c', 'core.hooksPath=' + os.devnull, '-c', 'core.fsmonitor=false', *args],
                   env={'GIT_INDEX_FILE': str(index)} if index else None)


def safe_path(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f'symlink path refused: {path}')
    return path


def relative(project, value, *, allow_link=False):
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        raise ValueError('paths must be nonempty strings')
    path = Path(value)
    if path.is_absolute() or '..' in path.parts or not path.parts or '\\' in value:
        raise ValueError('paths must be project-relative without traversal')
    result = project / path
    if allow_link:
        safe_path(result.parent)
        return result
    return safe_path(result)


def keys(value, allowed, required):
    if not isinstance(value, dict) or set(value) - set(allowed) or set(required) - set(value):
        raise ValueError('unknown or missing configuration fields')


def validate_pin(pin):
    keys(pin, ('url', 'revision'), ('url', 'revision'))
    if not isinstance(pin['revision'], str) or not re.fullmatch('[0-9a-f]{40}', pin['revision']):
        raise ValueError('revision must be a full lowercase 40-character commit')
    url = pin['url']
    if not isinstance(url, str) or any(ord(c) < 32 for c in url):
        raise ValueError('invalid upstream URL')
    parsed = urlsplit(url)
    if parsed.scheme not in ('https', 'ssh', 'file') or (parsed.scheme != 'file' and not parsed.hostname):
        raise ValueError('use an https://, ssh:// or file:// upstream URL')
    if parsed.scheme == 'file' and (parsed.netloc not in ('', 'localhost') or not parsed.path.startswith('/')):
        raise ValueError('file URL must name a local absolute path')


def load_config(project, config):
    if not config.is_file() or not stat.S_ISREG(config.stat().st_mode):
        raise ValueError('config must be a regular file')
    value = json.loads(config.read_text(encoding='utf-8'))
    keys(value, ('schema_version', 'upstream', 'cache', 'registration', 'runtimes', 'provenance', 'openspec'),
         ('schema_version', 'upstream', 'cache', 'runtimes'))
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ValueError('schema_version must be 1')
    pin = value['upstream']
    validate_pin(pin)
    cache_parent = relative(project, value['cache'])
    cache = cache_parent / pin['revision']
    registration = relative(project, value['registration'], allow_link=True) if 'registration' in value else None
    if not isinstance(value['runtimes'], list):
        raise ValueError('runtimes must be a list')
    runtimes = []
    names = set()
    paths = [cache_parent, config, config.with_name('installation.json')]
    if registration:
        paths.append(registration)
    for runtime in value['runtimes']:
        keys(runtime, ('name', 'host', 'models', 'output'), ('name', 'host', 'output'))
        name = runtime['name']
        if not isinstance(name, str) or not re.fullmatch('[a-z][a-z0-9-]*', name) or name in names:
            raise ValueError('runtime names must be unique lowercase identifiers')
        names.add(name)
        if runtime['host'] not in ('codex', 'opencode'):
            raise ValueError('host must be codex or opencode')
        item = dict(runtime, output=relative(project, runtime['output']))
        if 'models' in runtime:
            item['models'] = relative(project, runtime['models'])
            if not item['models'].is_file() or not stat.S_ISREG(item['models'].stat().st_mode):
                raise ValueError('models must be a regular file')
            if item['models'] not in paths:
                paths.append(item['models'])
        paths.append(item['output'])
        runtimes.append(item)
    if 'provenance' in value:
        provenance = relative(project, value['provenance'])
        record, installed = provenance_record(project, provenance)
        paths.extend((provenance, installed))
    if 'openspec' in value:
        observation = value['openspec']
        keys(observation, ('command', 'root', 'version'), ('command', 'root', 'version'))
        args = observation['command']
        if not isinstance(args, list) or not args or any(
                not isinstance(arg, str) or not arg or any(ord(c) < 32 for c in arg) for arg in args):
            raise ValueError('OpenSpec command must be a nonempty literal argument list')
        paths.extend((relative(project, args[0]), relative(project, observation['root'])))
        if not isinstance(observation['version'], str) or not observation['version'].strip() or any(
                ord(c) < 32 for c in observation['version']):
            raise ValueError('OpenSpec version must be an exact nonempty line')
    for i, path in enumerate(paths):
        for other in paths[i + 1:]:
            if path == other or path.is_relative_to(other) or other.is_relative_to(path):
                raise ValueError('configuration paths must not overlap')
    return pin, cache_parent, cache, registration, runtimes


def provenance_record(project, path):
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError('provenance must be a regular file')
    record = json.loads(path.read_text())
    keys(record, ('schema_version', 'upstream', 'source_path', 'installed_path', 'sha256'),
         ('schema_version', 'upstream', 'source_path', 'installed_path', 'sha256'))
    if type(record['schema_version']) is not int or record['schema_version'] != 1:
        raise ValueError('provenance schema_version must be 1')
    validate_pin(record['upstream'])
    if record['source_path'] != INSTALLER:
        raise ValueError('provenance must identify the canonical installer source path')
    installed = relative(project, record['installed_path'])
    if not isinstance(record['sha256'], str) or not re.fullmatch('[0-9a-f]{64}', record['sha256']):
        raise ValueError('provenance sha256 must be a full lowercase digest')
    if not installed.is_file() or not stat.S_ISREG(installed.stat().st_mode):
        raise ValueError('installed installer must be a regular file')
    if hashlib.sha256(installed.read_bytes()).hexdigest() != record['sha256']:
        raise ValueError('installed installer differs from reviewed provenance hash')
    return record, installed


def inventory(root):
    """Reject links and special files before reading any cache content."""
    safe_path(root)
    if not root.is_dir() or not (root / '.git').is_dir():
        raise ValueError('cache must have a real .git directory')
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(directory) / name
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                raise ValueError(f'unsupported cache entry: {path}')
    metadata = root / '.git'
    for name in ('objects/info/alternates', 'objects/info/http-alternates', 'info/grafts', 'shallow'):
        if (metadata / name).exists():
            raise ValueError(f'unsupported Git metadata: {name}')
    if any(metadata.rglob('*.promisor')):
        raise ValueError('partial object store refused')


def verify_checkout(cache, pin):
    inventory(cache)
    metadata = cache / '.git'
    if (metadata / 'HEAD').read_text().strip() != pin['revision']:
        raise ValueError('cache HEAD differs from pinned detached revision')
    def config_value(*args):
        return command(['git', 'config', '--no-includes', '--file', str(metadata / 'config'), *args])
    if config_value('--get', 'remote.origin.url').decode().strip() != pin['url']:
        raise ValueError('cache origin differs from declared URL')
    settings = config_value('--list', '-z').lower().split(b'\0')
    if any(b'partialclone' in item.split(b'\n', 1)[0]
           or item.split(b'\n', 1)[0].endswith(b'.promisor') for item in settings):
        raise ValueError('partial clone configuration refused')
    # Only object bytes enter this independent Git repository. Cached config can
    # neither weaken fsck nor invoke helpers, hooks, filters, includes or lazy fetch.
    with tempfile.TemporaryDirectory(prefix='team-object-check-') as temporary:
        controlled = Path(temporary) / 'git'
        command(['git', '-c', 'init.templateDir=', 'init', '--bare', str(controlled)])
        shutil.copytree(metadata / 'objects', controlled / 'objects', dirs_exist_ok=True)
        git(controlled, 'fsck', '--full', '--strict', pin['revision'])
        if git(controlled, 'cat-file', '-t', pin['revision']).strip() != b'commit':
            raise ValueError('pin must identify a commit')
        expected, expected_index, directories = set(), set(), set()
        for entry in git(controlled, 'ls-tree', '-rz', '--full-tree', pin['revision']).split(b'\0'):
            if not entry:
                continue
            metadata_entry, name = entry.split(b'\t', 1)
            mode, kind, oid = metadata_entry.split()
            path = cache / os.fsdecode(name)
            if kind != b'blob' or mode not in (b'100644', b'100755'):
                raise ValueError('unsupported upstream tree entry')
            safe_path(path)
            if not path.is_file() or path.read_bytes() != git(controlled, 'cat-file', 'blob', oid.decode()):
                raise ValueError(f'tracked bytes differ: {path}')
            if bool(path.stat().st_mode & stat.S_IXUSR) != (mode == b'100755'):
                raise ValueError('tracked executable mode differs')
            expected.add(path.relative_to(cache).as_posix())
            expected_index.add(mode + b' ' + oid + b' 0\t' + name)
            directories.update(p.relative_to(cache).as_posix() for p in path.parents if cache in p.parents)
        if set(git(controlled, 'ls-files', '--stage', '-z', index=cache / '.git/index').split(b'\0')) - {b''} != expected_index:
            raise ValueError('cache index differs from pinned tree')
        debug = git(controlled, 'ls-files', '--debug', index=cache / '.git/index')
        if any(flag != b'0' for flag in re.findall(rb'flags: ([0-9a-f]+)', debug)):
            raise ValueError('cache index flags differ')
        present = set()
        for directory, dirs, files in os.walk(cache):
            if Path(directory) == cache:
                dirs.remove('.git')
            for name in dirs:
                if (Path(directory) / name).relative_to(cache).as_posix() not in directories:
                    raise ValueError('extra cache directory')
            present.update((Path(directory) / name).relative_to(cache).as_posix() for name in files)
        if present != expected:
            raise ValueError('cache inventory differs from pinned tree')
        required = {ADAPTER, PACKAGE + '/SKILL.md', PACKAGE + '/assets/handoff.md',
                    'THIRD_PARTY_NOTICES.md'}
        for dependency in ('openspec', 'using-git-worktrees'):
            required.update(PACKAGE + '/third_party/' + dependency + '/' + name
                            for name in ('README.md', 'LICENSE', 'UPSTREAM.json'))
        required.add(PACKAGE + '/third_party/using-git-worktrees/SKILL.md')
        if not required <= expected:
            raise ValueError('missing canonical source or notices')


def adapter_for(cache):
    spec = importlib.util.spec_from_file_location('pinned_team_adapter', cache / ADAPTER)
    module = importlib.util.module_from_spec(spec)
    # Suppress bytecode writes into the immutable verified cache.
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def install(project, config, action='install'):
    project = safe_path(project)
    if not project.is_dir():
        raise ValueError('project must be an existing directory')
    config = relative(project, config)
    pin, parent, cache, registration, runtimes = load_config(project, config)
    if not cache.exists():
        if action == 'verify':
            raise ValueError('pinned cache is missing')
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.clone-', dir=parent) as temporary:
            staging = Path(temporary) / 'checkout'
            command(['git', '-c', 'core.hooksPath=' + os.devnull, '-c', 'init.templateDir=',
                     '-c', 'protocol.allow=never', '-c', 'protocol.https.allow=always',
                     '-c', 'protocol.ssh.allow=always', '-c', 'protocol.file.allow=always',
                     'clone', '--no-checkout', '--no-local', '--', pin['url'], str(staging)])
            # Fresh clone config and objects were produced by trusted Git, not a
            # cached helper. Disable filters/hooks and inherited config on checkout.
            command(['git', '-c', 'core.hooksPath=' + os.devnull, '-c', 'core.fsmonitor=false',
                     '-C', str(staging), 'checkout', '--detach', pin['revision']])
            verify_checkout(staging, pin)
            staging.rename(cache)
    verify_checkout(cache, pin)
    configured = json.loads(config.read_text())
    if 'provenance' in configured:
        record, installed = provenance_record(project, relative(project, configured['provenance']))
        if record['upstream'] == pin and installed.read_bytes() != (cache / INSTALLER).read_bytes():
            raise ValueError('installer provenance differs from canonical pinned source bytes')
    package = cache / PACKAGE
    receipt_path = config.with_name('installation.json')
    safe_path(receipt_path)
    if receipt_path.exists() and not stat.S_ISREG(receipt_path.stat().st_mode):
        raise ValueError('receipt must be a regular file')
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    if registration:
        safe_path(registration.parent)
        if any(path.exists() and not path.is_dir() for path in registration.parents):
            raise ValueError('registration has a non-directory ancestor')
        if registration.is_symlink():
            target = os.readlink(registration)
            target_path = Path(target)
            # PACKAGE spans two path segments; compare the whole allowed layout.
            revision = target_path.parent.parent.name
            owned_target = (re.fullmatch('[0-9a-f]{40}', revision) is not None
                            and target_path == parent / revision / PACKAGE)
            owned = (owned_target and isinstance(receipt, dict) and receipt.get('schema_version') == 1
                     and receipt.get('registration') == str(registration)
                     and receipt.get('target') == target)
            if not owned:
                raise ValueError('foreign skill registration refused')
        elif registration.exists():
            raise ValueError('existing skill registration refused')
        elif action == 'verify':
            raise ValueError('skill registration missing')
    adapter = adapter_for(cache)
    if not callable(getattr(adapter, 'preflight_generated', None)):
        raise ValueError('pinned adapter is incompatible: callable preflight_generated is required')
    team = adapter.load_team(package)
    plans = []
    for runtime in runtimes:
        models = adapter.load_models(runtime.get('models'), team)
        files = adapter.render(runtime['host'], package, runtime['output'], team, models)
        adapter.preflight_generated(runtime['output'], runtime['host'], files)
        if action == 'verify':
            if not runtime['output'].is_dir():
                raise ValueError('runtime output missing')
            for name, content in files.items():
                if (runtime['output'] / name).read_bytes() != content.encode():
                    raise ValueError('runtime differs from current configuration')
        plans.append((runtime, files))
    if action == 'verify':
        if registration and os.readlink(registration) != str(package):
            raise ValueError('registration does not target current pin')
        return cache
    for runtime, files in plans:
        adapter.write_generated(runtime['output'], runtime['host'], package, files)
    if registration:
        registration.parent.mkdir(parents=True, exist_ok=True)
        if registration.is_symlink():
            registration.unlink()
        registration.symlink_to(package, target_is_directory=True)
        receipt_path.write_text(json.dumps({'schema_version': 1, 'registration': str(registration),
                                           'target': str(package)}, indent=2) + '\n')
    return cache


def observations(project, config, cache, *, native_codex=False, check_openspec=False):
    """Explicit trusted-tool diagnostics, after the default static verification."""
    project = safe_path(project)
    configured = json.loads(relative(project, config).read_text())
    if native_codex:
        adapter = adapter_for(cache)
        codex = [runtime for runtime in configured['runtimes'] if runtime['host'] == 'codex']
        if not codex:
            raise ValueError('native Codex observation requires a configured Codex runtime')
        for runtime in codex:
            output = relative(project, runtime['output'])
            settings = tomllib.loads((output / 'config.toml').read_text())
            args = ['codex', '--cd', str(project)]
            for assignment in adapter.toml_assignments(settings):
                args.extend(('-c', assignment))
            command([*args, 'features', 'list'], cwd=project)
        print('PASS: native Codex configuration loader; no inference requested')
    if check_openspec:
        if 'openspec' not in configured:
            raise ValueError('OpenSpec observation requires configured command, root and version')
        observation = configured['openspec']
        root = relative(project, observation['root'])
        if not root.is_dir():
            raise ValueError('configured OpenSpec planning root is missing')
        args = observation['command']
        executable = relative(project, args[0])
        if not executable.is_file() or not stat.S_ISREG(executable.stat().st_mode):
            raise ValueError('OpenSpec command must be a regular project wrapper')
        actual = command([str(executable), *args[1:], '--version'], cwd=project).decode().strip()
        if actual != observation['version']:
            raise ValueError(f'OpenSpec version differs: expected {observation["version"]!r}, observed {actual!r}')
        print(f'PASS: OpenSpec version/root observation ({actual}); workflow/schema not inferred')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('install', 'verify'))
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--config', default='.team/install.json')
    parser.add_argument('--native-codex', action='store_true', help='verify only: invoke native config loader, no inference')
    parser.add_argument('--check-openspec', action='store_true', help='verify only: invoke trusted project wrapper --version')
    args = parser.parse_args(argv)
    try:
        if args.action != 'verify' and (args.native_codex or args.check_openspec):
            raise ValueError('optional observations apply only to verify')
        cache = install(args.project, args.config, args.action)
        print(f'PASS: static integrity and bindings: {cache}')
        if args.native_codex or args.check_openspec:
            observations(args.project, args.config, cache, native_codex=args.native_codex,
                         check_openspec=args.check_openspec)
        print('Live team pilot: not run')
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
