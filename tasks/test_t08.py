from t08 import count_occurrences

def test_count_occurrences():
    assert count_occurrences([1, 2, 3, 2, 1], 2) == 2
    assert count_occurrences([1, 1, 1], 1)        == 3
    assert count_occurrences([1, 2, 3], 4)        == 0
