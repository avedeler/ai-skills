"""Regression checks for the approved BC-01 through BC-06 behavior."""

import unittest
from decimal import Decimal
from fractions import Fraction

from batching import batch_count


class IntSubclass(int):
    pass


class ConversionTrap:
    def __int__(self):
        raise AssertionError("must not coerce")

    def __index__(self):
        raise AssertionError("must not coerce")

    def __lt__(self, other):
        raise AssertionError("must reject type before comparing")


class BatchCountTests(unittest.TestCase):
    def test_empty(self):
        for size in (1, 7, 10**1000):
            with self.subTest(size_bits=size.bit_length()):
                self.assertEqual(batch_count(0, size), 0)

    def test_contract_examples(self):
        for count, size, expected in ((7, 7, 1), (8, 7, 2), (14, 7, 2)):
            with self.subTest(count=count, size=size):
                self.assertEqual(batch_count(count, size), expected)

    def test_boundary_examples(self):
        for count, size, expected in ((1, 7, 1), (6, 7, 1), (13, 7, 2),
                                      (15, 7, 3), (1, 1, 1), (50, 1, 50)):
            with self.subTest(count=count, size=size):
                self.assertEqual(batch_count(count, size), expected)

    def test_rejects_non_builtin_ints_in_either_argument(self):
        invalid = (True, False, IntSubclass(3), 3.0, "3", b"3", None,
                   [], {}, Decimal(3), Fraction(3), ConversionTrap())
        for value in invalid:
            for args in ((value, 7), (7, value)):
                with self.subTest(value_type=type(value).__name__, position=0 if args[0] is value else 1):
                    with self.assertRaises(TypeError):
                        batch_count(*args)

    def test_type_checks_precede_domain_validation(self):
        for args in ((-1, True), (-1, 0.0), (None, 0),
                     (ConversionTrap(), -1), (-1, ConversionTrap())):
            with self.subTest(args_types=tuple(type(x).__name__ for x in args)):
                with self.assertRaises(TypeError):
                    batch_count(*args)

    def test_negative_items(self):
        for count in (-1, -7, -(10**1000)):
            with self.subTest(count_bits=count.bit_length()):
                with self.assertRaises(ValueError):
                    batch_count(count, 7)

    def test_nonpositive_batch_size_even_for_empty_items(self):
        for count in (0, 1, 7):
            for size in (0, -1, -(10**1000)):
                with self.subTest(count=count, size_bits=size.bit_length()):
                    with self.assertRaises(ValueError):
                        batch_count(count, size)

    def test_exact_builtin_result_type(self):
        for count, size in ((0, 7), (1, 7), (14, 7), (10**1000, 3)):
            self.assertIs(type(batch_count(count, size)), int)

    def test_large_integers_around_exact_multiple(self):
        size = 10**1000 + 7
        quotient = 10**600 + 13
        for count, expected in ((size * quotient - 1, quotient),
                                (size * quotient, quotient),
                                (size * quotient + 1, quotient + 1)):
            self.assertEqual(batch_count(count, size), expected)
        self.assertEqual(batch_count(2**53 + 1, 1), 2**53 + 1)

    def test_minimal_capacity_invariant(self):
        for count in range(151):
            for size in range(1, 26):
                result = batch_count(count, size)
                self.assertGreaterEqual(result, 0)
                self.assertGreaterEqual(result * size, count)
                if result:
                    self.assertLess((result - 1) * size, count)

    def test_repeatability(self):
        inputs = ((0, 9), (8, 7), (10**1000, 7))
        first = [batch_count(*args) for args in inputs]
        self.assertEqual([batch_count(*args) for args in reversed(inputs)], first[::-1])


if __name__ == "__main__":
    unittest.main()
