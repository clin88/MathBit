from tests.testhelpers import *
from simplify import simplify, evalexpr


def test_solver_mult_basic():
    assert test_generator(simplify('5 * (4 * 3)')) == 60
    assert test_generator(simplify('5 * (4 * x)')) == M(20, 'x')
    assert test_generator(simplify('(x * 5) * 4 * 3')) == M(60, 'x')
    assert test_generator(simplify('(x * y * 5) * 4 * 3')) == M(60, 'x', 'y')


def test_solver_mult_combine_symbols():
    assert test_generator(simplify('x * x')) == E('x', 2)
    #assert test(simplify_expr, '3 * x * y * 3 * y / (4 * y * x)')) == F(M(9, S('x'), E(S('y'), 2)), M(4, S('y'), S('x'))))


def test_solver_mult_fractions():
    assert test_generator(simplify('5 * (4 / y)')) == F(20, 'y')
    assert test_generator(simplify('4 / x * y * 1 * z')) == F(M(4.0, 'y', 'z'), 'x')
    assert test_generator(simplify('4 / x * (y / 1) * z')) == F(M(4, 'y', 'z'), 'x')
    assert test_generator(simplify('4 / x * (y * 1) * z')) == F(M(4, 'y', 'z'), 'x')
    assert test_generator(simplify('3 * x / 4 * y')) == F(M(3, 'x', 'y'), 4)


def test_solver_plus():
    assert test_generator(simplify('5 + 4 + 3')) == 12
    assert test_generator(simplify('5 + x + x + 3')) == P(8, M(2, 'x'))


def test_exp():
    assert test_generator(simplify('3 ^ 4')) == 81
    assert test_generator(simplify('(x ^ 4) ^ 3')) == E('x', 12)
    assert test_generator(simplify('(x / y) ^ 2')) == F(E('x', 2), E('y', 2))
    assert test_generator(simplify('(x * y) ^ 2')) == M(E('x', 2), E('y', 2))


def test_simplify_fractions():
    assert test_generator(simplify('a/b')) == F('a', 'b')
    assert test_generator(simplify('a/b/c/d/e')) == F('a', M('b', 'c', 'd', 'e'))
    assert test_generator(simplify('a/(b/(c/(d/e)))')) == F(M('a','c','e'),M('b','d'))


def test_eval():
    assert evalexpr(M(5, 4, 3)) == 60
    assert evalexpr(P(3, 4, 5)) == 12
    assert evalexpr(M(5, P(4, 5), 6)) == 270

if __name__ == "__main__":
    test_simplify_fractions()
    test_solver_mult_fractions()
    test_solver_plus()
    test_solver_mult_basic()
    test_exp()
    test_solver_mult_combine_symbols()
    pass

