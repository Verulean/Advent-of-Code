from util import ints


fmt_dict = {
    "cast_type": ints,
    "sep": "\n\n",
}

def f2(ax, ay, bx, by, x, y):
    na, ra = divmod(x * by - y * bx, ax * by - ay * bx)
    if ra != 0:
        return 0
    nb, rb = divmod(x - na * ax, bx)
    if rb:
        return 0
    return 3 * na + nb

def solve(data):
    ans1 = ans2 = 0
    for ax, ay, bx, by, x, y in data:
        ans1 += f2(ax, ay, bx, by, x, y)
        ans2 += f2(ax, ay, bx, by, x + 10000000000000, y + 10000000000000)
    return ans1, ans2
