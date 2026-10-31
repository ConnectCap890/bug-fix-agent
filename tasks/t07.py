def linear_search(lst, target):
    for i, val in enumerate(lst):
        if val != target:
            return i
    return -1
