# Contributing

## Add a skill

1. Choose a specific task, a lowercase hyphenated name, and a category. Check the
   catalog for overlap before creating another entry point.
2. Copy [templates/skill/SKILL.md](templates/skill/SKILL.md) to
   `skills/<name>/SKILL.md`. Replace its metadata and instructional placeholders.
3. Define when the skill applies, what information it needs, its decision process,
   output contract, boundaries, failure handling, and completion criteria.
4. Add `references/`, `assets/`, or `scripts/` only when needed. Keep all runtime
   links inside the skill directory. A plain `SKILL.md` package is supported.
5. Add a catalog entry with `name`, `path`, `category`, and useful `tags`. Add a
   category definition when none fits; the validator does not hard-code categories.
6. Copy [templates/evaluation.json](templates/evaluation.json) to
   `evals/<name>.json`. Provide realistic positive, boundary, and failure scenarios.
7. Add a worked example under `examples/<category>/` when it materially helps
   readers. Label invented inputs and outputs as synthetic. Update the README's
   available-skills table.
8. Run static validation and relevant behavioral evaluations. Report what ran,
   what passed, and what remains untested.

## Portability and scope

Follow [portability requirements](docs/portability.md). Core skills must work
without a particular provider, model, host, paid service, or agent framework.
Use capability requirements and explicit input/output contracts. Do not assume
that planning a workflow authorizes executing it. Preserve existing authorization
and avoid redundant approval prompts.

Keep original skills independent of a persona or individual. Third-party skills
must retain creator attribution and applicable license notices. Pin imported
material to an immutable revision, record its source and local modifications,
and include its license and provenance inside the consuming package so they
travel with copies. Update [third-party notices](THIRD_PARTY_NOTICES.md) when
adding or changing an import. Separate synthetic examples from real results.

## Review changes

Describe the trigger, resulting behavior, and evidence. For renamed skills,
update the directory, frontmatter, catalog, links, evaluation filename and scenario
targets together. Check whether users need to move an installed directory.

Use [the evaluation guide](evals/README.md) for decision, permission, or output
changes. Static checks alone are insufficient for behavioral claims. Model-hosted
evaluation runs are optional until explicitly authorized and available; identify
unrun cases without presenting them as passes.

Run:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

The CI workflow runs the same dependency-free check. Add dependencies only when
they have a concrete benefit and documented installation requirements.

Optional host adapters live under `adapters/<skill-name>/` and reference the core
package. Keep native registration, model selection and launch configuration there;
do not duplicate role prompts, workflow decisions or third-party material. Use
Python 3.11+ for the full repository test suite. Document verified host versions
and distinguish native configuration checks from a live agent pilot.
