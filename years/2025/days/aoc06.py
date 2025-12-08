from operator import add, mul
from functools import reduce
import numpy as np


fmt_dict = { "strip": False }

def solve(data: list[str]) -> tuple[int, int]:
    grid = np.array([[*line, " "] for line in data])
    ans1 = ans2 = 0
    m, n = grid.shape
    digits = [0] * (m - 1)
    acc = 0
    op = None
    for j in range(n):
        column = grid[:, j]
        if np.all(column == " "):
            ans1 += reduce(op, digits)
            ans2 += acc
            digits = [0] * (m - 1)
            continue
        num = 0
        for i, c in enumerate(column):
            match c:
                case "+":
                    op = add
                    acc = 0
                case "*":
                    op = mul
                    acc = 1
                case " ":
                    pass
                case _:
                    d = int(c)
                    digits[i] = digits[i] * 10 + d
                    num = num * 10 + d
        acc = op(acc, num)
    return ans1, ans2
