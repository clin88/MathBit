from utils import cat

def test_join():
    assert cat([1, 2, 3], [4, 5], [6], [4, 5]) == (1,2,3,4,5,6)
    assert cat([1, 2, 3], [4, 5], 6, [4, 5]) == (1,2,3,4,5,6)
