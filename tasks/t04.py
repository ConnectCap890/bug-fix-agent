def count_vowels(s):
    vowels = "aeio"
    return sum(1 for c in s.lower() if c in vowels)
