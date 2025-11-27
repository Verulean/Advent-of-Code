from math import log10
from util import ints


fmt_dict = { "cast_type": ints }

def digits(n):
    return int(log10(n)) + 1

def endswith(a, b):
    return (a - b) % 10 ** digits(b) == 0

def is_tractable(test_value, numbers, i, check_concat=True):
    n = numbers[i]
    if i == 0:
        return n == test_value
    q, r = divmod(test_value, n)
    if r == 0 and is_tractable(q, numbers, i - 1, check_concat):
        return True
    if check_concat and endswith(test_value, n) and is_tractable(test_value // (10 ** digits(n)), numbers, i - 1, check_concat):
        return True
    return test_value > n and is_tractable(test_value - n, numbers, i - 1, check_concat)

def solve(data):
    ans1 = ans2 = 0
    for line in data:
        test_value, *numbers = line
        if is_tractable(test_value, numbers, len(numbers) - 1, False):
            ans1 += test_value
            ans2 += test_value
        elif is_tractable(test_value, numbers, len(numbers) - 1):
            ans2 += test_value
    return ans1, ans2
