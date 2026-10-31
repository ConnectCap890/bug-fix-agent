from t07 import linear_search

def test_linear_search():
    assert linear_search([1, 2, 3, 4], 3) == 2
    assert linear_search([1, 2, 3], 1)    == 0
    assert linear_search([1, 2, 3], 5)    == -1
