# Catalog format

`catalog.json` is the machine-readable discovery index. The current format is
version 1. A format change requires a version bump and matching validator/docs
updates; adding categories or skills does not.

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | integer | Format version, currently `1` |
| `categories` | object | Category IDs mapped to `title` and `description` strings |
| `skills` | array | Skill records with `name`, `path`, `category`, and `tags` |

Each skill record uses:

- `name`: globally unique lowercase letters/digits separated by single hyphens,
  at most 64 characters; matches the package directory and frontmatter.
- `path`: exactly `skills/<name>`, relative to repository root.
- `category`: an existing category ID. Choose one primary category; tags cover
  cross-cutting concerns.
- `tags`: one or more unique lowercase hyphenated labels. Tags are descriptive,
  not a hard-coded taxonomy.

Categories use the same lowercase hyphenated ID syntax. Each has a nonempty title
and description. Empty categories are allowed as future organization points.
Every package under `skills/` must be registered exactly once; every registration
must resolve to a package. Every skill has an evaluation file at
`evals/<name>.json`, containing scenarios that name that skill.

## Package format

The only required runtime file is `SKILL.md`. Use a simple YAML frontmatter block
with `name` and a precise, single-line `description` describing task triggers and
exclusions. The current validator supports unquoted single-line strings without
YAML-ambiguous `: ` or ` #` sequences. Keep descriptions at most 1,024 characters.
The rest of the file is Markdown instructions.

Optional runtime files belong in the package's `references/`, `assets/`, or
`scripts/` directories. Link them using relative Markdown links. Runtime links
must remain inside that package; copying a package must not silently break it.
External sources may supplement instructions, but mandatory facts needed to
execute the skill should be bundled or explicitly identified as a prerequisite.

The validator checks package metadata, registration, local link targets, and
scenario structure. It does not validate external URLs, Markdown anchor targets,
or semantic correctness. Instructions still require review and evaluation.
