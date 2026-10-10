"""Exercise development-team evidence failures without models or live services."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / "skills/openspec-development-team"
spec = importlib.util.spec_from_file_location("check_readiness", PACKAGE / "scripts/check_readiness.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DevelopmentTeamTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((PACKAGE / "assets/policy.example.json").read_text())
        self.packet = json.loads((PACKAGE / "assets/evidence.example.json").read_text())
        self.candidate = self.packet["candidate"]

    def errors(self):
        return checker.check(self.policy, self.packet, self.candidate, allow_synthetic=True)

    def test_synthetic_example_requires_explicit_fixture_mode(self):
        self.assertTrue(any("Synthetic" in e for e in checker.check(self.policy, self.packet, self.candidate)))
        self.assertEqual(self.errors(), [])

    def test_stale_pass_does_not_cover_new_candidate(self):
        self.packet["checks"]["unit"]["candidate"] = "sha256:" + "b" * 64
        self.assertTrue(any("check unit: stale" in e for e in self.errors()))

    def test_failed_or_skipped_required_check_cannot_pass(self):
        for status in ("failed", "skipped", "not_run", "blocked"):
            with self.subTest(status=status):
                self.packet["checks"]["unit"]["status"] = status
                self.assertTrue(any("check unit: required result" in e for e in self.errors()))

    def test_check_cannot_claim_success_with_nonzero_exit(self):
        self.packet["checks"]["integration"]["exit_code"] = 1
        self.assertTrue(any("successful command exit" in e for e in self.errors()))

    def test_dropped_scenario_is_not_full_conformance(self):
        self.packet["traceability"].pop()
        self.assertTrue(any("missing required scenario" in e for e in self.errors()))

    def test_docs_mapping_cannot_disappear(self):
        del self.packet["traceability"][0]["doc_ref"]
        self.assertTrue(any("needs documentation" in e for e in self.errors()))

    def test_author_cannot_supply_independent_code_review(self):
        self.packet["code_review"]["session_id"] = self.packet["author_sessions"][0]
        self.assertTrue(any("independent non-author" in e for e in self.errors()))

    def test_security_trigger_cannot_be_skipped(self):
        self.packet["security"]["triggers"] = ["authorization"]
        self.assertTrue(any("security_review: missing receipt" in e for e in self.errors()))
        self.packet["security"]["review"] = dict(self.packet["code_review"], session_id="independent-security-review")
        self.assertEqual(self.errors(), [])

    def test_unknown_security_is_not_low_risk(self):
        self.packet["security"]["triage"] = "unknown"
        self.assertTrue(any("unknown or incomplete" in e for e in self.errors()))

    def test_unapplied_specs_block_and_cannot_claim_idempotence(self):
        self.packet["spec_sync"]["remaining_deltas"] = 1
        self.packet["spec_sync"]["idempotent"] = False
        errors = self.errors()
        self.assertTrue(any("deltas remain" in e for e in errors))
        self.assertTrue(any("second comparison" in e for e in errors))

    def test_no_delta_docs_change_can_have_justified_no_sync(self):
        self.policy["spec_sync_required"] = False
        self.packet["spec_sync"].update(delta_count=0, status="not_applicable", reason="Selected schema reports no delta specs.")
        self.assertEqual(self.errors(), [])

    def test_material_finding_needs_closure_evidence(self):
        finding = {"id": "F1", "severity": "major", "status": "open"}
        self.packet["findings"] = [finding]
        self.assertTrue(any("unresolved material finding" in e for e in self.errors()))
        finding["status"] = "closed"
        self.assertTrue(any("closure evidence required" in e for e in self.errors()))
        finding["closure_evidence"] = "synthetic:reviewed-regression"
        self.assertEqual(self.errors(), [])

    def test_two_failed_correction_rounds_stop(self):
        self.packet["correction"]["failed_rounds"] = 2
        self.assertTrue(any("stop limit" in e for e in self.errors()))

    def test_stalled_progress_stops_earlier(self):
        self.packet["correction"]["stalled"] = True
        self.assertTrue(any("stalled" in e for e in self.errors()))

    def test_bad_types_report_gaps_instead_of_crashing(self):
        mutations = [("checks", []), ("security", "unknown"), ("spec_sync", None),
                     ("traceability", [None]), ("author_sessions", None)]
        for key, value in mutations:
            with self.subTest(key=key):
                packet = copy.deepcopy(self.packet)
                packet[key] = value
                self.assertTrue(checker.check(self.policy, packet, self.candidate, True))

    def test_cli_rejects_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("{")
            result = subprocess.run([sys.executable, str(PACKAGE / "scripts/check_readiness.py"),
                                     "--policy", str(path), "--packet", str(path),
                                     "--expected-candidate", self.candidate], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("INVALID INPUT", result.stderr)

    def test_role_manifest_bundles_unique_short_prompts(self):
        team = json.loads((PACKAGE / "assets/team.json").read_text())
        ids = [role["id"] for role in team["roles"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn(team["coordinator"], ids)
        for role in team["roles"]:
            with self.subTest(role=role["id"]):
                path = (PACKAGE / "assets" / role["prompt"]).resolve()
                self.assertTrue(path.is_relative_to(PACKAGE.resolve()))
                content = path.read_text()
                prompt = content.split("## System prompt\n", 1)[1].split("## Boundary", 1)[0]
                self.assertLess(len(prompt.split()), 300)

    def test_workspace_references_and_license_survive_standalone_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "openspec-development-team"
            shutil.copytree(PACKAGE, package, ignore=shutil.ignore_patterns("__pycache__"))
            team = json.loads((package / "assets/team.json").read_text())
            for key in ("integration_guide", "record_template", "bundled_skill",
                        "attribution", "license", "provenance"):
                path = (package / "assets" / team["workspace"][key]).resolve()
                self.assertTrue(path.is_relative_to(package))
                self.assertTrue(path.is_file(), key)
            self.assertEqual(team["workspace"]["owner"], team["coordinator"])

    def test_vendored_upstream_files_match_recorded_revision_hashes(self):
        vendor = PACKAGE / "third_party/using-git-worktrees"
        metadata = json.loads((vendor / "UPSTREAM.json").read_text())
        self.assertRegex(metadata["revision"], r"\A[0-9a-f]{40}\Z")
        self.assertEqual({entry["path"] for entry in metadata["files"]}, {"SKILL.md", "LICENSE"})
        for entry in metadata["files"]:
            with self.subTest(file=entry["path"]):
                data = (vendor / entry["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"])
        self.assertIn(metadata["copyright"], (vendor / "LICENSE").read_text())


if __name__ == "__main__":
    unittest.main()
