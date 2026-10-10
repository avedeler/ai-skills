# AI Skills

A reusable library of skills for AI-assisted work. Skills are organized by
category and packaged as portable `SKILL.md` directories. They do not require a
particular AI vendor, model, assistant application, or agent framework.

## Available skills

| Category | Skill | Purpose |
| --- | --- | --- |
| AI systems | [ai-agent-team-architect](skills/ai-agent-team-architect/SKILL.md) | Design one business workflow, choose the smallest useful architecture, and specify prompts, handoffs, tools, costs, tests, and rollout |
| AI systems | [ai-agent-team-review](skills/ai-agent-team-review/SKILL.md) | Review a proposed or running workflow, identify failure and evidence gaps, and assess readiness for the next stage |

The machine-readable [catalog](catalog.json) is the discovery index. It supports
AI systems, software engineering, research, writing, data analysis, operations,
and additional categories without changing the skill format. Categories with no
entries reserve space for future work; they do not imply those skills exist yet.

## Use a skill

1. Select a skill from the catalog and copy its **entire directory**, including
   any bundled references, assets, or scripts.
2. Place it in your assistant's documented skill location or import the package.
   Discovery paths and supported features vary by host; check your host's docs.
3. Load the registered skill name and describe the task. If your assistant does
   not support skill discovery, provide `SKILL.md` and the files it references as
   context instead.

Check for existing packages before copying and preserve local changes. Reload
the host if it caches discovery. Restricted installations may require a catalog
or policy update by their operator. Loading a skill does not grant permissions,
install tools, or authorize external actions.

For example, load `ai-agent-team-architect` and ask:

> Design a workflow for turning approved product notes into a weekly newsletter.
> We have a document workspace, an email platform, four setup hours, and a $75
> monthly budget. A human must approve every send. Ask for missing information,
> then produce the implementation packet.

Load `ai-agent-team-review` when a design or pilot is ready to inspect:

> Review this workflow for a supervised pilot. Inspect the design, prompts,
> permissions, test results, and costs. Separate design gaps from implementation
> failures and identify the smallest useful next action.

These two skills create plans and reviews. They can guide authorized
implementation, but a plan alone does not deploy an agent team. See the
[worked synthetic example](examples/ai-systems/newsletter-workflow.md) for the
expected artifacts and an honest treatment of untested assumptions.

## Repository structure

```text
catalog.json                 # Categories and skill discovery metadata
skills/<skill-name>/
  SKILL.md                   # Required entry point and trigger description
  references/                # Optional detailed guidance
  assets/                    # Optional reusable templates and fixtures
  scripts/                   # Optional bounded helper programs
templates/                   # Starter files for new skills and evaluations
examples/<category>/         # Worked examples; not runtime dependencies
evals/<skill-name>.json       # Behavioral evaluation scenarios per skill
scripts/validate_skills.py   # Dependency-free catalog/package validation
docs/                        # Format and portability guidance
```

Packages use a flat directory of globally unique names so they can be copied to
hosts that discover immediate child directories. Categories and tags provide
organization without changing runtime paths. A skill may contain only `SKILL.md`;
additional directories are optional and added when useful.

## Add another type of skill

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and the
[skill starter](templates/skill/SKILL.md). Register the new package in
`catalog.json`, choose an existing category or add one, and add evaluation
scenarios. Writing, research, coding, and operational skills follow the same
contract; domain-specific guidance stays inside their own packages.

See [catalog format](docs/catalog.md) and
[portability requirements](docs/portability.md). Avoid fixed model versions,
vendor-specific APIs, or required paid services in core skills. If a task needs
an integration, describe the capability contract and make any concrete adapter
optional and explicit.

## Validate and evaluate

Python 3.10 or newer is sufficient for static validation:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

The validator checks the catalog, skill metadata, bundled references, local
Markdown links, and evaluation fixture shape. It runs in repository CI as well.
It does not invoke a model, install packages, or contact external services.

Behavioral scenarios are **test specifications**, not recorded passes. Follow
the [evaluation guide](evals/README.md) in your actual host. Static checks do not
establish model behavior, integration access, or business results.
