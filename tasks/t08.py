def count_occurrences(lst, item):
    count = 0
    for x in lst:
        if x != item:
            count += 1
    return count
