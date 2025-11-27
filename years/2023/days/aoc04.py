from collections import defaultdict
from util import ints


def solve(data):
    n = len(data)
    p1 = 0
    cards = defaultdict(int)
    for i, line in enumerate(data):
        cards[i] += 1
        l, r = map(set, map(ints, line.split(": ")[1].split(" | ")))
        overlaps = len(l & r)
        if overlaps:
            p1 += 2 ** (overlaps - 1)
            for j in range(i + 1, i + overlaps + 1):
                if j >= n:
                    break
                cards[j] += cards[i]

    return p1, sum(cards.values())
