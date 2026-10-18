# Research and calibration

Reviewed 2026-10-18. This is a source-backed routing recommendation, not a benchmark of these models on your repositories. Public API capabilities and prices do not guarantee Codex Cloud availability, subscription consumption, or identical runtime behavior. Live tool metadata controls execution.

## Findings and decisions

| Question | Evidence | Recommendation |
| --- | --- | --- |
| Which root? | OpenAI positions Sol 6.1 for demanding, ambiguous agent work [1, 2]. | Keep Sol 6.1 high. Do synthesis and integration in the root instead of paying for a duplicate coordinator. |
| Which architecture model? | Astra is the most capable option; Sol 6.1 is positioned as approaching its performance at lower cost [2, 3]. | Keep Astra high for genuine architectural decisions. Do not send routine design prose or a familiar implementation plan to Astra by default. Evaluate Astra low and Sol high on low-risk architectural comparisons. |
| Which implementation model? | Luna is positioned for focused tasks; Sol for demanding multi-step work [1, 2, 4]. | Keep Luna medium for clear, bounded code; Sol medium for ambiguity. Promote intricate debugging to Sol high. Classify by uncertainty and consequence, not lines changed. |
| Is medium always best for Luna? | Codex subagent guidance suggests Luna high as a starting point, whereas the model API default is medium [1, 4]. | Preserve the user's medium default. Evaluate high for bounded tasks needing deeper tracing; use Sol when uncertainty comes from requirements or interacting systems. Neither recommendation establishes a universal optimum. |
| Is high always needed for Astra? | Codex guidance suggests starting Astra at low, while high is supported [1, 3]. | Keep high for the requested difficult architecture role. Compare low for constrained alternatives before changing the default. |
| Which research model? | Astra supports demanding research; Sol offers a lower-cost complex-work option [2, 3]. | Sol high synthesizes deep research; Luna gathers independently scoped evidence. Use Astra only for unresolved high-consequence reasoning, not merely a long source list. |
| Will more agents save tokens? | OpenAI notes that delegation can add tokens and fits independent scopes better than serial/shared-state work [5]. | Use a small number of bounded scopes and compact briefs. Delegate for expected total-work benefit; avoid blanket fan-out. |
| Should we add more model families? | The preferred three cover distinct capability/cost tiers [2–4]. | No additional default: extra routing complexity needs evidence. An older Sol or a specialized research model is not automatically more efficient or available in the spawn tool. |

The routing table is an engineering inference combining those sources with the user's requested defaults. No primary source establishes that this exact OpenSpec policy is optimal. Effort names are not directly comparable measures of compute across models.

## Cost and token economics

Observed standard API rates per million text tokens, for the short-context pricing band:

| Model | Uncached input | Cached input | Output |
| --- | ---: | ---: | ---: |
| Luna | $0.10 | $0.01 | $0.50 |
| Sol 6.1 | $2.00 | $0.10 | $10.00 |
| Astra | $10.00 | $1.00 | $50.00 |

Sources: [2–4]. Recheck prices before budgeting. Long-context bands, cache writes, tools, service tiers, and regional processing can change costs. API prices are illustrative and must not be presented as Codex plan billing.

At equal uncached token volumes, Luna is 20× cheaper than Sol and Astra is 5× more expensive than Sol. That does not mean equal token consumption or equal task quality. For an illustrative 10,000 input + 2,000 output tokens, base costs are $0.002, $0.04, and $0.20 respectively, excluding all other charges. Repeated failed attempts and root review can erase a routing advantage.

Compare expected completion cost, not just a child call:

```text
E[routed] = child attempt + added handoff/review + P(escalation) × escalation cost
E[direct] = direct execution + its necessary review
```

For those illustrative Luna/Sol volumes, if added coordination cost is H and escalation is one equivalent Sol run, Luna-first is cheaper than a $0.04 direct attempt only if `H + 0.04 × P(escalation) < 0.038`. This is arithmetic, not a measured failure threshold. Verification still must meet the same quality bar. Root context, reasoning tokens, latency, and repair effort matter even when the child is inexpensive.

Token efficiency and dollar efficiency are different objectives. Record both when available, and optimize accepted work with no critical regression. Do not repeatedly re-read the repository or load every supporting skill reference; concise invocation metadata and selective references also reduce context overhead [6].

## OpenSpec and runtime implications

OpenSpec resolves templates, dependencies, and operation instructions from the installed schema; apply is not a generic command to launch arbitrary coders [7, 8]. The router should coordinate the existing workflow rather than replace generated OpenSpec skills. Current Codex integration uses skills, and command spelling differs across clients [9].

Codex skill discovery supports repository `.agents/skills` directories [10]. Checking the skill into each repository is the simplest reproducible Cloud distribution. User-home installations can disappear with disposable environments; a machine-local copy is not an account-wide install. Native collaboration tool availability and per-agent model overrides must be detected on each session. Responses API multi-agent documentation is a different execution surface and cannot establish that a Cloud session supports the same configuration [5].

## Calibration before changing defaults

Build a representative set of completed repository tasks with known acceptance checks: routine edits, bounded search, cross-module implementation, concurrency bugs, proposals, architecture, and research synthesis. Use separate disposable worktrees with the same starting commit, task context, tools, and checks. Do not compare models on different specifications.

Compare the current policy with (a) Sol-only, (b) Luna medium versus high on bounded tasks, and (c) Astra high versus low and Sol high on architecture. Repeat enough times to expose variability; a single success is a smoke test. Blind-review substantive artifacts when practical.

Record accepted completion rate, severity of defects, spec-scenario coverage, model/effort actually used, input/cached/output/reasoning tokens where exposed, total root-plus-child cost, latency, escalations, and human review time. Keep missing telemetry null. Include failed runs rather than excluding them. Promote a cheaper route only when quality remains acceptable on held-out tasks; prefer confidence intervals to a claim of precise savings from a tiny sample.

The bundled evaluation cases check routing behavior and failure handling; they are not quality or cost measurements. No paid multi-model benchmark was run while authoring this package.

## Primary sources

1. [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) — task fit, model/effort guidance, inheritance, custom-agent configuration.
2. [GPT-6.1 Sol model](https://developers.openai.com/api/docs/models/gpt-6.1-sol) — capabilities, efforts, prices.
3. [GPT-6 Astra model](https://developers.openai.com/api/docs/models/gpt-6-astra) — capabilities, efforts, prices.
4. [GPT-6 Luna model](https://developers.openai.com/api/docs/models/gpt-6-luna) — capabilities, efforts, prices.
5. [Responses API multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) — delegation tradeoffs; a distinct API surface.
6. [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — focused descriptions and progressive disclosure.
7. [OpenSpec OPSX workflow](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md) — schema-driven workflow and profiles.
8. [OpenSpec CLI reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md) — status, instructions, validation, archive behavior.
9. [How OpenSpec commands work](https://github.com/Fission-AI/OpenSpec/blob/main/docs/how-commands-work.md) — tool-specific invocation and generated skill locations.
10. [Build skills](https://learn.chatgpt.com/docs/build-skills) — discovery locations and optional metadata.

These are live documentation links, not immutable version pins. Revalidate after a significant model, Codex, or OpenSpec update.
