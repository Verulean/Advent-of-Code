from util import D8, grid_where


def count_removable_rolls(rolls: set[tuple[int, int]]) -> int:
    rolls_to_remove = set()
    for i, j in rolls:
        neighbors = { (i + di, j + dj) for di, dj in D8 } & rolls
        if len(neighbors) < 4:
            rolls_to_remove.add((i, j))
    rolls.difference_update(rolls_to_remove)
    return len(rolls_to_remove)

def remove_all_rolls(rolls: set[tuple[int, int]]) -> None:
    q = rolls.copy()
    while q:
        i, j = q.pop()
        neighbors = { (i + di, j + dj) for di, dj in D8 } & rolls
        if len(neighbors) < 4:
            rolls.remove((i, j))
            q |= neighbors

def solve(data: list[str]) -> tuple[int, int]:
    rolls = grid_where(data, "@")
    starting_rolls = len(rolls)
    ans1 = count_removable_rolls(rolls)
    remove_all_rolls(rolls)
    return ans1, starting_rolls - len(rolls)
