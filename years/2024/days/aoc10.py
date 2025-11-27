from util import Neighbors, grid_where, to_array


def find_paths(grid, i, j):
    m, n = grid.shape
    neighbors = Neighbors(m=m, n=n)
    paths = {((i, j),)}
    for h in range(1, 10):
        new_paths = set()
        for path in paths:
            (i, j) = path[-1]
            for ii, jj in neighbors(i, j):
                if grid[ii, jj] == h:
                    new_paths.add(path + ((ii, jj),))
        paths = new_paths
    return paths

def solve(data):
    grid = to_array(data, f=int)
    ans1 = ans2 = 0
    for i, j in grid_where(grid, 0):
        paths = find_paths(grid, i, j)
        ans1 += len(set(path[-1] for path in paths))
        ans2 += len(paths)
    return ans1, ans2
