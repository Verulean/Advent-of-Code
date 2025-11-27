from itertools import pairwise
from util import ints


fmt_dict = { "cast_type": ints }

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def get_expected_sign(diffs):
    p, n = 0, 0
    for d in diffs:
        if d > 0:
            p += 1
        elif d < 0:
            p -= 1
    return 1 if p > n else -1

def is_safe(line):
    diffs = [b - a for a, b in pairwise(line)]
    expected_sign = get_expected_sign(diffs)
    candidates = []
    for i, d in enumerate(diffs):
        if abs(d) > 3 or sign(d) != expected_sign:
            candidates.append(i)
    match len(candidates):
        case 0:
            return 2
        case 2:
            i, j = candidates
            if j != i + 1:
                return 0
            d = diffs[i] + diffs[j]
            if 1 <= abs(d) <= 3 and sign(d) == expected_sign:
                return 1
        case 1:
            i = candidates[0]
            if i == 0 or i == len(diffs) - 1:
                return 1
            di = diffs[i]
            if di == 0:
                return 1
            d = di + diffs[i - 1]
            if 1 <= abs(d) <= 3 and sign(d) == expected_sign:
                return 1
            d = di + diffs[i + 1]
            if 1 <= abs(d) <= 3 and sign(d) == expected_sign:
                return 1
            return 0
        case _:
            return 0
    return 0

def solve(data):
    ans1, ans2 = 0, 0
    for line in data:
        match is_safe(line):
            case 1:
                ans2 += 1
            case 2:
                ans1 += 1
                ans2 += 1
    return ans1, ans2
