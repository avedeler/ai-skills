#!/usr/bin/env python3
"""Render or launch native agent configurations from one shared skill package.

Python 3.11+, standard library only. Rendering never launches agents or changes
host/project configuration. Generated files contain bindings, not role copies.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tomllib

PACKAGE = Path(__file__).resolve().parents[2] / "skills/openspec-development-team"
MARKER = "adapter-manifest.json"
PREFIX = "ai-team-"
FIELDS = {"codex": {"model", "model_reasoning_effort"},
          "opencode": {"model", "variant"}}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def safe_text(value, label):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f"{label} must be a nonempty single-line string")
    # OpenCode expands these tokens before parsing JSON, including in model IDs.
    if "{" in value or "}" in value:
        raise ValueError(f"{label} cannot contain substitution braces")
    return value


def load_team(package):
    package = package.resolve(strict=True)
    safe_text(str(package), "skill path")
    team = read_json(package / "assets/team.json")
    roles = team["roles"]
    ids = [role["id"] for role in roles]
    if len(ids) != len(set(ids)) or team["coordinator"] not in ids:
        raise ValueError("invalid core role inventory")
    for role in roles:
        if not re.fullmatch(r"[a-z][a-z0-9-]*", role["id"]):
            raise ValueError("invalid role ID")
        path = (package / "assets" / role["prompt"]).resolve(strict=True)
        if not path.is_relative_to(package) or not path.is_file():
            raise ValueError("role prompt must be inside the core package")
    for path in (package / "SKILL.md", package / "assets/handoff.md"):
        if not path.is_file():
            raise ValueError(f"missing core instruction file: {path}")
    return team


def load_models(path, team):
    value = read_json(path) if path else {"schema_version": 1}
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise ValueError("models must be an object with schema_version 1")
    if set(value) - {"schema_version", *FIELDS}:
        raise ValueError("unknown models configuration field")
    ids = {role["id"] for role in team["roles"]}
    for host, allowed in FIELDS.items():
        settings = value.get(host, {})
        if not isinstance(settings, dict) or set(settings) - ids:
            raise ValueError(f"{host}: expected settings keyed by core role ID")
        for role, fields in settings.items():
            if not isinstance(fields, dict) or set(fields) - allowed:
                raise ValueError(f"{host}/{role}: allowed fields are {sorted(allowed)}")
            for key, setting in fields.items():
                safe_text(setting, f"{host}/{role}/{key}")
            if host == "opencode" and "model" in fields:
                provider, separator, model = fields["model"].partition("/")
                if not provider or not separator or not model:
                    raise ValueError(f"{host}/{role}: use provider/model-id")
    return value


def role_path(package, role):
    return (package / "assets" / role["prompt"]).resolve()


def binding(package, team, role, host):
    """Native dispatch/path instructions only; domain instructions remain in core."""
    lines = [f"Shared skill package: {package}",
             "Resolve relative links from the source file that contains them.",
             f"Load and follow {role_path(package, role)} before acting.",
             f"Use the assignment/return contract in {package / 'assets/handoff.md'}."]
    if role["id"] == team["coordinator"]:
        lines += [f"Load and follow the coordinator workflow in {package / 'SKILL.md'}.",
                  "Use the following native agent names for the core role IDs:"]
        lines += [f"- {r['id']}: {PREFIX}{r['id']}" for r in team["roles"]
                  if r["id"] != team["coordinator"]]
        if host == "codex":
            lines += ["Dispatch with spawn_agent agent_type set to that native name and "
                      "fork_context=false. Supply the bounded handoff explicitly; "
                      "full-history forks may ignore or reject configured roles.",
                      "Release completed specialist slots through the host lifecycle "
                      "before exceeding its thread limit; retain their handoff records."]
        else:
            lines += ["Dispatch with the native Task tool using those subagent names."]
        lines += ["Use the configured role models; do not override them in dispatch or "
                  "silently substitute another model after an error."]
    return "\n".join(lines) + "\n"


def toml_assignments(value, prefix=()):
    """Only JSON scalar leaves are needed by our small native config subset."""
    for key, item in value.items():
        path = (*prefix, key)
        if isinstance(item, dict):
            yield from toml_assignments(item, path)
        else:
            yield ".".join(json.dumps(part) for part in path) + " = " + json.dumps(item, ensure_ascii=False)


def render(host, package, output, team, models):
    configured = models.get(host, {})
    coordinator = next(r for r in team["roles"] if r["id"] == team["coordinator"])
    bootstrap = binding(package, team, coordinator, host)
    if host == "codex":
        config = dict(configured.get(coordinator["id"], {}))
        config["agents"] = {"enabled": True}
        files = {"bootstrap.md": bootstrap}
        for role in team["roles"]:
            if role == coordinator:
                continue
            name = PREFIX + role["id"]
            relative = f"roles/{name}.toml"
            settings = dict(configured.get(role["id"], {}))
            settings["developer_instructions"] = binding(package, team, role, host)
            files[relative] = "\n".join(toml_assignments(settings)) + "\n"
            config["agents"][name] = {"description": role["purpose"],
                                      "config_file": str(output / relative)}
        files["config.toml"] = "\n".join(toml_assignments(config)) + "\n"
        return files

    agents = {}
    for role in team["roles"]:
        name = PREFIX + role["id"]
        primary = role == coordinator
        prompt = binding(package, team, role, host)
        prompt += f"\n{{file:{role_path(package, role)}}}\n"
        prompt += f"\n{{file:{package / 'assets/handoff.md'}}}\n"
        if primary:
            prompt += f"\n{{file:{package / 'SKILL.md'}}}\n"
        permission = {"task": {"*": "deny"}}
        if primary:
            permission["task"].update({PREFIX + r["id"]: "allow" for r in team["roles"]
                                       if r != coordinator})
        if role["id"] in {"code-reviewer", "security-reviewer"}:
            # Bash can write even when the editor is denied. Other host tools
            # still need their normal permission policy; this is not a sandbox.
            permission.update(edit="deny", bash="deny")
        agents[name] = {"description": role["purpose"],
                        "mode": "primary" if primary else "subagent",
                        "prompt": prompt, "permission": permission,
                        **configured.get(role["id"], {})}
    return {"opencode.json": json_text({"$schema": "https://opencode.ai/config.json", "agent": agents}),
            "bootstrap.md": bootstrap}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def preflight_generated(output, host, files):
    """Refuse to replace user files or edited outputs; never edit host configs."""
    if any(path.is_symlink() for path in (output, *output.parents)):
        raise ValueError("output directory must not traverse a symlink")
    existing = {}
    if output.exists():
        if not output.is_dir():
            raise ValueError("output must be a directory")
        if any(path.is_symlink() for path in output.rglob("*")):
            raise ValueError("generated output contains a symlink")
        if any(not (stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode))
               for p in output.rglob("*")):
            raise ValueError("generated output contains a special file")
        present = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
        if present:
            if MARKER not in present:
                raise ValueError("output contains files not owned by this adapter; choose an empty directory")
            previous = read_json(output / MARKER)
            if previous.get("adapter") != "openspec-development-team" or previous.get("host") != host:
                raise ValueError("output belongs to another adapter/host")
            existing = previous.get("files", {})
            if not isinstance(existing, dict) or present != set(existing) | {MARKER}:
                raise ValueError("output file inventory changed; preserve it and use a new directory")
            for name, expected in existing.items():
                if digest((output / name).read_bytes()) != expected:
                    raise ValueError(f"generated file was edited: {name}; use a new output directory")
            if set(existing) - set(files):
                raise ValueError("generated layout changed; use a new output directory")


def write_generated(output, host, package, files):
    """Validate ownership before writing generated bindings."""
    preflight_generated(output, host, files)
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest = {"schema_version": 1, "adapter": "openspec-development-team", "host": host,
                "package": str(package),
                "files": {name: digest(text.encode()) for name, text in files.items()}}
    (output / MARKER).write_text(json_text(manifest), encoding="utf-8")


def opencode_environment(config, environment):
    environment = dict(environment)
    # Preserve existing user configuration. Inline JSONC cannot be safely merged
    # with the standard library: fail instead of silently dropping it.
    existing = json.loads(environment.get("OPENCODE_CONFIG_CONTENT") or "{}")
    if not isinstance(existing, dict) or not isinstance(existing.get("agent", {}), dict):
        raise ValueError("OPENCODE_CONFIG_CONTENT must contain a JSON object with an agent object")
    if set(existing.get("agent", {})) & set(config["agent"]):
        raise ValueError("existing inline configuration defines an ai-team agent; resolve the collision")
    existing["agent"] = {**existing.get("agent", {}), **config["agent"]}
    environment["OPENCODE_CONFIG_CONTENT"] = json.dumps(existing)
    return environment


def launch_spec(host, output, project, task, executable, native_args, environment):
    prompt = (output / "bootstrap.md").read_text(encoding="utf-8") + "\nRequested task:\n" + task
    if host == "codex":
        config = tomllib.loads((output / "config.toml").read_text(encoding="utf-8"))
        command = [executable or "codex", "--cd", str(project)]
        for assignment in toml_assignments(config):
            command += ["-c", assignment]
        command += [*native_args, "--", prompt]
        return command, dict(environment)
    config = read_json(output / "opencode.json")
    coordinator = next(name for name, role in config["agent"].items() if role["mode"] == "primary")
    command = [executable or "opencode", str(project), *native_args,
               "--agent", coordinator, "--prompt", prompt]
    return command, opencode_environment(config, environment)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("render", "run"))
    parser.add_argument("--host", required=True, choices=tuple(FIELDS))
    parser.add_argument("--models", type=Path, help="omitted role settings inherit host defaults")
    parser.add_argument("--skill", type=Path, default=PACKAGE, help="path to the canonical complete skill package")
    parser.add_argument("--output", type=Path, required=True, help="dedicated generated directory; keep for resume")
    parser.add_argument("--project", type=Path, help="assigned repository/worktree; required for run")
    parser.add_argument("--task", help="authorized development task; required for run")
    parser.add_argument("--executable", help="optional path to the native host executable")
    args, native_args = parser.parse_known_args(argv)
    if native_args and native_args[0] != "--":
        parser.error("native arguments must follow --")
    native_args = native_args[1:]
    try:
        package = args.skill.resolve(strict=True)
        # absolute() intentionally preserves symlinks so write_generated can reject them.
        output = args.output.absolute()
        safe_text(str(output), "output path")
        if output.is_relative_to(package) or package.is_relative_to(output):
            raise ValueError("generated output must be separate from the canonical skill package")
        if args.action == "run" and (not args.project or not args.task):
            raise ValueError("run requires --project and --task")
        project = args.project.resolve(strict=True) if args.project else None
        if project is not None and not project.is_dir():
            raise ValueError("project must be an existing directory")
        if args.action == "render" and native_args:
            raise ValueError("native arguments apply only to run")
        team = load_team(package)
        models = load_models(args.models, team)
        files = render(args.host, package, output, team, models)
        write_generated(output, args.host, package, files)
        print(f"Rendered {args.host} bindings in {output}; core instructions remain in {package}", flush=True)
        if args.action == "render":
            return 0
        command, environment = launch_spec(args.host, output, project, args.task,
                                            args.executable, native_args, os.environ)
        return subprocess.run(command, cwd=project, env=environment, check=False).returncode
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
