class PolynomialInterpolator:
    def __init__(self, dx, target):
        self.dx = dx
        self.x = target
        self.known = {}
        self.curr_differences = [0]
        self.prev_differences = [0]
        self.sat = False

    def add(self, x, y):
        self.known[x] = y
        if x == self.x:
            self.sat = True
            return
        self.curr_differences[0] = y
        for i, (curr, prev) in enumerate(zip(self.curr_differences, self.prev_differences)):
            d = curr - prev
            if not d:
                for j in range(i + 1, len(self.curr_differences)):
                    self.curr_differences[j] = 0
                self.sat = True
                self.x0 = x
                break
            elif i + 1 < len(self.curr_differences):
                self.curr_differences[i + 1] = d
            else:
                self.curr_differences.append(d)
        self.prev_differences = self.curr_differences.copy()

    def __call__(self):
        if self.x in self.known:
            return self.known[self.x]
        derivatives = self.curr_differences.copy()
        for _ in range((self.x - self.x0) // self.dx):
            for i in range(len(derivatives) - 1, 0, -1):
                derivatives[i - 1] += derivatives[i]
        return derivatives[0]

def count_steps(n, garden, start, targets):
    curr_boundary = { start }
    prev_boundary = set()
    counts = [0, 0]
    dx = n
    interpolators = { target: PolynomialInterpolator(dx, target) for target in targets }
    steps = max(targets)
    for t in range(steps + 1):
        parity = t % 2
        counts[parity] += len(curr_boundary)
        for target, interp in interpolators.items():
            if interp.sat:
                continue
            if (target - t) % dx == 0:
                interp.add(t, counts[parity])
        if all(interp.sat for interp in interpolators.values()):
            break
        temp = set()
        for i, j in curr_boundary:
            for di, dj in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                ii, jj = i + di, j + dj
                if (ii % n, jj % n) not in garden or (ii, jj) in prev_boundary:
                    continue
                temp.add((ii, jj))
        prev_boundary, curr_boundary = curr_boundary, temp
    return tuple(interpolators[target]() for target in targets)

def solve(data):
    n = len(data)
    garden = set()
    start = None
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            if c == "#":
                continue
            garden.add((i, j))
            if c == "S":
                start = (i, j)
    return count_steps(n, garden, start, (64, 26501365))
