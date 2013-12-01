from tests.testhelpers import *
from simplifier import simplify
from parse import parse

def test_solver_mult_basic():
    assert test_generator(simplify(parse('5 * (4 * 3)'))) == 60
    assert test_generator(simplify(parse('5 * (4 * x)'))) == M(20, 'x')
    assert test(simplify, parse('(x * 5) * 4 * 3')) == M(60, 'x')
    assert test(simplify, parse('(x * y * 5) * 4 * 3')) == M(60, 'x', 'y')


def test_solver_mult_combine_symbols():
    assert test(simplify, parse('x * x')) == E('x', 2)
    #assert test(simplify_expr, parse('3 * x * y * 3 * y / (4 * y * x)')) == F(M(9, S('x'), E(S('y'), 2)), M(4, S('y'), S('x'))))


def test_solver_mult_fractions():
    assert test(simplify, parse('5 * (4 / y)')) == F(20, 'y')
    assert test(simplify, parse('4 / x * y * 1 * z')) == F(M(4, 'y', 'z'), 'x')
    assert test(simplify, parse('4 / x * (y / 1) * z')) == F(M(4, 'y', 'z'), 'x')
    assert test(simplify, parse('4 / x * (y * 1) * z')) == F(M(4, 'y', 'z'), 'x')
    assert test(simplify, parse('3 * x / 4 * y')) == F(M(3, 'x', 'y'), 4)


def test_solver_plus():
    assert test_generator(simplify(parse('5 + 4 + 3'))) == 12
    assert test_generator(simplify(parse('5 + x + x + 3'))) == P(8, M(2, 'x'))


if __name__ == "__main__":
    test_solver_mult_basic()
