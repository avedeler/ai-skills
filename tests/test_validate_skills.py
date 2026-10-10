"""Regression checks for catalog extensibility and package portability."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "validate_skills", Path(__file__).resolve().parents[1] / "scripts/validate_skills.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "skills" / "garden-planning"
        self.package.mkdir(parents=True)
        (self.package / "SKILL.md").write_text(
            "---\nname: garden-planning\ndescription: Plan a garden from site constraints.\n---\n\n"
            "# Garden planning\n\nUse supplied site constraints and label unknowns.\n"
        )
        self.catalog = {
            "schema_version": 1,
            "categories": {"gardening": {"title": "Gardening", "description": "Garden planning."}},
            "skills": [{"name": "garden-planning", "path": "skills/garden-planning",
                        "category": "gardening", "tags": ["planning"]}],
        }
        self.write_catalog()
        (self.root / "evals").mkdir()
        self.scenarios = [{"id": "garden-missing-site", "skill": "garden-planning",
                           "prompt": "Help plan my garden; the site size is unknown.",
                           "expected_behaviors": ["Asks for site constraints."],
                           "forbidden_behaviors": ["Invents the site size."]}]
        self.write_scenarios()

    def write_catalog(self):
        (self.root / "catalog.json").write_text(json.dumps(self.catalog))

    def write_scenarios(self):
        (self.root / "evals/garden-planning.json").write_text(json.dumps(self.scenarios))

    def test_new_category_and_standalone_skill_need_no_optional_directories(self):
        self.assertEqual(validator.validate(self.root), [])

    def test_runtime_reference_must_travel_with_package(self):
        (self.root / "README.md").write_text("# Shared instructions\n")
        with (self.package / "SKILL.md").open("a") as document:
            document.write("\n[Required instructions](../../README.md)\n")
        self.assertTrue(any("runtime link escapes skill package" in e
                            for e in validator.validate(self.root)))

    def test_missing_bundled_reference_is_rejected(self):
        with (self.package / "SKILL.md").open("a") as document:
            document.write("\n[Required instructions](references/missing.md)\n")
        self.assertTrue(any("missing local link" in e for e in validator.validate(self.root)))

    def test_local_worktrees_do_not_contaminate_package_validation(self):
        for name in (".worktrees", "worktrees"):
            checkout = self.root / name / "unrelated-change"
            checkout.mkdir(parents=True)
            (checkout / "README.md").write_text("[Unrelated broken link](missing.md)\n")
        self.assertEqual(validator.validate(self.root), [])

    def test_worktree_named_package_subdirectories_are_still_validated(self):
        for name in (".worktrees", "worktrees"):
            directory = self.package / name
            directory.mkdir()
            (directory / "README.md").write_text("[Required reference](missing.md)\n")
        errors = validator.validate(self.root)
        self.assertEqual(sum("missing local link" in error for error in errors), 2)

    def test_catalog_path_cannot_target_another_package(self):
        self.catalog["skills"][0]["path"] = "skills/something-else"
        self.write_catalog()
        self.assertTrue(any("path must be" in e for e in validator.validate(self.root)))

    def test_renamed_skill_cannot_keep_stale_evaluation_target(self):
        self.scenarios[0]["skill"] = "old-skill-name"
        self.write_scenarios()
        self.assertTrue(any("skill must match" in e for e in validator.validate(self.root)))

    def test_malformed_category_reports_an_error(self):
        self.catalog["skills"][0]["category"] = ["gardening"]
        self.write_catalog()
        self.assertTrue(any("unknown category" in e for e in validator.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
