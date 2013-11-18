from testhelpers import *

p = EquationParser()

"""
    Parser tests
"""


def test_parse_basic():
    assert p.parse('1 + 2 + 3 + 4') == Ex(P(1, 2, 3, 4))
    assert p.parse('1 * 2 * 3 * 4') == Ex(M(1, 2, 3, 4))
    assert p.parse('2 / 3 / 4') == Ex(F(F(2, 3), 4))
    assert p.parse('2 ^ 3 ^ 4') == Ex(E(2, E(3, 4)))


def test_parse_nested():
    assert p.parse('1 + (a + b)') == Ex(P(1, P('a', 'b')))
    assert p.parse('1 + [(a * b) + -4]') == Ex(P(1, P(M('a', 'b'), -4)))


def test_parse_float():
    assert p.parse('-1.234 * x') == Ex(M(N('-1.234'), 'x'))


def test_parse_misc():
    assert p.parse('3 * 4 + -5 / 3 ^ 5') == E(P(M(3, 4), F(-5, E(3, 5))))


def test_parse_equals():
    assert p.parse('3 = 4') == Ex(Eq(3, 4))
    assert p.parse('3 ^ 2 = 6') == Ex(Eq(P(3, 2), 6))