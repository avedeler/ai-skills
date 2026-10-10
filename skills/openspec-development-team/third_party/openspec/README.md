# OpenSpec attribution

This package builds on **OpenSpec**, developed by **Fission AI and the OpenSpec
contributors** at [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec).
OpenSpec's workflow and skills are upstream work, not inventions of this package.

**Copyright (c) 2024 OpenSpec Contributors.** OpenSpec is licensed under the
[MIT License](LICENSE); the complete upstream license is included unchanged.
The upstream skill metadata identifies its author as `openspec` and license as MIT.

## Workflow and skill sources

The team adapts the following OpenSpec workflows into dedicated role assignments.
These links identify the upstream skills at the attribution reference revision
`9111a7654d7800391459431fff4eaf66e33a3d2e`:

| Upstream skill | Use in this package |
| --- | --- |
| [openspec-propose](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/skills/openspec-propose/SKILL.md) | [Planner](../../assets/agents/planner.md): proposal, requirements, design and tasks |
| [openspec-apply-change](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/skills/openspec-apply-change/SKILL.md) | [Implementer](../../assets/agents/implementer.md): implement scoped tasks and report progress |
| [openspec-update-change](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/skills/openspec-update-change/SKILL.md) | [Planner](../../assets/agents/planner.md): reconcile planning artifacts after decisions change |
| [openspec-verify-change](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/skills/openspec-verify-change/SKILL.md) | [Code reviewer](../../assets/agents/code-reviewer.md): implementation/artifact conformance |
| [openspec-sync-specs](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/skills/openspec-sync-specs/SKILL.md) | [Documentation/spec steward](../../assets/agents/documentation-steward.md): delta-to-canonical spec synchronization |
| [openspec-archive-change](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/skills/openspec-archive-change/SKILL.md) | [Lifecycle](../../references/lifecycle.md): archive after verified completion and authorization |

The dedicated role prompts, orchestration, testing/correction policies and
readiness checker are local integration work. They are not verbatim copies of
the upstream skills. No upstream CLI or generated `SKILL.md` files are bundled
in this directory; the license and source provenance are bundled here.

Use the target repository's installed, version-appropriate OpenSpec workflows as
described in [the adapter](../../references/lifecycle.md). The pinned links record
where attribution was verified; they do not require that runtime version, claim
that it was the original integration source revision, or authorize an automatic
download or installation. Other schema-supported workflows may be used when
present in the target repository.

## Preservation and updates

[UPSTREAM.json](UPSTREAM.json) records the reference revision, source paths,
checksums and scope of reuse. Preserve this notice and the full license when
copying or redistributing the team package or its OpenSpec-derived instructions.
When copying individual role prompts, include the linked attribution and license.
Future direct imports must record their actual revision and any modifications
and retain applicable notices. This notice covers OpenSpec material; it does not
assign OpenSpec's license to unrelated local code or imply upstream endorsement.
