from collections import Counter
from util import lmap

fmt_dict = { 'sep': None }

def solve(data):
    nums = lmap(int, data.split())
    lefts, rights = nums[::2], nums[1::2]
    lefts.sort()
    rights.sort()
    left_count = Counter(lefts)
    right_count = Counter(rights)
    ans1 = sum(abs(ll - rr) for ll, rr in zip(lefts, rights))
    ans2 = sum(x * n * right_count[x] for x, n in left_count.items())
    return ans1, ans2
