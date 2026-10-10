# Repository guidance

This repository contains reusable, vendor- and model-agnostic skills across
multiple categories. Read the relevant package before editing it.

- Keep runtime packages self-contained under `skills/<name>/`. References must
  remain inside the package; examples and evaluation files are repository support
  material and must not be required for a copied skill to work.
- Use `SKILL.md` with `name` and `description` frontmatter. The name matches the
  directory and catalog entry. Prefer decisions and concise procedures in the
  entry point; optional `references/`, `assets/`, and `scripts/` hold detail.
- Update `catalog.json` when adding or renaming a skill. Categories and tags are
  extensible. Do not assume every skill is about AI teams or requires helper files.
- Preserve vendor/model neutrality. Describe required capabilities, not an assumed
  provider, version, client, paid service, or installed integration. Optional
  adapters must be clearly separated from the portable instructions.
- Keep host-specific bindings under `adapters/<skill-name>/`. Load role prompts
  from the canonical skill package instead of maintaining host-specific copies.
  Model selection belongs in adapter settings, not in core role instructions.
- Keep original skills independent of named creators or personas. Preserve creator
  attribution, provenance, and license notices for third-party material; bundle
  those notices inside every package that redistributes it.
- Skills do not grant authority. Respect the user's existing scope and host
  policy without adding redundant approvals for authorized work.
- Do not fabricate tool access, sources, prices, test passes, or deployment status.
  Label synthetic examples and distinguish proposed evaluations from results.
- Add or update `evals/<skill-name>.json` for changed behavior. Keep secrets,
  customer records, and local host state out of commits.
- Use standard-library Python for static validation. Run
  `python3 scripts/validate_skills.py` and appropriate focused checks after edits.
