from testhelpers import *
from solver import simplify_expr


def test_solver_mult_basic():
    assert test(simplify_expr, p.parse('5 * (4 * 3)')) == N(60)
    assert test(simplify_expr, p.parse('5 * (4 * x)')) == M(20, 'x')
    assert test(simplify_expr, p.parse('(x * 5) * 4 * 3')) == M(60, 'x')
    assert test(simplify_expr, p.parse('(x * y * 5) * 4 * 3')) == M(60, 'x', 'y')


def test_solver_mult_combine_symbols():
    assert test(simplify_expr, p.parse('x * x')) == E('x', 2)
    #assert test(simplify_expr, p.parse('3 * x * y * 3 * y / (4 * y * x)')) ==\
    #       F(M(9, S('x'), E(S('y'), 2)), M(4, S('y'), S('x'))))


def test_solver_mult_fractions():
    assert test(simplify_expr, p.parse('5 * (4 / y)')) == F(20, 'y')
    assert test(simplify_expr, p.parse('4 / x * y * 1 * z')) == F(M(4, 'y', 'z'), S('x'))
    assert test(simplify_expr, p.parse('4 / x * (y / 1) * z')) == F(M(4, 'y', 'z'), S('x'))
    assert test(simplify_expr, p.parse('4 / x * (y * 1) * z')) == F(M(4, 'y', 'z'), S('x'))
    assert test(simplify_expr, p.parse('3 * x / 4 * y')) == F(M(3, 'x', 'y'), N(4))


def test_solver_plus():
    assert simplify_expr(p.parse('5 + 4 + 3')) == N(12)
    assert simplify_expr(p.parse('5 + x + x + 3')) == P(8, M(2, 'x'))