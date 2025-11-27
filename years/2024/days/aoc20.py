from collections import defaultdict, deque
from util import grid_find, grid_where


def get_all_paths(walls, start, end):
    seen = set()
    paths = set()
    q = deque()
    q.append((start,))
    while q:
        path = q.popleft()
        curr = path[-1]
        if curr == end:
            paths.add(path)
            continue
        if curr in seen:
            continue
        seen.add(curr)
        for direction in (-1, 1, -1j, 1j):
            adj = curr + direction
            if adj in walls:
                continue
            q.append(path + (adj,))
    return paths

def get_cheaters(paths, cheat_time):
    cheaters = defaultdict(set)
    for path in paths:
        rev_path = {p: t for t, p in enumerate(path)}
        for t, p in enumerate(path):
            for di in range(-cheat_time, cheat_time + 1):
                leeway = cheat_time - abs(di)
                for dj in range(0 - leeway, 0 + leeway + 1):
                    dt = abs(di) + abs(dj)
                    p2 = p + di + dj * 1j
                    if rev_path.get(p2, 0) - t >= 100 + dt:
                        cheaters[dt].add((p, p2))
    return cheaters

def solve(data):
    walls = grid_where(data, "#", complex=True)
    start = grid_find(data, "S", complex=True)
    end = grid_find(data, "E", complex=True)
    cheats = get_cheaters(get_all_paths(walls, start, end), 20)
    return len(cheats[2]), sum(map(len, cheats.values()))
