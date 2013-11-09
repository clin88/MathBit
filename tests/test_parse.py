from parse import *
from operators import *
from decimal import Decimal as D
import solver
from solver import Simplifier
from abbreviated_operations import *

p = EquationParser()

"""
    Parser tests
"""

def test_parse_basic():
    assert p.parse('1 + 2 + 3 + 4') == Ex(P(1, 2, 3, 4))
    assert p.parse('1 * 2 * 3 * 4') == Ex(M(1, 2, 3, 4))
    assert p.parse('2 / 3 / 4') == Ex(F(F(2, 3), 4))
    assert p.parse('2 ^ 3 ^ 4') == Expr(Pow(2, Pow(3, 4)))

def test_parse_nested():
    assert p.parse('1 + (a + b)') == Expr(Plus(1, Plus('a', 'b')))
    assert p.parse('1 + [(a * b) + -4]') == Expr(Plus(1, Plus(Mult('a', 'b'), -4)))

def test_parse_float():
    assert p.parse('-1.234 * x') == Expr(Mult(N('-1.234'), 'x'))

def test_parse_misc():
    assert p.parse('3 * 4 + -5 / 3 ^ 5') == Expr(Plus(Mult(3, 4), Fraction(-5, Pow(3, 5))))

