from t02 import sum_to_n

def test_sum_to_n():
    assert sum_to_n(5)  == 15
    assert sum_to_n(1)  == 1
    assert sum_to_n(10) == 55
