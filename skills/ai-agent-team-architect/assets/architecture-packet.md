# Architecture packet template

Replace bracketed fields. Omit a table only when it genuinely does not apply and
explain why. These are deliverables, not claims that implementation has occurred.

Workflow: [name]  |  Business owner: [person/role]  |  Revision/date: [value]
Target stage: [design / implementation / supervised pilot / broader automation]
Current state: [proposed / implemented / tested / deployed, with evidence]

## Brief and evidence

| Type | Fact, assumption, or unknown | Source/date | Effect if wrong | Resolution owner |
| --- | --- | --- | --- | --- |
| [fact/assumption/unknown] | [statement] | [source or unavailable] | [impact] | [owner] |

Record business, existing tools, frequency/volume, manual baseline, setup hours,
monthly budget, data restrictions, success criteria, and established authority.

## 1. Workflow to automate first and why

- Trigger, inputs, recipient, completion condition: [values].
- Scope and explicit exclusions: [values].
- Alternatives considered and reason for the choice: [evidence or assumptions].
- Selected mechanism: [deterministic / one agent / team / human assisted].
- Why this complexity is necessary: [specific boundary or measured advantage].
- What remains manual and what not to build: [steps and reasons].

## 2. Team and ownership

| Step/role | Business owner | One job | Inputs → outputs | Tools and scope | Stop/escalate when | Model requirement | Success criterion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [role or deterministic step] | [owner] | [job] | [schemas] | [scope] | [conditions] | [capabilities or N/A] | [observable check] |

Count all agents, including any lead. Identify the orchestrator/state owner and
human approval owner. A one-agent or zero-agent design is acceptable.

## 3. Copyable prompts and task templates

Use [agent-prompt.md](agent-prompt.md) for each agent. Supply actual prompt text,
contract references, good/bad examples, and a task template; role names alone are
not an implementation packet. Record prompt and model/config versions.

## 4. Handoff diagram and contracts

Provide a Mermaid or text diagram with trigger, owners, review, rejection,
approval, external action, completion, and blocked/recovery paths.
Fill [handoff-contract.md](handoff-contract.md) for each boundary. Specify the
authoritative state store and who can advance each state.

## 5. Tools, models, setup, and costs

| Tool/model | Purpose | Integration and setup steps | Permissions/data scope | Owner | Cost basis and source/date | Free/manual alternative |
| --- | --- | --- | --- | --- | --- | --- |
| [existing first] | [step removed] | [concrete steps] | [minimum needed] | [owner] | [verified price or unknown] | [option/limitation] |

Include access prerequisites, budget/time caps, credential references (never
secrets), and how permission/approval enforcement will be checked. Separate a
connector's possible capability from verified installed access.

## 6. Test plan and operating controls

Fill [operations.md](operations.md): memory, review checklist, three failures per
role, retry/stop/recovery rules, and at least five tests including two edge cases.
For each test identify proposed/observed status and evidence. Include a safe way
to test side effects, such as a sandbox or a stubbed destination.

## 7. Launch plan

| Stage / proposed day | Work and accountable owner | Entry condition | Exit evidence | Stop condition and recovery |
| --- | --- | --- | --- | --- |
| Design/setup / 1–2 | [work, owner] | [brief ready] | [contracts, prompts, access design] | [blocker, fallback] |
| Validation / 3–4 | [work, owner] | [implementation ready] | [recorded passing cases] | [failure, fix and rerun] |
| Supervised pilot / 5–6 | [work, owner] | [pilot gates met] | [approved runs and metrics] | [threshold, pause/reconcile] |
| Decision / 7 | [work, owner] | [enough representative evidence] | [continue/revise/stop decision] | [insufficient evidence: extend] |

Revise the timeline for available setup hours and dependencies. Readiness evidence
determines progression; a calendar date is not a release gate.

## 8. Honest economics and weekly measures

Use the formulas in the operating template. State volume, assumptions, estimates
or observations, uncertainty, setup cost, and maintenance effort. Do not claim
positive ROI when unknown or negative. Name an owner and response for each metric.

## 9. Next workflow

[One candidate, dependencies, evidence needed before starting, and why it follows
the first workflow. Say “not yet” when current results do not justify expansion.]

## 10. Common mistakes and prevention

Give five mistakes specific to this design and a concrete prevention for each.
Tie them to the actual controls rather than generic encouragement.

## START HERE FIRST

[One action the user can take today, with an observable result and an owner.]
