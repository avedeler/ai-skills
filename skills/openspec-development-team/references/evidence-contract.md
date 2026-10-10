# Evidence packet and readiness checker

The bundled checker is an optional, dependency-free consistency check. It neither
dispatches agents nor runs tests. It cannot authenticate a review, inspect the
meaning of a spec, or prove that a supplied result is true. Integrate it only after
the coordinating host supplies trusted policy, candidate identity, and receipts.
An agent-editable passing JSON file is not an enforcement or authorization boundary.

## Inputs

- [policy.example.json](../assets/policy.example.json): reviewed required check
  IDs, required requirement/scenario pairs, security and spec-sync obligations,
  and the correction cap. Store the real policy under the target project's normal
  change controls. Workers cannot delete obligations merely to make this pass.
- [evidence.example.json](../assets/evidence.example.json): a **synthetic fixture**
  showing the expected shape. It is rejected unless fixture mode is explicit.
- Expected candidate: `sha256:` plus a 64-character lowercase hex content digest,
  provided by the trusted snapshot adapter. The script does not compute it.

The host adapter must bind the digest to source/tests/config, relevant OpenSpec and
documentation snapshots, and substantive delivery claims. It should collect real
job/command receipts, session provenance, and task/spec state from their original
sources. Recomputing a candidate or refreshing evidence must not reset correction
counters. Existing OpenSpec tasks and runtime state remain authoritative; this is
a derived readiness report, not a second task database.

## Contract

Both inputs have `schema_version: 1`. The packet explicitly marks `synthetic`,
names its `candidate`, and lists the actual `author_sessions`. Required sections:

| Section | Required evidence |
| --- | --- |
| `planning`, `tasks` | Candidate, `status: passed`, evidence of complete applicable artifacts/tasks |
| `checks` | Every policy check ID with candidate, `status: passed`, nonempty raw evidence and integer `exit_code: 0` |
| `traceability` | Each required scenario exactly once, linked to a required check, test/acceptance ref, and documentation ref or explicit N/A reason |
| `code_review` | Passing receipt with candidate, evidence and a session outside `author_sessions` |
| `security` | Candidate, complete triage, rationale and trigger list; independent passing review when policy requires it or any trigger exists |
| `documentation` | Passing candidate-bound coherence evidence |
| `spec_sync` | Delta count and candidate; verified result, zero remaining deltas and clean second comparison when required; justified N/A only with no deltas and policy permitting it |
| `findings` | All material findings closed with closure evidence; unknown severity/status rejected |
| `correction` | Persistent failed-round count below the stop limit and no stalled progress; zero failures is allowed when repairs are disabled |

Passing receipt fields are `candidate`, `status`, and `evidence`; executed checks
also require `exit_code`, and independent reviews require `session_id`. Check
names are host-defined, not fixed to one test runner. A manual acceptance check
can be normalized by a trusted adapter to a successful check receipt; never invent
an exit code for an unperformed manual check. Keep its actual evidence and origin.

The checker enforces equality of supplied candidate IDs. It does not follow URLs,
read raw evidence files, verify signatures, independently classify security risk,
or detect an omitted requirement/finding not present in the trusted inputs. The
independent reviewers and host integration remain necessary.

## Run the synthetic demonstration

From this skill directory, with Python 3.10 or newer:

```sh
python3 scripts/check_readiness.py \
  --policy assets/policy.example.json \
  --packet assets/evidence.example.json \
  --expected-candidate sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  --allow-synthetic
```

Without `--allow-synthetic`, the fixture must fail. Replace the inputs and expected
candidate with actual host-collected data for a real consistency check. Exit codes
are `0` for consistent, `1` for readiness gaps, and `2` for unreadable/invalid JSON.
No result authorizes merge, deployment, permission changes, or archive.
