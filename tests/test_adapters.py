"""Exercise native bindings without model calls or installed host CLIs."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "development_team_adapter", ROOT / "adapters/openspec-development-team/adapter.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ai-skills adapter ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "canonical skill"
        shutil.copytree(adapter.PACKAGE, self.package, ignore=shutil.ignore_patterns("__pycache__"))
        self.team = adapter.load_team(self.package)
        self.output = self.root / "generated bindings"
        self.models = {"schema_version": 1, "codex": {}, "opencode": {}}
        for role in self.team["roles"]:
            identifier = role["id"]
            self.models["codex"][identifier] = {"model": "model-" + identifier,
                                                   "model_reasoning_effort": "high"}
            self.models["opencode"][identifier] = {"model": "provider-" + identifier + "/model",
                                                      "variant": "high"}

    def render(self, host, models=None):
        return adapter.render(host, self.package, self.output, self.team,
                              self.models if models is None else models)

    def write(self, host, models=None):
        files = self.render(host, models)
        adapter.write_generated(self.output, host, self.package, files)
        return files

    def test_all_eight_codex_models_are_independent_native_bindings(self):
        files = self.render("codex")
        config = tomllib.loads(files["config.toml"])
        self.assertEqual(config["model"], "model-coordinator")
        self.assertTrue(config["agents"]["enabled"])
        for role in self.team["roles"]:
            if role["id"] == "coordinator":
                continue
            name = adapter.PREFIX + role["id"]
            path = Path(config["agents"][name]["config_file"]).relative_to(self.output).as_posix()
            settings = tomllib.loads(files[path])
            self.assertEqual(settings["model"], "model-" + role["id"])
            self.assertEqual(settings["model_reasoning_effort"], "high")
            self.assertNotIn("sandbox_mode", settings)  # Native roles inherit runtime permissions.
            self.assertNotIn("model_provider", settings)

    def test_opencode_models_variants_and_dispatch_permissions_are_per_agent(self):
        agents = json.loads(self.render("opencode")["opencode.json"])["agent"]
        self.assertEqual(len(agents), len(self.team["roles"]))
        for role in self.team["roles"]:
            identifier = role["id"]
            settings = agents[adapter.PREFIX + identifier]
            self.assertEqual(settings["model"], f"provider-{identifier}/model")
            self.assertEqual(settings["variant"], "high")
            self.assertEqual(settings["mode"], "primary" if identifier == "coordinator" else "subagent")
            self.assertEqual(settings["permission"]["task"]["*"], "deny")
        coordinator = agents[adapter.PREFIX + "coordinator"]
        self.assertEqual(sum(v == "allow" for v in coordinator["permission"]["task"].values()), 7)
        for identifier in ("code-reviewer", "security-reviewer"):
            self.assertEqual(agents[adapter.PREFIX + identifier]["permission"]["edit"], "deny")
            self.assertEqual(agents[adapter.PREFIX + identifier]["permission"]["bash"], "deny")

    def test_omitted_models_and_effort_inherit_instead_of_being_reset(self):
        for host in adapter.FIELDS:
            files = self.render(host, {"schema_version": 1})
            if host == "codex":
                configs = [tomllib.loads(text) for name, text in files.items() if name.endswith(".toml")]
            else:
                configs = json.loads(files["opencode.json"])["agent"].values()
            for config in configs:
                for key in ("model", "model_reasoning_effort", "variant"):
                    self.assertNotIn(key, config)

    def test_core_instructions_are_referenced_and_not_duplicated(self):
        for host in adapter.FIELDS:
            files = self.render(host)
            for role in self.team["roles"]:
                source = adapter.role_path(self.package, role)
                self.assertIn(str(source), "\n".join(files.values()))
                self.assertNotIn(source.read_text(), "\n".join(files.values()))
            source = self.package / "assets/agents/implementer.md"
            source.write_text(source.read_text() + "\nUpdated canonical instruction.\n")
            self.assertEqual(files, self.render(host))

    def test_invalid_model_maps_fail_instead_of_silently_falling_back(self):
        mutations = [
            lambda v: v["codex"].update(typo={"model": "a"}),
            lambda v: v["codex"]["architect"].update(model_provider="ignored-provider"),
            lambda v: v["opencode"]["architect"].update(model="missing-provider"),
            lambda v: v["opencode"]["architect"].update(model="provider/"),
            lambda v: v["codex"]["architect"].update(model=""),
            lambda v: v["codex"]["architect"].update(model="bad\nmodel"),
            lambda v: v["opencode"]["architect"].update(model="{file:secret}"),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                value = copy.deepcopy(self.models)
                mutation(value)
                path = self.root / "models.json"
                path.write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    adapter.load_models(path, self.team)

    def test_generated_files_can_be_refreshed_for_model_changes(self):
        self.write("codex")
        self.models["codex"]["architect"]["model"] = "changed-model"
        self.write("codex")
        path = self.output / "roles/ai-team-architect.toml"
        self.assertEqual(tomllib.loads(path.read_text())["model"], "changed-model")

    def test_user_files_are_never_overwritten(self):
        self.output.mkdir()
        user_file = self.output / "config.toml"
        user_file.write_text("existing user config")
        with self.assertRaises(ValueError):
            self.write("codex")
        self.assertEqual(user_file.read_text(), "existing user config")

    def test_edited_generated_files_block_the_entire_refresh(self):
        self.write("codex")
        edited = self.output / "roles/ai-team-architect.toml"
        edited.write_text("local edits")
        config = (self.output / "config.toml").read_bytes()
        with self.assertRaises(ValueError):
            self.write("codex")
        self.assertEqual(edited.read_text(), "local edits")
        self.assertEqual((self.output / "config.toml").read_bytes(), config)

    def test_output_symlink_is_rejected_without_writing_to_its_target(self):
        target = self.root / "other directory"
        target.mkdir()
        self.output.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.write("codex")
        self.assertEqual(list(target.iterdir()), [])

    def test_opencode_preserves_existing_config_and_refuses_name_collisions(self):
        config = json.loads(self.render("opencode")["opencode.json"])
        existing = {"model": "original/model", "agent": {"existing-agent": {"mode": "primary"}}}
        environment = {"OPENCODE_CONFIG_CONTENT": json.dumps(existing),
                       "OPENCODE_CONFIG": "/existing/config.json", "KEEP_THIS": "unchanged"}
        result = adapter.opencode_environment(config, environment)
        merged = json.loads(result["OPENCODE_CONFIG_CONTENT"])
        self.assertEqual(merged["model"], existing["model"])
        self.assertEqual(merged["agent"]["existing-agent"], existing["agent"]["existing-agent"])
        self.assertEqual(result["OPENCODE_CONFIG"], environment["OPENCODE_CONFIG"])
        self.assertEqual(result["KEEP_THIS"], "unchanged")
        self.assertEqual(json.loads(environment["OPENCODE_CONFIG_CONTENT"]), existing)
        with self.assertRaises(ValueError):
            adapter.opencode_environment(config, result)
        with self.assertRaises(ValueError):
            adapter.opencode_environment(config, {"OPENCODE_CONFIG_CONTENT": "{/*JSONC*/}"})

    def test_launch_preserves_literal_task_paths_and_host_configuration(self):
        task = 'Literal $(echo no) `echo no` "quoted" task'
        for host in adapter.FIELDS:
            with self.subTest(host=host):
                self.output = self.root / host
                self.write(host)
                command, env = adapter.launch_spec(host, self.output, self.root, task,
                                                    "/fake native cli", [], {"EXISTING": "value"})
                self.assertEqual(command[0], "/fake native cli")
                self.assertIn(str(self.root), command)
                self.assertTrue(command[-1].endswith(task))
                self.assertEqual(env["EXISTING"], "value")
                if host == "codex":
                    self.assertNotIn("developer_instructions", " ".join(command[1:-1]))
                    self.assertIn("fork_context=false", command[-1])

    def test_render_never_launches_a_host_and_run_propagates_failure(self):
        arguments = ["--host", "codex", "--skill", str(self.package),
                     "--output", str(self.output)]
        with patch.object(adapter.subprocess, "run") as run:
            self.assertEqual(adapter.main(["render", *arguments]), 0)
            run.assert_not_called()
            run.return_value.returncode = 19
            self.assertEqual(adapter.main(["run", *arguments, "--project", str(self.root),
                                           "--task", "Scoped change", "--", "--no-alt-screen"]), 19)
            self.assertFalse(run.call_args.kwargs.get("shell", False))
            self.assertIn("--no-alt-screen", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
