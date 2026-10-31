from t09 import clamp

def test_clamp():
    assert clamp(5,  1, 10) == 5
    assert clamp(-5, 1, 10) == 1
    assert clamp(15, 1, 10) == 10
