# Synthetic batching fixture

This disposable, standard-library Python fixture exposes
`batch_count(item_count: int, batch_size: int) -> int` according to
[CONTRACT.md](CONTRACT.md). It calculates the minimum number of batches needed
for trusted in-process integer counters.

Both arguments must have exactly Python's built-in `int` type. Booleans, integer
subclasses, floats, strings, and other types raise `TypeError`; there is no
coercion. Type validation for both arguments precedes domain validation. A
negative item count or a batch size below one raises `ValueError`, including
an invalid batch size when the item count is zero.

Zero items require zero batches. An exactly full final batch does not add an
empty batch. The result is an exact built-in `int`, including for arbitrary-size
integers, with no floating-point conversion. The function performs deterministic
arithmetic with no external effects or dependencies.

Run these examples from this fixture directory:

```python
>>> from batching import batch_count
>>> batch_count(0, 7)
0
>>> batch_count(7, 7)
1
>>> batch_count(8, 7)
2
>>> batch_count(14, 7)
2
>>> batch_count(10**100 + 1, 10**100)
2

```

Run the regression suite from this fixture directory:

```sh
python3 -B -m unittest discover -s . -p test_batching.py -v
```

From this fixture directory, check the executable examples:

```sh
python3 -B -m doctest -v README.md
```

Tests cover exact input types, validation precedence, domain boundaries, empty
input, full and partial batches, large integers, minimal-capacity invariants,
result type, and repeatability. External-effect absence is also suitable for
source inspection because the implementation contains only built-in type checks,
integer arithmetic, and exception construction.

This fixture is a local behavioral pilot. Native OpenSpec validation, schema
conformance, synchronization, and archive are unavailable/unverified; manual
contract coherence does not establish native OpenSpec execution.
