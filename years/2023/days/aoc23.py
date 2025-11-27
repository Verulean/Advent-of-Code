from collections import defaultdict, deque
from util import Neighbors


directed = { "^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1) }

def make_digraph(grid):
    m, n = len(grid), len(grid[0])
    neighbors = Neighbors(0, m, n)
    start = (0, 1)
    end = (m - 1, n - 2)
    digraph = defaultdict(dict)
    seen = set()
    q = deque()
    q.append((0, start, start))
    while q:
        n, curr, junction = q.pop()
        i, j = curr
        paths = 0
        to_add = []
        for ii, jj in neighbors(i, j):
            c = grid[ii][jj]
            if c == "#":
                continue
            paths += 1
            if (ii, jj) in seen:
                continue
            di, dj = ii - i, jj - j
            if (di, dj) != directed.get(c, (di, dj)):
                continue
            to_add.append((ii, jj))
        if paths > 2 or curr == end:
            digraph[junction][curr] = n
            for p in to_add:
                q.append((1, p, curr))
        else:
            seen.add(curr)
            for p in to_add:
                q.append((n + 1, p, junction))
    # collapse start and end
    first_junction, start_cost = next(iter(digraph[start].items()))
    last_junction, end_cost = next((node, adjs[end]) for node, adjs in digraph.items() if end in adjs)
    del digraph[start]
    for node, adjs in digraph.items():
        if node == first_junction:
            for adj in adjs:
                adjs[adj] += start_cost
        if last_junction in adjs:
            adjs[last_junction] += end_cost
    return digraph, first_junction, last_junction

def make_graph(digraph):
    graph = defaultdict(dict)
    for src, adjs in digraph.items():
        for adj, cost in adjs.items():
            graph[src][adj] = cost
            graph[adj][src] = cost
    return graph

def find_longest(graph, start, end):
    ret = 0
    q = deque()
    q.append((0, start, { start }))
    while q:
        cost, curr, seen = q.pop()
        if curr == end:
            ret = max(ret, cost)
            continue
        for adj, adj_cost in graph[curr].items():
            if adj in seen:
                continue
            adj_seen = seen | { adj }
            q.append((cost + adj_cost, adj, adj_seen))
    return ret

def solve(data):
    digraph, start, end = make_digraph(data)
    ans1 = find_longest(digraph, start, end)
    ans2 = find_longest(make_graph(digraph), start, end)
    return ans1, ans2
