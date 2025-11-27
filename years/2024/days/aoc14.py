from math import prod
from statistics import variance
from util import ints


fmt_dict = { "cast_type": ints }

m, n = 101, 103

def step(points, velocities):
    return [((x + vx) % m, (y + vy) % n) for (x, y), (vx, vy) in zip(points, velocities)]

def get_safety_factor(points):
    x_mid, y_mid = m // 2, n // 2
    counts = [0] * 4
    for x, y in points:
        if x == x_mid or y == y_mid:
            continue
        counts[2 * (x > x_mid) + (y > y_mid)] += 1
    return prod(counts)

def solve(data):
    points = [line[:2] for line in data]
    velocities = [line[2:] for line in data]
    best_x_variance = (10_000, 0)
    best_y_variance = (10_000, 0)
    for t in range(1, 104):
        points = step(points, velocities)
        if t == 100:
            ans1 = get_safety_factor(points)
        x_variance = variance(p[0] for p in points)
        if x_variance < best_x_variance[0]:
            best_x_variance = x_variance, t
        y_variance = variance(p[1] for p in points)
        if y_variance < best_y_variance[0]:
            best_y_variance = y_variance, t
    ans2 = 51 * (best_x_variance[1] * n + best_y_variance[1] * m) % (m * n)
    return ans1, ans2
