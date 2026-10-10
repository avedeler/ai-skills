# Portability requirements

The core skill is a portable set of task instructions. A host may add discovery,
tools, permissions, storage, or execution, but none is assumed merely because
the skill exists.

## Vendor and model independence

- Describe capabilities such as structured output, source comparison, image
  interpretation, or tool use before selecting a model. Specific availability,
  quality, context limits, and prices must be verified in the user's environment.
- Do not name a required provider, model version, assistant application, agent
  framework, or paid service in core instructions. Optional examples or adapters
  must not become hidden requirements.
- Choose integrations by input/output contract, required permissions, and failure
  behavior. Offer a manual or generic file-based path when practical.
- Use plain text, Markdown, JSON, and ordinary relative files where appropriate.
  A skill may specify another open format when its domain calls for it.
- Do not assume cross-model behavior is identical. Re-evaluate representative
  cases when model, prompt, host, or integration behavior changes.

## Host boundaries

A description of a tool is not proof that it is installed or authorized. Discover
available capabilities and respect actual access controls. Skill text cannot
grant permission, bypass approval, or guarantee prompt-injection resistance.
Carry over sufficient authorization from the user's request; do not repeatedly
ask for the same approval. Consequential unknowns should block only dependent work.

Helpers in `scripts/` are optional unless explicitly documented as prerequisites.
State their inputs, outputs, dependencies, external effects, and failure modes.
Prefer deterministic checks over model judgment for schema and arithmetic.

## Honest evidence

Keep facts, assumptions, unknowns, and observed results distinct. Do not turn a
proposed test into a pass or an architecture into a deployed system. Give enough
source/version context for another model or human to verify the result. Original
instructions must not depend on a named creator or persona. Credit third-party
creators and preserve their licenses; attribution is provenance, not a required
runtime, model, or provider.
