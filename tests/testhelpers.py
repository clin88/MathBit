from nose.tools import nottest
from core import Symbol as S
from core import Mult as M
from core import Frac as F
from core import Plus as P
from core import Exp as E
from core import Nmbr as N

# tricks my IDE to not removing the above imports:

if False:
    S, M, F, P, E, N


@nottest
def test(func, *args, **kwargs):
    """
        Helper function to run a test and print the result to stdout. Nosetests prints this to console in the
        event of failure.
    """
    result = func(*args, **kwargs)
    print(result, type(result))
    return result


@nottest
def test_generator(generator):
    while True:
        try:
            result = generator.__next__()
            top = result.top()
            print("STEP %s" % top)
        except StopIteration as e:
            result = e.value
            break

    print(result, type(result))
    return result


@nottest
def testexpr(func, expr):
    cursor = make_cursor(expr)
    return test_generator(func(cursor))
