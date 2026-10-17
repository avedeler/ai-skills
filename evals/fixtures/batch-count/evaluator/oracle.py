#!/usr/bin/env python3
"""Independent contract oracle; run with the path to a trusted local module."""

import argparse
import importlib.util
import json
import sys


class IntSubclass(int):
    """A value excluded by the contract's exact built-in integer requirement."""


def load_function(path):
    spec = importlib.util.spec_from_file_location("pilot_batching_candidate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load candidate module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, "batch_count")
    if not callable(function):
        raise TypeError("batch_count is not callable")
    return function


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module_path")
    args = parser.parse_args()
    try:
        function = load_function(args.module_path)
    except Exception as error:
        print(json.dumps({"status": "LOAD_ERROR", "error": repr(error)}))
        return 2

    passed = 0
    failed = 0

    def record(case_id, requirement, check):
        nonlocal passed, failed
        try:
            check()
        except Exception as error:
            failed += 1
            print(json.dumps({"case": case_id, "requirement": requirement,
                              "status": "FAIL", "detail": repr(error)}))
        else:
            passed += 1
            print(json.dumps({"case": case_id, "requirement": requirement,
                              "status": "PASS"}))

    def exact(count, size, expected):
        result = function(count, size)
        if type(result) is not int or result != expected:
            raise AssertionError(
                f"batch_count({count!r}, {size!r}) returned {result!r} "
                f"({type(result).__name__}); expected exact int {expected}"
            )

    # Expected constants and independently derived mathematical invariants are
    # intentionally independent of the implementation's quotient expression.
    examples = [
        (0, 1, 0), (0, 7, 0), (1, 7, 1), (6, 7, 1), (7, 7, 1),
        (8, 7, 2), (14, 7, 2), (15, 7, 3), (1, 1, 1), (2, 1, 2),
        (2**80, 1, 2**80), (10**40, 10**20, 10**20),
        (10**40 + 1, 10**20, 10**20 + 1),
    ]
    for index, (count, size, expected) in enumerate(examples, 1):
        record(f"EX-{index:02}", "BC-03/BC-04/BC-05",
               lambda c=count, s=size, e=expected: exact(c, s, e))

    def rejects(count, size, expected_exception):
        try:
            result = function(count, size)
        except expected_exception:
            return
        except Exception as error:
            raise AssertionError(
                f"Expected {expected_exception.__name__}; got {type(error).__name__}"
            ) from error
        raise AssertionError(
            f"Expected {expected_exception.__name__}; returned {result!r}"
        )

    invalid_types = [
        (True, 1), (False, 1), (1, True), (1, False), (1.0, 1),
        (1, 1.0), ("1", 1), (1, "1"), (None, 1), (1, None),
        (IntSubclass(1), 1), (1, IntSubclass(1)), (-1, False),
        (True, 0), (-1, "1"),
    ]
    for index, (count, size) in enumerate(invalid_types, 1):
        record(f"TYPE-{index:02}", "BC-01",
               lambda c=count, s=size: rejects(c, s, TypeError))

    invalid_domains = [(-1, 1), (-100, 3), (0, 0), (1, 0), (3, -2), (-1, 0)]
    for index, (count, size) in enumerate(invalid_domains, 1):
        record(f"DOMAIN-{index:02}", "BC-02",
               lambda c=count, s=size: rejects(c, s, ValueError))

    def invariant(count, size):
        result = function(count, size)
        if type(result) is not int or result < 0:
            raise AssertionError(f"Expected nonnegative exact int; got {result!r}")
        if count == 0:
            if result != 0:
                raise AssertionError(f"Empty input produced {result} batches")
        elif not (result * size >= count and (result - 1) * size < count):
            raise AssertionError(
                f"Capacity/minimality violated for count={count}, size={size}, "
                f"result={result}"
            )

    counts = [0, 1, 2, 6, 7, 8, 13, 14, 15, 99, 100, 101, 10**40 + 3]
    sizes = [1, 2, 3, 7, 10, 100, 10**20]
    for count_index, count in enumerate(counts, 1):
        for size_index, size in enumerate(sizes, 1):
            record(f"INV-{count_index:02}-{size_index:02}", "BC-03/BC-04/BC-05",
                   lambda c=count, s=size: invariant(c, s))

    def monotonic_capacity(count):
        previous = None
        for size in sizes:
            result = function(count, size)
            if type(result) is not int or result < 0:
                raise AssertionError(f"Expected nonnegative exact int; got {result!r}")
            if previous is not None and result > previous:
                raise AssertionError("Increasing capacity increased the batch count")
            previous = result

    for index, count in enumerate(counts, 1):
        record(f"MONO-{index:02}", "BC-04/BC-05",
               lambda c=count: monotonic_capacity(c))

    print(json.dumps({"summary": {"total": passed + failed,
                                  "passed": passed, "failed": failed},
                      "scope": "Functional BC-01..05 only; BC-06/07 need independent review"}))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
