#!/usr/bin/env python3
"""Validate catalog structure, portable skill packages, links, and scenarios.

Uses only Python's standard library. Does not execute skill scripts, call models,
check external URLs, or establish behavioral correctness.
"""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def slug(value: object) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value))


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def read_json(path: Path, errors: list[str]) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: cannot read JSON: {exc}")
        return None


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    catalog = read_json(root / "catalog.json", errors)
    if not isinstance(catalog, dict):
        return errors + ["catalog.json: expected an object"]
    if type(catalog.get("schema_version")) is not int or catalog["schema_version"] != 1:
        errors.append("catalog.json: unsupported schema_version; expected 1")
    if set(catalog) != {"schema_version", "categories", "skills"}:
        errors.append("catalog.json: expected schema_version, categories, and skills fields")
    categories = catalog.get("categories")
    if not isinstance(categories, dict) or not categories:
        errors.append("catalog.json: categories must be a nonempty object")
        categories = {}
    for category, metadata in categories.items():
        if not slug(category) or not isinstance(metadata, dict):
            errors.append(f"catalog.json: invalid category {category!r}")
        elif set(metadata) != {"title", "description"} or not all(nonempty(v) for v in metadata.values()):
            errors.append(f"catalog.json: category {category} needs title and description")

    records = catalog.get("skills")
    if not isinstance(records, list) or not records:
        errors.append("catalog.json: skills must be a nonempty array")
        records = []
    registered: set[str] = set()
    for index, record in enumerate(records, 1):
        label = f"catalog skill {index}"
        if not isinstance(record, dict):
            errors.append(f"{label}: expected an object")
            continue
        if set(record) != {"name", "path", "category", "tags"}:
            errors.append(f"{label}: expected name, path, category, and tags")
        name = record.get("name")
        if not slug(name) or len(name) > 64:
            errors.append(f"{label}: invalid name")
            continue
        if name in registered:
            errors.append(f"{label}: duplicate name {name}")
        registered.add(name)
        if record.get("path") != f"skills/{name}":
            errors.append(f"{label}: path must be skills/{name}")
        category = record.get("category")
        if not isinstance(category, str) or category not in categories:
            errors.append(f"{label}: unknown category {category!r}")
        tags = record.get("tags")
        if not isinstance(tags, list) or not tags or not all(slug(tag) for tag in tags):
            errors.append(f"{label}: tags must be nonempty slug strings")
        elif len(tags) != len(set(tags)):
            errors.append(f"{label}: duplicate tags")

    packages = sorted((root / "skills").glob("*/SKILL.md"))
    discovered = {path.parent.name for path in packages}
    for name in sorted(registered - discovered):
        errors.append(f"{name}: registered package has no SKILL.md")
    for name in sorted(discovered - registered):
        errors.append(f"{name}: package missing from catalog")
    for directory in (root / "skills").glob("*"):
        if directory.is_dir() and not (directory / "SKILL.md").is_file():
            errors.append(f"{directory.name}: skill directory has no SKILL.md")

    for path in packages:
        label = path.relative_to(root)
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{label}: cannot read skill: {exc}")
            continue
        match = re.match(r"\A---\n(.*?)\n---\n(.*\S.*)\Z", content, re.S)
        if not match:
            errors.append(f"{label}: missing frontmatter or skill body")
            continue
        fields: dict[str, str] = {}
        for line in match[1].splitlines():
            field = re.fullmatch(r"([a-z-]+): (.+)", line)
            if not field:
                errors.append(f"{label}: use one-line YAML string fields")
                continue
            key, value = field.groups()
            if key in fields:
                errors.append(f"{label}: duplicate field {key}")
            fields[key] = value
            if ": " in value or " #" in value or value.startswith(('"', "'", "[", "{", "|", ">")):
                errors.append(f"{label}: use an unambiguous plain YAML scalar")
        if set(fields) != {"name", "description"}:
            errors.append(f"{label}: expected only name and description metadata")
        name = fields.get("name", "")
        if not slug(name) or len(name) > 64 or name != path.parent.name:
            errors.append(f"{label}: name must be valid and match the directory")
        description = fields.get("description", "")
        if not nonempty(description) or len(description) > 1024:
            errors.append(f"{label}: description must contain 1–1024 characters")

    for path in sorted(root.rglob("*.md")):
        if ".git" in path.relative_to(root).parts:
            continue
        label = path.relative_to(root)
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{label}: cannot read Markdown: {exc}")
            continue
        content = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", content, flags=re.M | re.S)
        package = next((p.parent for p in packages if path.is_relative_to(p.parent)), None)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            target = target.strip().strip("<>")
            try:
                parsed = urlsplit(target)
            except ValueError:
                errors.append(f"{label}: malformed link: {target}")
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root):
                errors.append(f"{label}: link escapes repository: {target}")
            elif not destination.exists():
                errors.append(f"{label}: missing local link: {target}")
            elif package and not destination.is_relative_to(package):
                errors.append(f"{label}: runtime link escapes skill package: {target}")

    eval_paths = sorted((root / "evals").glob("*.json"))
    eval_names = {path.stem for path in eval_paths}
    for name in sorted(registered - eval_names):
        errors.append(f"{name}: missing evals/{name}.json")
    ids: set[str] = set()
    for path in eval_paths:
        if path.stem not in registered:
            errors.append(f"{path.name}: evaluation file has no registered skill")
        scenarios = read_json(path, errors)
        if not isinstance(scenarios, list) or not scenarios:
            errors.append(f"{path.name}: expected a nonempty scenario array")
            continue
        for index, scenario in enumerate(scenarios, 1):
            label = f"{path.name} scenario {index}"
            if not isinstance(scenario, dict):
                errors.append(f"{label}: expected an object")
                continue
            for field in ("id", "skill", "prompt"):
                if not nonempty(scenario.get(field)):
                    errors.append(f"{label}: missing string {field}")
            identifier = scenario.get("id")
            if isinstance(identifier, str):
                if identifier in ids:
                    errors.append(f"{label}: duplicate scenario id {identifier}")
                ids.add(identifier)
            if scenario.get("skill") != path.stem:
                errors.append(f"{label}: skill must match evaluation filename")
            for field in ("expected_behaviors", "forbidden_behaviors"):
                values = scenario.get(field)
                if not isinstance(values, list) or not values or not all(nonempty(v) for v in values):
                    errors.append(f"{label}: {field} must be nonempty strings")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root.resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    packages = list((root / "skills").glob("*/SKILL.md"))
    print(f"PASS: catalog, {len(packages)} skill packages, Markdown links, and evaluation fixtures")
    print("Static validation only; model behavior and live integrations were not tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
