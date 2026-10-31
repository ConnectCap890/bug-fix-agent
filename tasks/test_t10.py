from t10 import multiply_list

def test_multiply_list():
    assert multiply_list([1, 2, 3, 4]) == 24
    assert multiply_list([5])          == 5
    assert multiply_list([2, 3])       == 6
