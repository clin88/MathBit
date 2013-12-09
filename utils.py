from collections import Iterable
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

class GenHelper(Iterator):
    """Adds utility functions for working with generators.

    Can be decorated onto generator functions with @genhelper.
    """
    def __init__(self, genf, args, kwargs):
        self._gen = genf(*args, **kwargs)

    def __next__(self):
        return next(self._gen)

    def __iter__(self):
        return self

    def fin(self):
        """Consume entire generator and return return value.
        """
        while True:
            try:
                next(self._gen)
            except StopIteration as e:
                return e.value

def genhelper(f):
    @wraps(f)
    def __(*args, **kwargs):
        return Gen(f, args, kwargs)

    return __

def cat(*iters, type=Iterable):
    """Flattens iters if instance of type.
    """
    unpackif = lambda iter: iter if isinstance(iter, type) else (iter,)
    unpacked = map(unpackif, iters)
    return tuple(chain(*unpacked))