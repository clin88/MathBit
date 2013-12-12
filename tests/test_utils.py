from utils import cat, flatten
from tests.testhelpers import *

def test_cat():
    assert cat([1, 2, 3], [4, 5], [6]) == (1,2,3,4,5,6)
    assert cat([1, 2, 3], [4, 5], 6) == (1,2,3,4,5,6)

def test_flatten():
    node = M(1,F(3,4),3, M(4,5),6)
    assert flatten(node) == M(1, F(3,4), 3, 4, 5, 6)


