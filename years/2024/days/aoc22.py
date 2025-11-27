from collections import Counter
from itertools import pairwise
from util import windowed


fmt_dict = { "cast_type": int }

def next(n):
    n ^= 64 * n
    n %= 16777216
    n ^= n // 32
    n %= 16777216
    n ^= 2048 * n
    n %= 16777216
    return n

def get_price(n):
    if n >= 0:
        return n % 10
    return -(-n % 10)

def solve(data):
    ans1 = 0
    sells = Counter()
    for n in data:
        seen_changes = set()
        prices = [get_price(n)]
        for _ in range(2000):
            n = next(n)
            prices.append(get_price(n))
        ans1 += n
        deltas = [b - a for a, b in pairwise(prices)]
        for sell_price, trigger_sequence in zip(prices[4:], windowed(deltas, 4)):
            if trigger_sequence in seen_changes:
                continue
            seen_changes.add(trigger_sequence)
            sells[trigger_sequence] += sell_price
    return ans1, max(sells.values())
