from t03 import find_max

def test_find_max():
    assert find_max([3, 1, 4, 1, 5, 9]) == 9
    assert find_max([1])                 == 1
    assert find_max([])                  is None
