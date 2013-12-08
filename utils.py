from itertools import chain
from collections.abc import Iterable

def fin(generator):
    """
    Returns the return value of a generator while skipping all yields
    """
    while True:
        try:
            next(generator)
        except StopIteration as e:
            return e.value


def replace(cursor, replacement):
    """
    If the focus node of cursor differs from replacement, replace it and yield. Otherwise, return same cursor.
    """
    if cursor.node != replacement:
        cursor = cursor.replace(replacement)
        yield cursor
    return cursor

def cat(*tuples):
    """Since the + operator is overloaded, use this function to concatenate tuples.

    If something is not iterable, make it a tuple.
    """

    makeiter = lambda item: item if isinstance(item, Iterable) else (item,)
    tuples = tuple(map(makeiter, tuples))
    return tuple(chain(*tuples))
