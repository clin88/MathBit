from parse import *
from operators import *


p = EquationParser()
def test__parse_basic():
    assert p.parse('1 + 2 + 3 + 4') == Plus(1, 2, 3, 4)
    assert p.parse('1 * 2 * 3 * 4') == Mult(1, 2, 3, 4)
    assert p.parse('2 / 3 / 4') == Fraction(Fraction(2, 3), 4)
    assert p.parse('2 ^ 3 ^ 4') == Pow(2, Pow(3, 4))

def test__parse_nested():
    assert p.parse('1 + (a + b)') == Plus(1, Brackets(Plus('a', 'b')))
    assert p.parse('1 + [(a * b) + -4]') == Plus(1, Brackets(Plus(Brackets(Mult('a', 'b')), -4)))

def test__parse_float():
    assert p.parse('-1.234 * x') == Mult(-1.234, 'x')

def test__parse_misc():
    assert p.parse('3 * 4 + -5 / 3 ^ 5') == Plus(Mult(3, 4), Fraction(-5, Pow(3, 5)))