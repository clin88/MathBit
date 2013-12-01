from nose.tools import nottest
from ops import Eq
from ops import Expr as Ex
from ops import Exp as E
from ops import Mult as M
from ops import Fraction as F
from ops import Plus as P
from ops import Symbol as S
from ops import Number as N

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

