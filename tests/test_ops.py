from decimal import Decimal as D

from core.ops import Operator
from core import OpCursor
from tests.testhelpers import *


def test_moveup():
    tree = M(
        E(1, 2),
        P('x', 'y', F(3, 4)),
        'x',
        'y'
    )
    cursor = OpCursor.makecursor(tree)
    cursor = cursor.movedown()
    assert cursor.moveup().node == tree


def test_instantiation():
    assert Operator(1, 2, 3, 4)


def test_basic_arithmetic():
    node = Operator(100)
    assert node * 5 == M(node, 5)
    assert 5 * node == M(5, node)
    assert node ** 5 == E(node, 5)
    assert 5 ** node == E(5, node)
    assert node / 5 == F(node, 5)
    assert 5 / node == F(5, node)
    assert node + 5 == P(node, 5)
    assert 5 + node == P(5, node)
    assert node - 5 == P(node, -5)
    assert 5 - node == P(5, -node)
    assert -node == M(-1, node)


def test_identity_ops():
    node = Operator(10)
    assert node * 1 == node
    assert 1 * node == node
    assert node / 1 == node
    assert node + 0 == node
    assert 0 + node == node
    assert node - 0 == node
    assert 0 - node == -node


def test_plus():
    node = P(100, 100)
    assert node + 5 == P(100, 100, 5)
    assert node + node == P(100, 100, 100, 100)
    assert node + 0 == node


def test_mult():
    node = M(2, 3)
    assert node * 5 == M(2, 3, 5)
    assert node * node == M(2, 3, 2, 3)
    assert -node == M(-1, 2, 3)
    assert node * 1 == node


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
    else:
        assert False

    node = F(2, 3)


def test_nmbr():
    assert N(5) == 5
    assert N('3.5') == D('3.5')
    assert N(3.5) == D(3.5)

    n = N(5)
    assert n * 5 == M(5, 5)
    assert n / 5 == F(5, 5)
    assert n ** 5 == E(5, 5)
    assert n + 5 == P(5, 5)
    assert n - 5 == P(5, -5)

    assert -1 * n == -5
    assert n * -1 == -5


def test_symbol():
    x = S('x')
    assert x * 5 == M(x, 5)
    assert x / 5 == F(x, 5)
    assert x ** 5 == E(x, 5)
    assert x + 5 == P(x, 5)
    assert x - 5 == P(x, -5)