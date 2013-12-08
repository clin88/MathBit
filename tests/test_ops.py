from ops import OpCursor, Operator
from tests.testhelpers import *

def test_moveup():
    tree = (
        (1, 2),
        ('x', 'y', (3, 4)),
        'x',
        'y'
    )
    cursor = OpCursor.makecursor(tree)
    cursor = cursor.movedown()
    assert cursor.moveup().node == tree

def test_instantiation():
    assert Operator(1,2,3,4)

def test_basic_arithmetic():
    node = Operator(100)
    assert 5 * node == M(5, node)
    assert node * 5 == M(node, 5)
    assert 5 ** node == E(5, node)
    assert node ** 5 == E(node, 5)
    assert 5 / node == F(5, node)
    assert node / 5 == F(node, 5)
    assert 5 + node == P(5, node)
    assert node + 5 == P(node, 5)
    assert 5 - node == P(5, M(-1, node))
    assert node - 5 == P(node, -5)
    assert -node == M(-1, node)

def test_plus():
    node = P(100, 100)
    assert 5 + node == P(5, 100, 100)
    assert node + 5 == P(100, 100, 5)
    assert node + node == P(100, 100, 100, 100)

def test_mult():
    node = M(2, 3)
    assert 5 * node == M(5, 2, 3)
    assert node * 5 == M(2, 3, 5)
    assert node * node == M(2, 3, 2, 3)
    assert -node == M(-1, 2, 3)

def test_exp():
    try:
        node = E(2, 3, 4)
    except TypeError:
        assert True

    node = E(2, 3)

def test_frac():
    try:
        node = F(2, 3, 4)
    except TypeError:
        assert True

    node = F(2, 3)
