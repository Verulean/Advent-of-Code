import numpy as np
from itertools import combinations
from util import ints, lmap


def p1(hailstones, lower, upper):
    ret = 0
    for (x1, y1, _, vx1, vy1, _), (x2, y2, _, vx2, vy2, _) in combinations(hailstones, 2):
        m1, m2 = vy1 / vx1, vy2 / vx2
        if m1 == m2:
            continue
        x = (y2 - y1 + m1 * x1 - m2 * x2) / (m1 - m2)
        y = y1 + m1 * (x - x1)
        if not (lower <= x <= upper and lower <= y <= upper):
            continue
        if (x - x1) / vx1 >= 0 and (x - x2) / vx2 >= 0:
            ret += 1
    return ret

def p2(hailstones):
    p1, p2, p3 = (hailstone[:3] for hailstone in hailstones)
    v1, v2, v3 = (hailstone[3:] for hailstone in hailstones)
    A = np.array([
        [0, v2[2] - v1[2], v1[1] - v2[1], 0, p1[2] - p2[2], p2[1] - p1[1]],
        [v1[2] - v2[2], 0, v2[0] - v1[0], p2[2] - p1[2], 0, p1[0] - p2[0]],
        [v2[1] - v1[1], v1[0] - v2[0], 0, p1[1] - p2[1], p2[0] - p1[0], 0],
        [0, v3[2] - v1[2], v1[1] - v3[1], 0, p1[2] - p3[2], p3[1] - p1[1]],
        [v1[2] - v3[2], 0, v3[0] - v1[0], p3[2] - p1[2], 0, p1[0] - p3[0]],
        [v3[1] - v1[1], v1[0] - v3[0], 0, p1[1] - p3[1], p3[0] - p1[0], 0],
    ])
    b = np.array([
        p2[1] * v2[2] - p2[2] * v2[1] - p1[1] * v1[2] + p1[2] * v1[1],
        p2[2] * v2[0] - p2[0] * v2[2] - p1[2] * v1[0] + p1[0] * v1[2],
        p2[0] * v2[1] - p2[1] * v2[0] - p1[0] * v1[1] + p1[1] * v1[0],
        p3[1] * v3[2] - p3[2] * v3[1] - p1[1] * v1[2] + p1[2] * v1[1],
        p3[2] * v3[0] - p3[0] * v3[2] - p1[2] * v1[0] + p1[0] * v1[2],
        p3[0] * v3[1] - p3[1] * v3[0] - p1[0] * v1[1] + p1[1] * v1[0],
    ])
    return int(np.linalg.solve(A, b)[:3].sum())

def solve(data):
    hailstones = lmap(ints, data)
    l, h = (7, 27) if len(data) < 10 else (2e14, 4e14)
    return p1(hailstones, l, h), p2(hailstones[:3])
