from nose.tools import nottest

# abbreviated imports for convenient test writing

from parse import EquationParser

p = EquationParser()


@nottest
def test(func, *args, **kwargs):
    """
        Helper function to run a test and print the result to stdout. Nosetests prints this to console in the
        event of failure.
    """
    result = func(*args, **kwargs)
    print result, type(result)
    return result

