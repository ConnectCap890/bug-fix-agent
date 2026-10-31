"""
we run this first to create the folder structure for buggy problems and their tests:
  - tasks -->  with 10 buggy Python files + 10 test files
  - runs -->   where agent logs will go
"""

import os

os.makedirs("tasks", exist_ok=True)
os.makedirs("runs", exist_ok=True)

files = {

# t01: wrong operator (== 1 instead of == 0)
"tasks/t01.py": """\
def is_even(n):
    return n % 2 == 1
""",
"tasks/test_t01.py": """\
from t01 import is_even

def test_is_even():
    assert is_even(2)  == True
    assert is_even(3)  == False
    assert is_even(0)  == True
    assert is_even(-4) == True
""",

# t02: off-by-one (range(1, n) misses the last number)
"tasks/t02.py": """\
def sum_to_n(n):
    total = 0
    for i in range(1, n):
        total += i
    return total
""",
"tasks/test_t02.py": """\
from t02 import sum_to_n

def test_sum_to_n():
    assert sum_to_n(5)  == 15
    assert sum_to_n(1)  == 1
    assert sum_to_n(10) == 55
""",

#t03: missing edge case (empty list crashes)
"tasks/t03.py": """\
def find_max(lst):
    max_val = lst[0]
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val
""",
"tasks/test_t03.py": """\
from t03 import find_max

def test_find_max():
    assert find_max([3, 1, 4, 1, 5, 9]) == 9
    assert find_max([1])                 == 1
    assert find_max([])                  is None
""",

#t04: missing character ('u' left out of vowels)
"tasks/t04.py": """\
def count_vowels(s):
    vowels = "aeio"
    return sum(1 for c in s.lower() if c in vowels)
""",
"tasks/test_t04.py": """\
from t04 import count_vowels

def test_count_vowels():
    assert count_vowels("hello")   == 2
    assert count_vowels("umbrella")== 3
    assert count_vowels("aeiou")   == 5
    assert count_vowels("rhythm")  == 0
""",

# t05: wrong operator (- 32 instead of + 32)
"tasks/t05.py": """\
def celsius_to_fahrenheit(c):
    return c * 9 / 5 - 32
""",
"tasks/test_t05.py": """\
from t05 import celsius_to_fahrenheit

def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0)    == 32
    assert celsius_to_fahrenheit(100)  == 212
    assert celsius_to_fahrenheit(-40)  == -40
""",

#t06: wrong slice (s[1:-1] instead of s[::-1])
"tasks/t06.py": """\
def is_palindrome(s):
    return s == s[1:-1]
""",
"tasks/test_t06.py": """\
from t06 import is_palindrome

def test_is_palindrome():
    assert is_palindrome("racecar") == True
    assert is_palindrome("hello")   == False
    assert is_palindrome("a")       == True
    assert is_palindrome("madam")   == True
""",

#t07: wrong comparison operator (!= instead of ==)
"tasks/t07.py": """\
def linear_search(lst, target):
    for i, val in enumerate(lst):
        if val != target:
            return i
    return -1
""",
"tasks/test_t07.py": """\
from t07 import linear_search

def test_linear_search():
    assert linear_search([1, 2, 3, 4], 3) == 2
    assert linear_search([1, 2, 3], 1)    == 0
    assert linear_search([1, 2, 3], 5)    == -1
""",

#t08: wrong operator (!= instead of ==)
"tasks/t08.py": """\
def count_occurrences(lst, item):
    count = 0
    for x in lst:
        if x != item:
            count += 1
    return count
""",
"tasks/test_t08.py": """\
from t08 import count_occurrences

def test_count_occurrences():
    assert count_occurrences([1, 2, 3, 2, 1], 2) == 2
    assert count_occurrences([1, 1, 1], 1)        == 3
    assert count_occurrences([1, 2, 3], 4)        == 0
""",

#t09: wrong return value (returns mx instead of mn)
"tasks/t09.py": """\
def clamp(value, mn, mx):
    if value < mn:
        return mx
    if value > mx:
        return mx
    return value
""",
"tasks/test_t09.py": """\
from t09 import clamp

def test_clamp():
    assert clamp(5,  1, 10) == 5
    assert clamp(-5, 1, 10) == 1
    assert clamp(15, 1, 10) == 10
""",

#t10: wrong starting value (0 instead of 1)
"tasks/t10.py": """\
def multiply_list(lst):
    result = 0
    for x in lst:
        result *= x
    return result
""",
"tasks/test_t10.py": """\
from t10 import multiply_list

def test_multiply_list():
    assert multiply_list([1, 2, 3, 4]) == 24
    assert multiply_list([5])          == 5
    assert multiply_list([2, 3])       == 6
""",

}

for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)
    print(f"created {path}")

print("\nDone. Folder structure ready.")
print("Next: install pytest with  pip install pytest")
print("Then confirm all tests fail:  cd tasks && pytest")