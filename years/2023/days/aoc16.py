from collections import deque


class MirrorGrid:
    def __init__(self, grid):
        self.__obstructions = { (i, j): c for i, row in enumerate(grid) for j, c in enumerate(row) if c != "." }
        self.__m = len(grid)
        self.__n = len(grid[0])

    def __raytrace(self, start):
        seen = set()
        exits = set()
        q = deque([start])
        while q:
            i, j, di, dj = q.pop()
            i, j = i + di, j + dj
            if (i, j, di, dj) in seen:
                continue
            if not (0 <= i < self.__m and 0 <= j < self.__n):
                exits.add((i, j, -di, -dj))
                continue
            seen.add((i, j, di, dj))
            match self.__obstructions.get((i, j), None):
                case "/":
                    di, dj = -dj, -di
                case "\\":
                    di, dj = dj, di
                case "|" if dj:
                    di, dj = 1, 0
                    q.append((i, j, -1, 0))
                case "-" if di:
                    di, dj = 0, 1
                    q.append((i, j, 0, -1))
            q.append((i, j, di, dj))
        energized = {x[:2] for x in seen}
        return len(energized), exits

    def __get_beam_starts(self):
        for i in range(self.__m):
            yield i, -1, 0, 1
            yield i, self.__n, 0, -1
        for j in range(self.__n):
            yield -1, j, 1, 0
            yield self.__m, j, -1, 0

    def find_coverage(self, start):
        return self.__raytrace(start)[0]

    def find_max_coverage(self):
        ret = 0
        starts = set(self.__get_beam_starts())
        while starts:
            coverage, exits = self.__raytrace(starts.pop())
            ret = max(ret, coverage)
            starts -= exits
        return ret

def solve(data):
    mirrors = MirrorGrid(data)
    p1 = mirrors.find_coverage((0, -1, 0, 1))
    p2 = mirrors.find_max_coverage()
    return p1, p2
