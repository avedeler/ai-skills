"""Pure batch planning for trusted, in-process built-in integer counters.

Both arguments must have exactly type int (including no bool or int subclasses).
Type validation precedes domain validation. Counts must be nonnegative and batch
sizes positive. All arithmetic remains exact for arbitrary-size Python integers.
"""


def batch_count(item_count: int, batch_size: int) -> int:
    """Return the minimum batches; zero items require zero batches.

    Raise TypeError for either non-built-in-int argument, then ValueError for
    a negative item_count or a batch_size below one. No coercion or external
    effects occur.
    """
    if type(item_count) is not int or type(batch_size) is not int:
        raise TypeError("item_count and batch_size must be built-in int values")
    if item_count < 0 or batch_size < 1:
        raise ValueError("item_count must be nonnegative and batch_size positive")
    return item_count // batch_size + (item_count > 0)
