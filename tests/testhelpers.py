from nose.tools import nottest
from ops import Eq
from ops import Exp as E
from ops import Mult as M
from ops import Frac as F
from ops import Plus as P
from ops import Symbol as S
from ops import Nmbr as N

x = S('x')
y = S('y')
z = S('z')

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
            print("STEP %s, %s" % (result, top))
        except StopIteration as e:
            result = e.value
            break

    print(result, type(result))
    return result

@nottest
def testexpr(func, expr):
    cursor = make_cursor(expr)
    return test_generator(func(cursor))
