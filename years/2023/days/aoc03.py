from functools import reduce
from operator import mul
from util import Neighbors


def solve(data):
    m, n = len(data), len(data[0])
    neighbors = Neighbors(1, m, n)
    numbers = {}

    def get_numbers(i, j):
        candidates = set(neighbors(i, j))
        new_numbers = {}
        while candidates:
            ii, jj = candidates.pop()
            row = data[ii]
            if not row[jj].isnumeric():
                continue
            j_min = j_max = jj
            while j_min > 0 and row[j_min - 1].isnumeric():
                j_min -= 1
                candidates.discard((ii, j_min))
            while j_max < n - 1 and row[j_max + 1].isnumeric():
                j_max += 1
                candidates.discard((ii, j_min))
            number = int(row[j_min : j_max + 1])
            new_numbers[(ii, j_min)] = number
        return new_numbers

    gear_ratio_sum = 0

    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c.isnumeric() or c == ".":
                continue
            new_numbers = get_numbers(i, j)
            numbers |= new_numbers
            if len(new_numbers) == 2 and c == "*":
                gear_ratio_sum += reduce(mul, new_numbers.values(), 1)
    
    return sum(numbers.values()), gear_ratio_sum
