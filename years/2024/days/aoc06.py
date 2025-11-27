from itertools import pairwise


def simulate_guard(next_block, i, j, di, dj, m, n, blocker=None):
    path = {}
    while True:
        if (i, j, di, dj) in path:
            return None
        bi, bj = next_block[(i, j, di, dj)]
        if di:
            if blocker:
                bii, bjj = blocker
                if bjj == bj and bii in range(i, bi, di):
                    bi = bii
                path[(i, j, di, dj)] = None
                i = bi - di
            else:
                for i in range(i, bi, di):
                    path[(i, j, di, dj)] = None
        else:
            if blocker:
                bii, bjj = blocker
                if bii == bi and bjj in range(j, bj, dj):
                    bj = bjj
                path[(i, j, di, dj)] = None
                j = bj - dj
            else:
                for j in range(j, bj, dj):
                    path[(i, j, di, dj)] = None
        if not (0 <= bi < m and 0 <= bj < n):
            return path
        di, dj = dj, -di

def parse(data):
    m, n = len(data), len(data[0])
    next_block = {}
    gi, gj = 0, 0
    for i, row in enumerate(data):
        l = i, -1
        for j, c in enumerate(row):
            match c:
                case "^":
                    gi, gj = i, j
                    next_block[(gi, gj, 0, -1)] = l
                case "#":
                    l = i, j
                case _:
                    next_block[(i, j, 0, -1)] = l
        r = i, n
        for j in range(n - 1, -1, -1):
            match row[j]:
                case "#":
                    r = i, j
                case _:
                    next_block[(i, j, 0, 1)] = r
    for j in range(n):
        u = -1, j
        for i in range(m):
            match data[i][j]:
                case "#":
                    u = i, j
                case _:
                    next_block[(i, j, -1, 0)] = u
        d = m, j
        for i in range(m - 1, -1, -1):
            match data[i][j]:
                case "#":
                    d = i, j
                case _:
                    next_block[(i, j, 1, 0)] = d
    return next_block, gi, gj, m, n

def solve(data):
    next_block, gi, gj, m, n = parse(data)
    seen = {(gi, gj)}
    ans2 = 0
    for (i, j, di, dj), (ii, jj, _, _) in pairwise(simulate_guard(next_block, gi, gj, -1, 0, m, n)):
        if (ii, jj) in seen:
            continue
        seen.add((ii, jj))
        if simulate_guard(next_block, i, j, di, dj, m, n, (ii, jj)) is None:
            ans2 += 1
    return len(seen), ans2
