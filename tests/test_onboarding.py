"""Offline onboarding fixtures built from this repository, without external services."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from test_install import ROOT, git, setup, snapshot

spec = importlib.util.spec_from_file_location('team_scaffold', ROOT / 'adapters/openspec-development-team/scaffold.py')
scaffold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scaffold)


def tree_snapshot(path):
    result = snapshot(path)
    result.update({str(p.relative_to(path)): ('directory' if p.is_dir() else 'special', p.lstat().st_mode)
                   for p in path.rglob('*') if not p.is_symlink() and not stat.S_ISREG(p.lstat().st_mode)})
    return result


class OnboardingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='onboarding source ')
        cls.source = Path(cls.fixture.name) / 'source'
        cls.source.mkdir()
        for name in ('skills', 'adapters'):
            shutil.copytree(ROOT / name, cls.source / name, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT / 'THIRD_PARTY_NOTICES.md', cls.source)
        git(cls.source, 'init')
        git(cls.source, 'config', 'user.name', 'Fixture')
        git(cls.source, 'config', 'user.email', 'fixture@example.invalid')
        git(cls.source, 'remote', 'add', 'origin', cls.source.as_uri())
        git(cls.source, 'add', '.')
        git(cls.source, 'commit', '-m', 'Synthetic reviewed onboarding source')
        cls.pin = git(cls.source, 'rev-parse', 'HEAD')

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project ; $(literal) space ')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def scaffold(self, **kwargs):
        return scaffold.scaffold(self.project, source=self.source, **kwargs)

    def config(self):
        return json.loads((self.project / '.team/install.json').read_text())

    def save(self, value):
        (self.project / '.team/install.json').write_text(json.dumps(value))

    def install(self, action='install'):
        return setup.install(self.project, '.team/install.json', action)

    def test_scaffold_preserves_project_and_repeats_exactly(self):
        originals = {'AGENTS.md': 'existing instructions', '.gitignore': 'existing ignore',
                     '.github/workflows/ci.yml': 'existing CI', 'openspec/config.yaml': 'existing schema',
                     'package.json': 'existing manifest', 'scripts/openspec.sh': 'existing wrapper'}
        for name, content in originals.items():
            path = self.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.scaffold()
        before = snapshot(self.project)
        self.scaffold()
        self.assertEqual(before, snapshot(self.project))
        for name, content in originals.items():
            self.assertEqual((self.project / name).read_text(), content)
        self.assertEqual(self.config()['upstream']['revision'], self.pin)
        self.assertEqual((self.project / 'scripts/team_install.py').read_bytes(),
                         (self.source / setup.INSTALLER).read_bytes())
        provenance = json.loads((self.project / '.team/installer-provenance.json').read_text())
        self.assertEqual(provenance['source_path'], setup.INSTALLER)
        self.assertEqual(provenance['upstream'], self.config()['upstream'])
        self.assertFalse(any(self.source.rglob('__pycache__')))

    def test_setup_script_repeat_and_default_offline_verify(self):
        self.scaffold()
        command = ['bash', str(self.project / 'scripts/team_setup.sh')]
        subprocess.run(command, cwd='/', check=True, capture_output=True)
        before = snapshot(self.project)
        subprocess.run(command, cwd='/', check=True, capture_output=True)
        subprocess.run(['python3', str(self.project / 'scripts/team_install.py'), 'verify',
                        '--project', str(self.project)], cwd='/', check=True, capture_output=True)
        self.assertEqual(before, snapshot(self.project))

    def test_setup_wrapper_literal_forwarding_and_exit_status(self):
        self.scaffold()
        binary = self.project / 'fake-bin/python3'
        binary.parent.mkdir()
        binary.write_text('#!/usr/bin/python3\nimport json,sys\nprint(json.dumps(sys.argv[1:]))\nraise SystemExit(7)\n')
        binary.chmod(0o755)
        literal = 'space; $(touch injected) `touch injected`'
        with patch.dict(os.environ, {'PATH': str(binary.parent) + os.pathsep + os.environ['PATH']}):
            result = subprocess.run(['bash', str(self.project / 'scripts/team_setup.sh'), literal],
                                    cwd='/', capture_output=True, text=True)
        self.assertEqual(result.returncode, 7)
        args = json.loads(result.stdout)
        self.assertEqual(args, [str(self.project / 'scripts/team_install.py'), 'install',
                                '--project', str(self.project), '--config', '.team/install.json', literal])
        self.assertFalse((self.project / 'injected').exists())

    def test_all_destination_collisions_preflight(self):
        cases = ('scripts-ancestor', 'late-file', 'late-dir', 'late-link', 'late-fifo')
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                self.project = Path(temporary)
                if case == 'scripts-ancestor':
                    (self.project / 'scripts').write_text('keep')
                else:
                    path = self.project / '.team/README.md'
                    path.parent.mkdir(parents=True)
                    if case == 'late-file':
                        path.write_text('keep')
                    elif case == 'late-dir':
                        path.mkdir()
                    elif case == 'late-link':
                        path.symlink_to(self.source)
                    else:
                        os.mkfifo(path)
                before = tree_snapshot(self.project)
                with self.assertRaises(ValueError):
                    self.scaffold()
                self.assertFalse((self.project / 'scripts/team_install.py').exists())
                self.assertFalse((self.project / '.team/install.json').exists())
                self.assertEqual(before, tree_snapshot(self.project))
                self.assertFalse((self.project / 'scripts').is_dir())

    def test_scaffold_cli_without_bytecode_or_network(self):
        result = subprocess.run(['python3', str(self.source / 'adapters/openspec-development-team/scaffold.py'),
                                 '--project', str(self.project)], check=True, capture_output=True, text=True)
        self.assertIn('Manual integration required', result.stdout)
        self.assertFalse(any(self.source.rglob('__pycache__')))
        self.assertFalse((self.project / '.tools').exists())

    def test_dirty_or_untracked_source_refused(self):
        extra = self.source / 'untracked'
        extra.write_text('local')
        try:
            with self.assertRaisesRegex(ValueError, 'clean'):
                self.scaffold()
            self.assertEqual(snapshot(self.project), {})
        finally:
            extra.unlink()

    def test_presets_exact_roles_and_only_experimental_difference(self):
        directory = ROOT / 'adapters/openspec-development-team/presets'
        default = json.loads((directory / 'codex-default.json').read_text())
        experimental = json.loads((directory / 'codex-experimental.json').read_text())
        expected = {'coordinator': ('gpt-6.1-sol', 'medium'), 'architect': ('gpt-6-astra', 'medium'),
                    'planner': ('gpt-6.1-sol', 'high'), 'implementer': ('gpt-6.1-sol', 'medium'),
                    'test-engineer': ('gpt-6.1-sol', 'high'), 'code-reviewer': ('gpt-6-astra', 'medium'),
                    'security-reviewer': ('gpt-6-astra', 'high'), 'documentation-steward': ('gpt-6.1-sol', 'medium')}
        self.assertEqual(default, {'schema_version': 1, 'codex': {
            role: {'model': model, 'model_reasoning_effort': effort} for role, (model, effort) in expected.items()}})
        default['codex']['implementer'] = {'model': 'gpt-6-luna', 'model_reasoning_effort': 'high'}
        self.assertEqual(default, experimental)
        self.scaffold(preset='codex-experimental')
        self.assertEqual(json.loads((self.project / '.team/models.json').read_text()), experimental)
        self.install()

    def test_opencode_inherits_and_rejects_codex_preset(self):
        with self.assertRaises(ValueError):
            self.scaffold(host='opencode', preset='codex-default')
        self.scaffold(host='opencode')
        self.assertEqual(json.loads((self.project / '.team/models.json').read_text()), {'schema_version': 1})
        self.install()
        self.install('verify')

    def test_provenance_hash_and_static_render_drift_refused(self):
        self.scaffold()
        cache = self.install()
        installer = self.project / 'scripts/team_install.py'
        original = installer.read_bytes()
        installer.write_bytes(original + b'\n# local drift\n')
        with self.assertRaisesRegex(ValueError, 'provenance hash'):
            self.install('verify')
        installer.write_bytes(original)
        output = self.project / '.tools/team-runtime/default/config.toml'
        output.write_text(output.read_text() + '# drift\n')
        with self.assertRaisesRegex(ValueError, 'edited'):
            self.install('verify')
        self.assertTrue(cache.is_dir())

    def test_invalid_provenance_and_overlap_before_cache_mutation(self):
        self.scaffold()
        record_path = self.project / '.team/installer-provenance.json'
        record = json.loads(record_path.read_text())
        for key, value in (('sha256', 'bad'), ('installed_path', '../escape'), ('unknown', 'field')):
            with self.subTest(key=key):
                altered = dict(record, **{key: value})
                record_path.write_text(json.dumps(altered))
                with self.assertRaises(ValueError):
                    self.install()
                self.assertFalse((self.project / '.tools').exists())
        record_path.write_text(json.dumps(record))
        config = self.config()
        config['runtimes'][0]['output'] = 'scripts'
        self.save(config)
        with self.assertRaisesRegex(ValueError, 'overlap'):
            self.install()
        self.assertFalse((self.project / '.tools').exists())

    def test_provenance_pin_update_does_not_require_old_checkout(self):
        self.scaffold()
        self.install()
        old = self.config()['upstream']['revision']
        (self.source / 'new.txt').write_text('new source')
        git(self.source, 'add', '.')
        git(self.source, 'commit', '-m', 'new fixture pin')
        try:
            value = self.config()
            value['upstream']['revision'] = git(self.source, 'rev-parse', 'HEAD')
            self.save(value)
            self.install()
            shutil.rmtree(self.project / '.tools/ai-skills' / old)
            self.install('verify')
        finally:
            git(self.source, 'reset', '--hard', self.pin)

    def test_optional_openspec_literal_version_root_and_default_no_execution(self):
        self.scaffold()
        wrapper = self.project / 'scripts/observe.sh'
        wrapper.write_text('#!/usr/bin/env python3\nimport json,sys\nfrom pathlib import Path\nPath("observed.json").write_text(json.dumps(sys.argv[1:]))\nprint("fixture-1")\n')
        wrapper.chmod(0o755)
        (self.project / 'openspec').mkdir()
        literal = 'space; $(touch injected) `touch injected`'
        value = self.config()
        value['openspec'] = {'command': ['scripts/observe.sh', literal], 'root': 'openspec', 'version': 'fixture-1'}
        self.save(value)
        cache = self.install()
        self.install('verify')
        self.assertFalse((self.project / 'observed.json').exists())
        setup.observations(self.project, '.team/install.json', cache, check_openspec=True)
        self.assertEqual(json.loads((self.project / 'observed.json').read_text()), [literal, '--version'])
        self.assertFalse((self.project / 'injected').exists())
        value['openspec']['version'] = 'wrong'
        self.save(value)
        with self.assertRaisesRegex(ValueError, 'version differs'):
            setup.observations(self.project, '.team/install.json', cache, check_openspec=True)
        (self.project / 'openspec').rmdir()
        with self.assertRaisesRegex(ValueError, 'root is missing'):
            setup.observations(self.project, '.team/install.json', cache, check_openspec=True)

    def test_native_codex_loader_arguments_no_inference(self):
        self.scaffold()
        cache = self.install()
        binary = self.project / 'bin/codex'
        binary.parent.mkdir()
        binary.write_text('#!/usr/bin/env python3\nimport json,sys\nfrom pathlib import Path\nPath("native-args.json").write_text(json.dumps(sys.argv[1:]))\n')
        binary.chmod(0o755)
        with patch.dict(os.environ, {'PATH': str(binary.parent) + os.pathsep + os.environ['PATH']}):
            setup.observations(self.project, '.team/install.json', cache, native_codex=True)
        args = json.loads((self.project / 'native-args.json').read_text())
        self.assertEqual(args[:2], ['--cd', str(self.project)])
        self.assertEqual(args[-2:], ['features', 'list'])
        self.assertIn('-c', args)
        self.assertFalse(any(argument in args for argument in ('exec', '--prompt', '--task')))

    def test_wrapper_template_forwards_literal_args_locally(self):
        self.scaffold()
        wrapper = self.project / 'scripts/openspec.sh'
        shutil.copy2(self.project / '.team/templates/openspec.sh', wrapper)
        binary = self.project / 'node_modules/.bin/openspec'
        binary.parent.mkdir(parents=True)
        binary.write_text('#!/usr/bin/env python3\nimport json,os,sys\nprint(json.dumps([sys.argv[1:],os.getcwd(),os.environ["OPENSPEC_TELEMETRY"],os.environ["XDG_CONFIG_HOME"]]))\n')
        binary.chmod(0o755)
        literal = 'space; $(touch injected)'
        result = subprocess.run(['bash', str(wrapper), literal], cwd='/', check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), [[literal], str(self.project), '0', str(self.project / '.tools/openspec-config')])


if __name__ == '__main__':
    unittest.main()
