from collections import deque
from util import D4, tadd


def rot90(d):
    return (d[1], -d[0])

def score_region(points):
    area = len(points)
    perimeter1 = 0
    perimeter2 = 0
    for p in points:
        for d in D4:
            neighbor = tadd(p, d)
            if neighbor not in points:
                perimeter1 += 1
                next_door_neighbor = tadd(p, rot90(d))
                if next_door_neighbor not in points or tadd(next_door_neighbor, d) in points:
                    perimeter2 += 1
    return area * perimeter1, area * perimeter2

def floodfill_region(grid, i, j, m, n):
    c = grid[i][j]
    points = {(i, j)}
    q = deque()
    q.append((i, j))
    while q:
        i, j = q.pop()
        for di, dj in D4:
            ii, jj = i + di, j + dj
            if (ii, jj) in points \
                or not (0 <= ii < m and 0 <= jj < n) \
                or grid[ii][jj] != c:
                continue
            points.add((ii, jj))
            q.append((ii, jj))
    return points

def solve(data):
    seen = set()
    ans1 = ans2 = 0
    m, n = len(data), len(data[0])
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if (i, j) in seen:
                continue
            points = floodfill_region(data, i, j, m, n)
            seen |= points
            score1, score2 = score_region(points)
            ans1 += score1
            ans2 += score2
    return ans1, ans2
