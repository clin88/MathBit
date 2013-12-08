from ops import Plus as P
from ops import Mult as M
from ops import Frac as F
from ops import Exp as E
from ops import Eq
from parse import parse
from decimal import Decimal as D
"""
    Parser tests
"""

def test_parse_basic():
    assert parse('1 + 2 + 3 + 4') == P(1, 2, 3, 4)
    assert parse('1 * 2 * 3 * 4') == M(1, 2, 3, 4)
    assert parse('2 / 3 / 4') == F(F(2, 3), 4)
    assert parse('2 ^ 3 ^ 4') == E(2, E(3, 4))


def test_parse_nested():
    assert parse('1 + (a + b)') == P(1, P('a', 'b'))
    assert parse('1 + [(a * b) + -4]') == P(1, P(M('a', 'b'), -4))


def test_parse_float():
    assert parse('-1.234 * x') == M(D('-1.234'), 'x')


def test_parse_misc():
    assert parse('3 * 4 + -5 / 3 ^ 5') == P(M(3, 4), F(-5, E(3, 5)))


def test_parse_equals():
    assert parse('3 = 4') == Eq(3, 4)
    assert parse('3 ^ 2 = 6') == Eq(P(3, 2), 6)