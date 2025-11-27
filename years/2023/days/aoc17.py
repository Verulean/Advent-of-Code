from util import Dijkstra, D4


class Crucible(Dijkstra):
    start = ((0, 0), None)

    def __init__(self, grid, min_dist, max_dist):
        super().__init__()
        self.grid = grid
        self.m, self.n = len(grid), len(grid[0])
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.end_pos = (self.m - 1, self.n - 1)

    def is_goal(self, state) -> bool:
        return state[0] == self.end_pos

    def neighbors(self, state):
        (i, j), prev_dir = state
        for di, dj in D4:
            if (di, dj) == prev_dir or (-di, -dj) == prev_dir:
                continue
            ii, jj = i, j
            d_cost = 0
            for dist in range(1, self.max_dist + 1):
                ii, jj = ii + di, jj + dj
                if not (0 <= ii < self.m and 0 <= jj < self.n):
                    break
                d_cost += self.grid[ii][jj]
                if dist >= self.min_dist:
                    adj_state = ((ii, jj), (di, dj))
                    yield d_cost, adj_state


def solve(data):
    grid = [[int(x) for x in row] for row in data]
    c = Crucible(grid, 1, 3)
    p1 = c.run()
    c.min_dist, c.max_dist = 4, 10
    p2 = c.run()
    return p1, p2
