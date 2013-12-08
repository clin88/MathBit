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