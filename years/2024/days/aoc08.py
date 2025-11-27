from collections import defaultdict
from math import gcd


def in_bounds(i, j, m, n):
    return 0 <= i < m and 0 <= j < n

def find_antinodes(antennae, m, n):
    ret = set()
    for i1, j1 in antennae:
        for i2, j2 in antennae:
            if i1 == i2 and j1 == j2:
                continue
            di, dj = i2 - i1, j2 - j1
            ret.update(((i1 - di, j1 - dj), (i2 + di, j2 + dj)))
    return { (i, j) for i, j in ret if in_bounds(i, j, m, n) }

def find_antinodes_2(antennae, m, n):
    ret = antennae.copy()
    for i1, j1 in antennae:
        for i2, j2 in antennae:
            if i1 == i2 and j1 == j2:
                continue
            di, dj = i2 - i1, j2 - j1
            assert(gcd(di, dj) == 1) # lol
            ii, jj = i1 - di, j1 - dj
            while in_bounds(ii, jj, m, n):
                ret.add((ii, jj))
                ii, jj = ii - di, jj - dj
            ii, jj = i2 + di, j2 + dj
            while in_bounds(ii, jj, m, n):
                ret.add((ii, jj))
                ii, jj = ii + di, jj + dj
    return ret

def solve(data):
    antinodes1 = set()
    antinodes2 = set()
    antenna_sets = defaultdict(set)
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c != ".":
                antenna_sets[c].add((i, j))
    m, n = len(data), len(data[0])
    for antennae in antenna_sets.values():
        antinodes1 |= find_antinodes(antennae, m, n)
        antinodes2 |= find_antinodes_2(antennae, m, n)
    return len(antinodes1), len(antinodes2)
