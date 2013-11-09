from abbreviated_operations import *
from parse import EquationParser
from solver import simplify_expr
from copy import deepcopy

p = EquationParser()
def test_solver():
    assert simplify_expr(p.parse('5 * (4 * 3)')) == Ex(N(60))
    assert simplify_expr(p.parse('5 * (4 * x)')) == Ex(M(20, 'x'))
    assert simplify_expr(p.parse('(x * 5) * 4 * 3')) == Ex(M(60, 'x'))
    assert simplify_expr(p.parse('(x * y * 5) * 4 * 3')) == Ex(M(60, 'x', 'y'))
