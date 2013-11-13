from testhelpers import *
from base import Operator
from base import Commutative as Com
from base import Noncommutative as NCom
from parse import EquationParser

p = EquationParser()

def test_repr_basic():
    assert repr(p.parse('5 + 4')) == '5 + 4'
    assert repr(p.parse('5*4+3/2')) == '5 * 4 + 3 / 2'
    assert repr(p.parse('5')) == '5'

#def test_repr_nested():
#    # if same operator and commutative, parenthesis are not necessary
#    assert repr(p.parse('5 + (4 + 3)')) == '5 + 4 + 3'
#    assert repr(p.parse('5 * (4 * 3)')) == '5 * 4 * 3'
#
#    # if contained in different operator with a later order of operation, the parenthesis are not necessary
#    assert repr(p.parse('5 + (4 * 3)')) == '5 + 4 * 3'
#    assert repr(p.parse('2 / (4 ^ 5)')) == '2 + 4 ^ 5'
#    assert repr(p.parse('2 * (4 ^ 5)')) == '2 + 4 ^ 5'
#
#    # if contained in noncommutative operation, but it's going to be first anyway, ditch paranthesis.
#    #assert repr(p.parse('(5 / 4) * 3')) == '5 / 4 * 3'

def test_hash():
    assert hash(Com(1, 2)) == hash(Com(2, 1))
    assert hash(Com(1, Com(2, 1))) == hash(Com(1, Com(1, 2)))

    assert hash(NCom(1, 2)) == hash(NCom(1, 2))
    assert hash(NCom(1, 2)) != hash(NCom(2, 1))