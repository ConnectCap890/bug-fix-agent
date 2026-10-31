from t06 import is_palindrome

def test_is_palindrome():
    assert is_palindrome("racecar") == True
    assert is_palindrome("hello")   == False
    assert is_palindrome("a")       == True
    assert is_palindrome("madam")   == True
