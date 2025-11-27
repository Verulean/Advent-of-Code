from functools import partial
from util import ints, lmap, smap


fmt_dict = { "cast_type": ints }

def pascalify(numbers):
    rows = [numbers]
    curr_row = numbers
    while not all(x == 0 for x in curr_row):
        curr_row = [b - a for a, b in zip(curr_row, curr_row[1:])]
        rows.append(curr_row)
    return rows[:-1]

def extrapolate(pyramid, reverse=False):
    if not reverse:
        return sum(row[-1] for row in pyramid)
    return sum(row[0] for row in pyramid[::2]) - sum(row[0] for row in pyramid[1::2])

def solve(histories):
    pyramids = lmap(pascalify, histories)
    ans1 = smap(extrapolate, pyramids)
    ans2 = smap(partial(extrapolate, reverse=True), pyramids)
    return ans1, ans2
