# Bounded batch-count evaluation fixture

These are synthetic, standard-library-only replay inputs from the
[2026-10-17 hosted pilot](../../reports/2026-10-17-development-team.md).
They are repository support material, not a runtime skill dependency or a new CI
gate. The scenario adapts `dev-team-specs-cannot-excuse-bug` and
`dev-team-stale-review`; it does not claim to execute those prompts verbatim.

The [public task](public-task.txt), [contract](fixture/CONTRACT.md), and
[rubric](rubric.md) were fixed before implementation. The evaluator authored the
[oracle](evaluator/oracle.py) separately from the implementation and its tests.
The oracle imports and executes a trusted local module; use the supplied fixtures.

Run from this directory:

```sh
python3 -B -m unittest discover -s fixture -p test_batching.py -v
python3 -B evaluator/oracle.py fixture/batching.py
(cd fixture && python3 -B -m doctest -v README.md)
```

Expected results: 11 unit tests, 138 oracle cases, and six doctest examples pass.
These checks reproduce local arithmetic behavior, not the historical model turns.

The controls intentionally fail; run them separately from passing checks:

```sh
python3 -B evaluator/oracle.py controls/initial_stub.py
python3 -B evaluator/oracle.py controls/seeded_batching.py
```

Both commands must exit 1. The initial stub produces 0 passed / 138 failed.
The seeded module produces 107 passed / 31 failed. It is the exact independently
injected source from the pilot: only the return expression changed to
`item_count // batch_size + (item_count > 0)`. Validation stays intact while
positive exact multiples overcount by one. This is a deliberate control, not a
spontaneous failure by the implementation model. Existing implementation tests
also detected it during the recorded run, before the single correction.

No native OpenSpec validation, synchronization, archive, CLI-adapter inference,
or enforced per-role isolation is established by these replay commands.
