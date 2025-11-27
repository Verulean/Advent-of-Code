def solve(data):
    galaxies = []
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "#":
                galaxies.append((i, j))
    xs = { i for i, row in enumerate(data) if "#" not in row }
    ys = { j for j, col in enumerate(zip(*data)) if "#" not in col }
    p1 = p2 = 0
    for i, (x1, y1) in enumerate(galaxies):
        for (x2, y2) in galaxies[i + 1:]:
            a1, a2 = (x1, x2) if x1 < x2 else (x2, x1)
            b1, b2 = (y1, y2) if y1 < y2 else (y2, y1)
            manhattan = a2 - a1 + b2 - b1
            crosses = 0
            for x in xs:
                if a1 < x < a2:
                    crosses += 1
            for y in ys:
                if b1 < y < b2:
                    crosses += 1
            p1 += manhattan + crosses
            p2 += manhattan + 999999 * crosses
    return p1, p2
