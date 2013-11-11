from testhelpers import *
from solver import simplify_expr

def test_solver_mult_basic():
    assert test(simplify_expr, p.parse('5 * (4 * 3)')) == Ex(N(60))
    assert test(simplify_expr, p.parse('5 * (4 * x)')) == Ex(M(20, 'x'))
    assert test(simplify_expr, p.parse('(x * 5) * 4 * 3')) == Ex(M(60, 'x'))
    assert test(simplify_expr, p.parse('(x * y * 5) * 4 * 3')) == Ex(M(60, 'x', 'y'))

def test_solver_mult_combine_symbols():
    assert test(simplify_expr, p.parse('x * x')) == Ex(Pow('x', 2))

def test_solver_mult_fractions():
    assert test(simplify_expr, p.parse('5 * (4 / y)')) == Ex(F(20, 'y'))
    assert test(simplify_expr, p.parse('4 / x * y * 1 * z')) == Ex(F(M(4, 'y', 'z'), S('x')))
    assert test(simplify_expr, p.parse('4 / x * (y / 1) * z')) == Ex(F(M(4, 'y', 'z'), S('x')))
    assert test(simplify_expr, p.parse('4 / x * (y * 1) * z')) == Ex(F(M(4, 'y', 'z'), S('x')))
    assert test(simplify_expr, p.parse('3 * x / 4 * y')) == Ex(F(M(3, 'x', 'y'), N(4)))