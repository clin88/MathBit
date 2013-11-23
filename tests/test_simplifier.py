from testhelpers import *
from simplifier import Simplifier
from output import PrintToConsole

s = Simplifier(PrintToConsole())

def test_solver_mult_basic():
    assert test(s.simplify, p.parse('5 * (4 * 3)')) == Ex(N(60))
    assert test(s.simplify, p.parse('5 * (4 * x)')) == Ex(M(20, 'x'))
    assert test(s.simplify, p.parse('(x * 5) * 4 * 3')) == Ex(M(60, 'x'))
    assert test(s.simplify, p.parse('(x * y * 5) * 4 * 3')) == Ex(M(60, 'x', 'y'))


def test_solver_mult_combine_symbols():
    assert test(s.simplify, p.parse('x * x')) == Ex(E('x', 2))
    #assert test(simplify_expr, p.parse('3 * x * y * 3 * y / (4 * y * x)')) ==\
    #       F(M(9, S('x'), E(S('y'), 2)), M(4, S('y'), S('x'))))


def test_solver_mult_fractions():
    assert test(s.simplify, p.parse('5 * (4 / y)')) == Ex(F(20, 'y'))
    assert test(s.simplify, p.parse('4 / x * y * 1 * z')) == Ex(F(M(4, 'y', 'z'), S('x')))
    assert test(s.simplify, p.parse('4 / x * (y / 1) * z')) == Ex(F(M(4, 'y', 'z'), S('x')))
    assert test(s.simplify, p.parse('4 / x * (y * 1) * z')) == Ex(F(M(4, 'y', 'z'), S('x')))
    assert test(s.simplify, p.parse('3 * x / 4 * y')) == Ex(F(M(3, 'x', 'y'), N(4)))


def test_solver_plus():
    assert test(s.simplify, p.parse('5 + 4 + 3')) == Ex(N(12))
    assert test(s.simplify, p.parse('5 + x + x + 3')) == Ex(P(8, M(2, 'x')))

