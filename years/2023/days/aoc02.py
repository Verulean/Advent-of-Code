from collections import defaultdict


def solve(data):
    ans1 = 0
    ans2 = 0
    for i, line in enumerate(data):
        minimum_cubes = defaultdict(int)
        draws = line.split(":")[1]
        for draw in draws.replace(";", ",").split(","):
            number, color = draw.split()
            number = int(number)
            minimum_cubes[color] = max(minimum_cubes[color], number)
        r, g, b = map(minimum_cubes.get, ("red", "green", "blue"))
        if r <= 12 and g <= 13 and b <= 14:
            ans1 += i + 1
        ans2 += r * g * b
    return ans1, ans2
