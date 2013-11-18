from operators import *

"""
    Low level helper functions.
"""


def test_walk_expr():
    from expression_helpers import walk_expr

    # test print ALL objects
    expr = Expr(Plus(Mult(N(3), N(4)), N(5)))
    assert list(walk_expr(expr)) == [Plus(Mult(N(3), N(4)), N(5)), Mult(N(3), N(4)), N(3), N(4), N(5)]

    # test print SELECT objects
    #expr = p.parse('3 * x + (5 ^ 2 * (4 + 3))')
    expr = Expr(Plus(Mult(3, 'x'), Mult(Exp(5, D('2.1')), Plus(4, 3))))
    assert list(walk_expr(expr, Mult)) == [Mult(3, 'x'), Mult(Exp(5, D('2.1')), Plus(4, 3))]
    assert list(walk_expr(expr, N)) == [N(3), N(5), N('2.1'), N(4), N(3)]
