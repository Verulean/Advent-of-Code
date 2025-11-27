from itertools import starmap
from math import ceil, floor, prod
from util import ints, quadratic


def win_count(time, distance):
    a, b = quadratic(1, -time, distance)
    return ceil(b) - floor(a) - 1

def solve(data):
    ans1 = prod(starmap(win_count, zip(*map(ints, data))))
    ans2 = win_count(*[ints(line.replace(" ", ""))[0] for line in data])
    return ans1, ans2
