def find_max(lst):
    max_val = lst[0]
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val
