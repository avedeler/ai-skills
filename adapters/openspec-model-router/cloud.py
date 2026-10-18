#!/usr/bin/env python3
"""Install, verify and preflight the reviewed OpenSpec cloud workflow."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import sys
import tempfile

ADAPTER = Path(__file__).resolve().parent
REPOSITORY = ADAPTER.parents[1]
ROUTER = REPOSITORY / "skills" / "openspec-model-router"
TEAM = REPOSITORY / "skills" / "openspec-development-team"
BEGIN = "<!-- BEGIN MANAGED OPENSPEC CLOUD WORKFLOW -->"
END = "<!-- END MANAGED OPENSPEC CLOUD WORKFLOW -->"
DEFAULT_VERSION = "1.14.3"
TIMEOUT = 20


def _inventory(source: Path) -> dict[str, bytes]:
    if source.is_symlink() or not source.is_dir():
        raise ValueError(f"required source package is missing or unsafe: {source}")
    result = {}
    for path in source.rglob("*"):
        if "__pycache__" in path.parts or path.suffix in (".pyc", ".pyo"):
            continue
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"source package contains a symlink: {path}")
        if stat.S_ISDIR(mode):
            continue
        if stat.S_ISREG(mode):
            result[path.relative_to(source).as_posix()] = path.read_bytes()
        else:
            raise ValueError(f"source package contains a nonregular entry: {path}")
    return result


def _installed_match(path: Path, expected: dict[str, bytes]) -> bool:
    try:
        path_mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(path_mode):
        if not path.exists() or not path.is_dir():
            return False
        path = path.resolve()
    try:
        path_mode = path.lstat().st_mode
    except FileNotFoundError:
        return False
    if not stat.S_ISDIR(path_mode):
        return False
    found = {}
    for child in path.rglob("*"):
        if "__pycache__" in child.parts or child.suffix in (".pyc", ".pyo"):
            continue
        mode = child.lstat().st_mode
        if stat.S_ISLNK(mode):
            return False
        if stat.S_ISDIR(mode):
            continue
        if stat.S_ISREG(mode):
            found[child.relative_to(path).as_posix()] = child.read_bytes()
        else:
            raise ValueError(f"installed package contains a nonregular entry: {child}")
    return found == expected


def _safe_parent(path: Path) -> None:
    for ancestor in reversed(path.parents):
        if ancestor.is_symlink() or (ancestor.exists() and not ancestor.is_dir()):
            raise ValueError(f"unsafe destination parent: {ancestor}")


def _stage_package(source: Path, destination: Path, expected: dict[str, bytes]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".cloud-skill-", dir=destination.parent) as tmp:
        staged = Path(tmp) / destination.name
        for rel, content in expected.items():
            target = staged / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        staged.rename(destination)


def _atomic_write(path: Path, content: bytes) -> None:
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, temporary = tempfile.mkstemp(prefix=".cloud-agents-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _router_expected() -> dict[str, bytes]:
    files = _inventory(ROUTER)
    files.update({f"references/{name}": (ADAPTER / name).read_bytes()
                  for name in ("model-profile.md", "runtime.md", "research.md")})
    return files


def _block(workspace: Path, skills_dir: Path, openspec_command: str = "openspec",
           openspec_version: str = DEFAULT_VERSION) -> bytes:
    text = (ADAPTER / "cloud-AGENTS.md").read_text()
    values = {
        "MODEL_ROUTER_SKILL": json.dumps(str((skills_dir / "openspec-model-router" / "SKILL.md").resolve())),
        "DEVELOPMENT_TEAM_SKILL": json.dumps(str((skills_dir / "openspec-development-team" / "SKILL.md").resolve())),
        "WORKSPACE_DISPLAY": json.dumps(str(workspace)),
        "WORKSPACE_ARG": shlex.quote(str(workspace)),
        "CLOUD_SCRIPT": shlex.quote(str(ADAPTER / "cloud.py")),
        "SKILLS_DIR": shlex.quote(str(skills_dir)),
        "OPENSPEC_COMMAND": shlex.quote(openspec_command),
        "OPENSPEC_VERSION": shlex.quote(openspec_version),
    }
    text = re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: values[match.group(1)], text)
    return text.rstrip("\n").encode()


def _managed_content(existing: bytes | None, block: bytes) -> bytes:
    if existing is None:
        return block + b"\n"
    start, end = BEGIN.encode(), END.encode()
    starts, ends = existing.count(start), existing.count(end)
    if starts != ends or starts > 1:
        raise ValueError("workspace AGENTS.md has malformed or duplicate managed boundaries")
    if starts:
        left, right = existing.index(start), existing.index(end) + len(end)
        if right < left or (right < len(existing) and existing[right:right + 1] not in (b"\n", b"\r")):
            raise ValueError("workspace AGENTS.md has malformed managed block")
        old = existing[left:right]
        if old != block:
            raise ValueError("managed workspace AGENTS.md block differs; preserve and reconcile it manually")
        return existing
    sep = b"" if not existing or existing.endswith((b"\n", b"\r")) else b"\n"
    return existing + sep + block + b"\n"


def _cli_path(command: str) -> str:
    if os.sep in command:
        candidate = Path(command).expanduser()
        if not candidate.is_file() or not os.access(candidate, os.X_OK):
            raise ValueError(f"OpenSpec executable is missing or not executable: {command}")
        return str(candidate.resolve())
    import shutil as _shutil
    found = _shutil.which(command)
    if not found:
        raise ValueError(f"OpenSpec executable not found: {command}")
    return str(Path(found).resolve())


def _project_cli_path(command: str, project: Path) -> str:
    candidate = Path(command).expanduser()
    if not candidate.is_absolute():
        project_candidate = project / candidate
        if os.sep in command or project_candidate.exists() or project_candidate.is_symlink():
            candidate = project_candidate
        else:
            return _cli_path(command)
    if not candidate.is_file() or not os.access(candidate, os.X_OK):
        raise ValueError(f"project OpenSpec executable is missing or not executable: {candidate}")
    return str(candidate.resolve())


def _check_version(command: str, expected: str, cwd: Path, label: str) -> None:
    try:
        result = subprocess.run([command, "--version"], cwd=cwd, capture_output=True,
                                text=True, timeout=TIMEOUT,
                                env={**os.environ, "OPENSPEC_TELEMETRY": "0"}, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ValueError(f"{label} version check timed out after {TIMEOUT}s") from exc
    except OSError as exc:
        raise ValueError(f"could not run {label} version check: {exc}") from exc
    actual = result.stdout.strip()
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise ValueError(f"{label} version check failed ({result.returncode})"
                         + (f": {detail}" if detail else ""))
    if actual != expected:
        raise ValueError(f"{label} version mismatch: expected {expected!r}, observed {actual!r}")


def _run(command: str, args: list[str], project: Path, timeout: int = TIMEOUT) -> dict:
    try:
        result = subprocess.run([command, *args], cwd=project, capture_output=True,
                                text=True, timeout=timeout,
                                env={**os.environ, "OPENSPEC_TELEMETRY": "0"}, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ValueError(f"OpenSpec command timed out after {timeout}s: {args[0]}") from exc
    except OSError as exc:
        raise ValueError(f"could not run OpenSpec command {args[0]}: {exc}") from exc
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise ValueError(f"OpenSpec command failed ({result.returncode}): {' '.join(args)}"
                         + (f": {detail}" if detail else ""))
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"OpenSpec returned malformed JSON for {' '.join(args)}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"OpenSpec returned a non-object for {' '.join(args)}")
    return payload


def _verify(workspace: Path, skills_dir: Path, openspec_command: str, expected_version: str) -> str:
    workspace = workspace.resolve()
    skills_dir = Path(os.path.abspath(skills_dir.expanduser()))
    command = _cli_path(openspec_command)
    router_expected = _router_expected()
    team_expected = _inventory(TEAM)
    router_path = skills_dir / "openspec-model-router"
    team_path = skills_dir / "openspec-development-team"
    if not _installed_match(router_path, router_expected):
        raise ValueError(f"router package/profile is missing or differs: {router_path}")
    if not _installed_match(team_path, team_expected):
        raise ValueError(f"development-team package is missing or differs: {team_path}")
    agents = workspace / "AGENTS.md"
    if agents.is_symlink() or not agents.is_file():
        raise ValueError(f"workspace managed instructions are missing: {agents}")
    expected_block = _block(workspace, skills_dir, command, expected_version)
    actual_agents = agents.read_bytes()
    if _managed_content(actual_agents, expected_block) != actual_agents:
        raise ValueError("workspace managed instructions are missing")
    _check_version(command, expected_version, workspace, "OpenSpec")
    return command


def install(workspace: Path, skills_dir: Path, openspec_command: str, openspec_version: str) -> None:
    workspace, skills_dir = workspace.resolve(), Path(os.path.abspath(skills_dir.expanduser()))
    if not workspace.is_dir():
        raise ValueError(f"workspace must be an existing directory: {workspace}")
    router_expected, team_expected = _router_expected(), _inventory(TEAM)
    router_path, team_path = skills_dir / "openspec-model-router", skills_dir / "openspec-development-team"
    agents = workspace / "AGENTS.md"
    for path in (router_path, team_path):
        _safe_parent(path)
    if router_path.is_symlink():
        raise ValueError(f"router installation path must not be a symlink: {router_path}")
    if router_path.exists() and not _installed_match(router_path, router_expected):
        raise ValueError(f"existing router installation differs: {router_path}")
    if team_path.exists() and not _installed_match(team_path, team_expected):
        raise ValueError(f"existing development-team installation differs: {team_path}")
    if not router_path.exists() and router_path.is_symlink():
        raise ValueError(f"broken router installation symlink: {router_path}")
    if not team_path.exists() and team_path.is_symlink():
        raise ValueError(f"broken development-team installation symlink: {team_path}")
    if agents.is_symlink() or (agents.exists() and not agents.is_file()):
        raise ValueError(f"workspace AGENTS.md must be a regular file: {agents}")
    prior = agents.read_bytes() if agents.exists() else None
    command = _cli_path(openspec_command)
    new_agents = _managed_content(prior, _block(workspace, skills_dir, command, openspec_version))
    _check_version(command, openspec_version, workspace, "OpenSpec prerequisite")
    # All content and CLI checks are complete before the first write.
    if not router_path.exists():
        _stage_package(ROUTER, router_path, router_expected)
    if not team_path.exists():
        _stage_package(TEAM, team_path, team_expected)
    if prior != new_agents:
        _atomic_write(agents, new_agents)


def preflight(workspace: Path, skills_dir: Path, openspec_command: str,
              openspec_version: str, project: Path, phase: str, change: str | None,
              project_openspec_command: str | None = None,
              project_openspec_version: str | None = None) -> dict:
    command = _verify(workspace.resolve(), Path(os.path.abspath(skills_dir.expanduser())),
                      openspec_command, openspec_version)
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"selected project must be an existing directory: {project}")
    if project_openspec_command is not None:
        command = _project_cli_path(project_openspec_command, project)
    _check_version(command, project_openspec_version or openspec_version, project,
                   "project OpenSpec")
    context = _run(command, ["context", "--json"], project)
    root = context.get("root")
    root_path = root.get("path") if isinstance(root, dict) else None
    if not isinstance(root_path, str) or not root_path or not Path(root_path).is_absolute():
        raise ValueError("OpenSpec context did not identify a project root")
    if not Path(root_path).is_dir():
        raise ValueError(f"OpenSpec context root does not exist: {root_path!r}")
    report = {"project": str(project), "root": root_path, "phase": phase}
    if phase == "explore":
        return report
    if not change:
        raise ValueError("apply preflight requires --change")
    status = _run(command, ["status", "--change", change, "--json"], project)
    if status.get("changeName") != change:
        raise ValueError(f"OpenSpec status selected {status.get('changeName')!r}, expected {change!r}")
    instructions = _run(command, ["instructions", "apply", "--change", change, "--json"], project)
    if instructions.get("changeName") != change:
        raise ValueError(f"OpenSpec instructions selected {instructions.get('changeName')!r}, expected {change!r}")
    if instructions.get("state") != "ready":
        raise ValueError(f"OpenSpec apply instructions are not ready (state={instructions.get('state')!r})")
    report.update({"change": change, "state": "ready"})
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "verify", "preflight"))
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--openspec-command", default="openspec")
    parser.add_argument("--openspec-version", default=DEFAULT_VERSION)
    parser.add_argument("--project-openspec-command")
    parser.add_argument("--project-openspec-version")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--phase", choices=("apply", "explore"), default="apply")
    parser.add_argument("--change")
    args = parser.parse_args(argv)
    try:
        if args.action != "preflight" and (args.project_openspec_command or args.project_openspec_version):
            raise ValueError("project OpenSpec options apply only to preflight")
        if args.action == "install":
            install(args.workspace, args.skills_dir, args.openspec_command, args.openspec_version)
            print("PASS: reviewed packages and managed workspace instructions installed or already current")
        elif args.action == "verify":
            _verify(args.workspace.resolve(), args.skills_dir.expanduser().absolute(),
                    args.openspec_command, args.openspec_version)
            print("PASS: installed bytes, managed instructions and OpenSpec version verified")
        else:
            if args.project is None:
                raise ValueError("preflight requires --project")
            report = preflight(args.workspace, args.skills_dir, args.openspec_command,
                               args.openspec_version, args.project, args.phase, args.change,
                               args.project_openspec_command, args.project_openspec_version)
            print(json.dumps(report, indent=2))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
