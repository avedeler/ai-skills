# Approved synthetic contract

This disposable fixture models batch planning for trusted, in-process integer
counters. It is not a service, parser, file processor, or production application.

The public API is `batch_count(item_count: int, batch_size: int) -> int` in
`batching.py`. The following requirements are fixed for this pilot.

- **BC-01 — Inputs:** both arguments must have exactly Python's built-in `int`
  type. Reject booleans, integer subclasses, and all other types with `TypeError`.
  This check precedes domain validation. Do not coerce values.
- **BC-02 — Domain:** reject a negative `item_count` or a `batch_size` below one
  with `ValueError`.
- **BC-03 — Empty input:** zero items require exactly zero batches.
- **BC-04 — Capacity:** for positive counts, return the least nonnegative integer
  `n` such that `n * batch_size >= item_count`. A full final batch does not require
  an additional empty batch. In particular, `batch_count(7, 7) == 1`,
  `batch_count(8, 7) == 2`, and `batch_count(14, 7) == 2`.
- **BC-05 — Integer fidelity:** return an exact built-in `int`, and preserve this
  behavior for arbitrary-size Python integers. Do not convert to floating point.
- **BC-06 — Scope and effects:** this is deterministic pure arithmetic. It must
  perform no network, filesystem, environment, process, or other external effects,
  and it must add no dependencies.
- **BC-07 — Coherence:** the module documentation, README examples, implementation,
  and regression tests must agree with BC-01 through BC-06. Preserve this approved
  contract rather than changing it to excuse an implementation defect.

Native OpenSpec validation, schema conformance, synchronization, and archive are
outside the available capabilities. A manual comparison against this contract
does not establish that any native OpenSpec operation ran or passed.
