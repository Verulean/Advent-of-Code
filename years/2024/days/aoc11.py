from collections import Counter


fmt_dict = { "sep": " " }

def blink(stones):
    new_stones = Counter()
    for s, n in stones.items():
        if s == "0":
            new_stones["1"] += n
        elif len(s) % 2 == 0:
            new_stones[s[:len(s) // 2]] += n
            new_stones[s[len(s) // 2:]] += n
        else:
            new_stones[str(2024 * int(s))] += n
    return new_stones

def solve(data):
    stones = Counter(data)
    for _ in range(25):
        stones = blink(stones)
    ans1 = sum(stones.values())
    for _ in range(50):
        stones = blink(stones)
    return ans1, sum(stones.values())
