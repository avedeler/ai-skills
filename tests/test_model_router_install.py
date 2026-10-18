"""Check that installing the optional router profile preserves existing work."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ADAPTER = Path(__file__).resolve().parents[1] / 'adapters' / 'openspec-model-router'
spec = importlib.util.spec_from_file_location('router_install', ADAPTER / 'install.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RouterInstallTests(unittest.TestCase):
    def test_complete_install_and_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            target = module.install(Path(temp))
            self.assertTrue((target / 'SKILL.md').is_file())
            for name in ('model-profile.md', 'runtime.md', 'research.md'):
                self.assertEqual((target / 'references' / name).read_bytes(),
                                 (ADAPTER / name).read_bytes())
            self.assertEqual(module.install(Path(temp)), target)

    def test_refuses_modified_install(self):
        with tempfile.TemporaryDirectory() as temp:
            target = module.install(Path(temp))
            marker = target / 'SKILL.md'
            marker.write_text('Local changes')
            with self.assertRaises(ValueError):
                module.install(Path(temp))
            self.assertEqual(marker.read_text(), 'Local changes')

    def test_refuses_symlink_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            outside = root / 'outside'
            outside.mkdir()
            (root / 'openspec-model-router').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                module.install(root)
            self.assertEqual(list(outside.iterdir()), [])
