"""Offline real-Git integration and preservation checks for the copied installer."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('team_install', ROOT / 'adapters/openspec-development-team/install.py')
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def git(path, *args):
    return subprocess.run(['git', '-C', str(path), *args], check=True,
                          capture_output=True).stdout.decode().strip()


def snapshot(path):
    return {str(p.relative_to(path)): ('link', os.readlink(p)) if p.is_symlink()
            else ('file', p.read_bytes(), p.stat().st_mode) for p in path.rglob('*')
            if p.is_symlink() or p.is_file()}


class InstallTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = tempfile.TemporaryDirectory(prefix='upstream fixture ')
        cls.source = Path(cls.fixture.name) / 'source'
        cls.source.mkdir()
        for name in ('skills', 'adapters'):
            shutil.copytree(ROOT / name, cls.source / name,
                            ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT / 'THIRD_PARTY_NOTICES.md', cls.source)
        git(cls.source, 'init')
        git(cls.source, 'config', 'user.name', 'Fixture')
        git(cls.source, 'config', 'user.email', 'fixture@example.invalid')
        git(cls.source, 'add', '.')
        git(cls.source, 'commit', '-m', 'Synthetic upstream A')
        cls.a = git(cls.source, 'rev-parse', 'HEAD')
        (cls.source / 'fixture.txt').write_text('B\n')
        git(cls.source, 'add', '.')
        git(cls.source, 'commit', '-m', 'Synthetic upstream B')
        cls.b = git(cls.source, 'rev-parse', 'HEAD')

    @classmethod
    def tearDownClass(cls):
        cls.fixture.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='project ; literal space ')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        (self.project / '.team').mkdir()
        self.config = self.project / '.team/install.json'
        self.value = {'schema_version': 1, 'upstream': {'url': self.source.as_uri(), 'revision': self.a},
                      'cache': '.tools/ai-skills', 'registration': '.agents/skills/openspec-development-team',
                      'runtimes': [{'name': 'default', 'host': 'codex', 'output': '.tools/runtime/default'},
                                   {'name': 'other', 'host': 'opencode', 'output': '.tools/runtime/other'}]}
        self.save()

    def save(self):
        self.config.write_text(json.dumps(self.value))

    def install(self, action='install'):
        return setup.install(self.project, '.team/install.json', action)

    def test_offline_repeat_verify_notices_and_literal_paths(self):
        cache = self.install()
        before = snapshot(self.project)
        original = setup.command
        def offline(args, **kwargs):
            self.assertNotIn('clone', args)
            self.assertNotIn('fetch', args)
            return original(args, **kwargs)
        with patch.object(setup, 'command', side_effect=offline):
            self.assertEqual(cache, self.install())
            self.assertEqual(cache, self.install('verify'))
        self.assertEqual(before, snapshot(self.project))
        self.assertTrue((cache / 'THIRD_PARTY_NOTICES.md').is_file())
        self.assertTrue((cache / 'skills/openspec-development-team/third_party/openspec/LICENSE').is_file())
        self.assertEqual((cache / 'adapters/openspec-development-team/install.py').read_bytes(),
                         (ROOT / 'adapters/openspec-development-team/install.py').read_bytes())

    def test_shared_models_and_host_linked_worktree(self):
        host = self.project / 'host'
        host.mkdir()
        git(host, 'init')
        git(host, 'config', 'user.name', 'Fixture')
        git(host, 'config', 'user.email', 'fixture@example.invalid')
        (host / 'README').write_text('host')
        git(host, 'add', '.')
        git(host, 'commit', '-m', 'host')
        worktree = self.project / 'linked worktree'
        git(host, 'worktree', 'add', '--detach', str(worktree))
        shutil.copytree(self.project / '.team', worktree / '.team')
        self.project = worktree
        self.config = worktree / '.team/install.json'
        shutil.copy2(ROOT / 'adapters/openspec-development-team/models.example.json',
                     worktree / '.team/models.json')
        for runtime in self.value['runtimes']:
            runtime['models'] = '.team/models.json'
        self.save()
        self.install()
        self.install('verify')
        self.assertTrue((worktree / '.git').is_file())

    def test_cache_and_metadata_symlink_boundaries(self):
        cache = self.install()
        elsewhere = self.project / 'moved-cache'
        cache.rename(elsewhere)
        cache.symlink_to(elsewhere, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install('verify')
        cache.unlink()
        elsewhere.rename(cache)
        metadata = cache / '.git'
        metadata.rename(self.project / 'moved-metadata')
        metadata.symlink_to(self.project / 'moved-metadata', target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install('verify')

    def test_special_config_models_and_output_preserved(self):
        self.install()
        output = self.project / '.tools/runtime/other/fifo'
        os.mkfifo(output)
        with self.assertRaises(ValueError):
            self.install()
        output.unlink()
        models = self.project / '.team/models.json'
        os.mkfifo(models)
        self.value['runtimes'][0]['models'] = '.team/models.json'
        self.save()
        with self.assertRaises(ValueError):
            self.install()
        models.unlink()
        self.config.unlink()
        os.mkfifo(self.config)
        with self.assertRaises(ValueError):
            self.install()

    def test_owned_update_retains_old_cache(self):
        old = self.install()
        before = snapshot(old)
        self.value['upstream']['revision'] = self.b
        self.save()
        new = self.install()
        self.assertEqual(before, snapshot(old))
        self.assertEqual((self.project / self.value['registration']).resolve(), new / setup.PACKAGE)
        self.install('verify')

    def test_invalid_config_before_mutation(self):
        variations = [('schema_version', True), ('unknown', 1), ('cache', '../escape'),
                      ('cache', '.team'), ('registration', '/absolute'),
                      ('upstream', {'url': 'ext::evil', 'revision': self.a}),
                      ('upstream', {'url': self.source.as_uri(), 'revision': self.a.upper()}),
                      ('runtimes', [{'name': 'x', 'host': 'codex', 'output': 'out'},
                                    {'name': 'x', 'host': 'codex', 'output': 'out2'}])]
        original = dict(self.value)
        for key, value in variations:
            with self.subTest(key=key, value=value):
                self.value = dict(original, **{key: value})
                self.save()
                before = snapshot(self.project)
                with self.assertRaises(ValueError):
                    self.install()
                self.assertEqual(before, snapshot(self.project))

    def test_later_output_failure_preserves_earlier_and_registration(self):
        self.install()
        self.value['upstream']['revision'] = self.b
        self.save()
        output = self.project / '.tools/runtime/other/opencode.json'
        output.write_text('local edits')
        paths = [self.project / '.tools/runtime', self.project / '.agents', self.project / '.team']
        before = [snapshot(p) for p in paths]
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(before, [snapshot(p) for p in paths])

    def test_foreign_registration_preserved(self):
        registration = self.project / self.value['registration']
        registration.parent.mkdir(parents=True)
        registration.symlink_to(self.source)
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(os.readlink(registration), str(self.source))

    def test_cache_tampering_refused_before_adapter(self):
        changes = {
            'head': lambda c: (c / '.git/HEAD').write_text(self.b),
            'origin': lambda c: git(c, 'remote', 'set-url', 'origin', 'https://example.invalid/other'),
            'staged': lambda c: git(c, 'update-index', '--force-remove', 'THIRD_PARTY_NOTICES.md'),
            'mode': lambda c: (c / 'THIRD_PARTY_NOTICES.md').chmod(0o755),
            'assume': lambda c: git(c, 'update-index', '--assume-unchanged', 'THIRD_PARTY_NOTICES.md'),
            'skip': lambda c: git(c, 'update-index', '--skip-worktree', 'THIRD_PARTY_NOTICES.md'),
            'missing': lambda c: (c / 'THIRD_PARTY_NOTICES.md').unlink(),
            'untracked': lambda c: (c / 'extra').write_text('extra'),
            'ignored': lambda c: ((c / '.git/info').mkdir(exist_ok=True), (c / '.git/info/exclude').write_text('ignored\n'), (c / 'ignored').write_text('extra')),
            'directory': lambda c: (c / 'extra-dir').mkdir(),
            'symlink': lambda c: (c / 'extra').symlink_to(self.source),
            'metadata-link': lambda c: (c / '.git/extra').symlink_to(self.source),
            'fifo': lambda c: os.mkfifo(c / 'fifo'),
            'alternates': lambda c: (c / '.git/objects/info/alternates').write_text(str(self.source / '.git/objects')),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                cache = self.install()
                change(cache)
                before = snapshot(self.project) if name != 'fifo' else None
                with patch.object(setup, 'adapter_for', side_effect=AssertionError('unverified adapter executed')):
                    with self.assertRaises((ValueError, subprocess.CalledProcessError)):
                        self.install('verify')
                if before is not None:
                    self.assertEqual(before, snapshot(self.project))
                shutil.rmtree(cache)

    def test_corrupt_object_cannot_weaken_fsck(self):
        cache = self.install()
        oid = git(cache, 'rev-parse', 'HEAD:adapters/openspec-development-team/adapter.py')
        bad = b'raise RuntimeError("executed corrupt adapter")\n'
        (cache / setup.ADAPTER).write_bytes(bad)
        obj = cache / '.git/objects' / oid[:2] / oid[2:]
        obj.parent.mkdir(exist_ok=True)
        if obj.exists():
            obj.chmod(0o644)
        obj.write_bytes(zlib.compress(b'blob ' + str(len(bad)).encode() + b'\0' + bad))
        git(cache, 'config', 'fsck.hashMismatch', 'ignore')
        skip = cache / '.git/skip-list'
        skip.write_text(oid + '\n')
        git(cache, 'config', 'fsck.skipList', str(skip))
        with patch.object(setup, 'adapter_for', side_effect=AssertionError('unverified adapter executed')):
            with self.assertRaises(subprocess.CalledProcessError):
                self.install('verify')

    def test_cached_helpers_and_inherited_git_environment_never_run(self):
        cache = self.install()
        sentinel = self.project / 'helper-ran'
        helper = self.project / 'helper'
        helper.write_text('#!/bin/sh\ntouch "' + str(sentinel) + '"\n')
        helper.chmod(0o755)
        for key in ('core.fsmonitor', 'core.hooksPath', 'filter.evil.smudge', 'filter.evil.clean'):
            git(cache, 'config', key, str(helper))
        git(cache, 'config', 'include.path', str(helper))
        with patch.dict(os.environ, {'GIT_DIR': '/missing', 'GIT_INDEX_FILE': '/missing',
                                    'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.fsmonitor',
                                    'GIT_CONFIG_VALUE_0': str(helper)}):
            self.install('verify')
        self.assertFalse(sentinel.exists())


if __name__ == '__main__':
    unittest.main()
