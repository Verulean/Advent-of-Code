fmt_dict = { "sep": "\n\n" }

def mirror_indices(i, n):
    for di in range(min(i, n - i)):
        yield i - di - 1, i + di

def score_grid(grid, error_count):
    m, n = len(grid), len(grid[0])
    for i in range(1, m):
        indices = tuple(mirror_indices(i, m))
        errors = 0
        for j in range(n):
            for i1, i2 in indices:
                if grid[i1][j] != grid[i2][j]:
                    errors += 1
                    if errors > error_count:
                        break
        else:
            if errors == error_count:
                return i * 100
    for j in range(1, n):
        indices = tuple(mirror_indices(j, n))
        errors = 0
        for i in range(m):
            for j1, j2 in indices:
                if grid[i][j1] != grid[i][j2]:
                    errors += 1
                    if errors > error_count:
                        break
        else:
            if errors == error_count:
                return j

def solve(data):
    grids = [block.split("\n") for block in data]
    ans1 = sum(score_grid(g, 0) for g in grids)
    ans2 = sum(score_grid(g, 1) for g in grids)
    return ans1, ans2
