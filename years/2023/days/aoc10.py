from collections import deque
from util import Neighbors, lmap


class PipeMaze:
    __PIPE_MAP = {
        ".": 0,
        "|": 1,
        "-": 2,
        "L": 3,
        "J": 4,
        "7": 5,
        "F": 6,
        "S": 7
    }

    __OPENINGS = (
        set(),
        {(-1, 0), (1, 0)},
        {(0, -1), (0, 1)},
        {(-1, 0), (0, 1)},
        {(-1, 0), (0, -1)},
        {(1, 0), (0, -1)},
        {(1, 0), (0, 1)}
    )

    def __init__(self, grid):
        self.__grid = [lmap(self.__PIPE_MAP.get, row) for row in grid]
        self.__start_type = None
        self.__neighbors = Neighbors(0, len(self.__grid), len(self.__grid[0]))
        self.__loop_grid = self.__map_loop()

    def __find_start(self):
        for i, row in enumerate(self.__grid):
            for j, tile in enumerate(row):
                if tile == 7:
                    return i, j

    def __get_openings(self, pipe):
        return self.__OPENINGS[self.__start_type if pipe == 7 else pipe]

    def __is_connected(self, source, dest, direction):
        di, dj = direction
        return direction in self.__get_openings(source) and (-di, -dj) in self.__get_openings(dest)

    def __map_loop(self):
        # Find and deduce pipe type of S
        start = self.__find_start()
        si, sj = start
        start_openings = set()
        for ii, jj in self.__neighbors(si, sj):
            di, dj = ii - si, jj - sj
            if (-di, -dj) in self.__get_openings(self.__grid[ii][jj]):
                start_openings.add((di, dj))
        for i, openings in enumerate(self.__OPENINGS):
            if start_openings <= openings:
                self.__start_type = i
                break
        if self.__start_type is None:
            raise RuntimeError("Could not determine the starting pipe type")
        # Flood fill loop
        loop_grid = [[0 for _ in self.__grid[0]] for _ in self.__grid]
        seen = set()
        q = deque([start])
        while q:
            i, j = q.popleft()
            if (i, j) in seen:
                continue
            seen.add((i, j))
            source = self.__grid[i][j]
            for ii, jj in self.__neighbors(i, j):
                di, dj = ii - i, jj - j
                dest = self.__grid[ii][jj]
                if not self.__is_connected(source, dest, (di, dj)):
                    continue
                q.append((ii, jj))
                loop_grid[ii][jj] = dest
        loop_grid[si][sj] = self.__start_type
        return loop_grid

    @property
    def loop_length(self):
        ret = 0
        for row in self.__loop_grid:
            for c in row:
                if c:
                    ret += 1
        return ret

    @property
    def enclosed_tiles(self):
        vertical_pipes = { 1, 3, 4 }
        count = 0
        for row in self.__loop_grid:
            inside = False
            for tile in row:
                if tile in vertical_pipes:
                    inside = not inside
                elif not tile and inside:
                    count += 1
        return count


def solve(data):
    maze = PipeMaze(data)
    return maze.loop_length // 2, maze.enclosed_tiles
