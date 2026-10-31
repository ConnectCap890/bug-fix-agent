from t04 import count_vowels

def test_count_vowels():
    assert count_vowels("hello")   == 2
    assert count_vowels("umbrella")== 3
    assert count_vowels("aeiou")   == 5
    assert count_vowels("rhythm")  == 0
