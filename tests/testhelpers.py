from nose.tools import nottest
from operators import Eq
from operators import Expr as Ex
from operators import Exp as E
from operators import Mult as M
from operators import Fraction as F
from operators import Plus as P
from operators import Symbol as S
from operators import Number as N

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

