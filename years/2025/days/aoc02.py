from functools import cache


fmt_dict = { "sep": "," }

@cache
def get_multiplier(count: int, length: int) -> int:
    return sum(10 ** (length * power) for power in range(count))

def sum_invalid_ids(a: int, b: int, num_digits: int, piece_length: int) -> int:
    piece_count, r = divmod(num_digits, piece_length)
    if r:
        return 0

    multiplier = get_multiplier(piece_count, piece_length)

    if num_digits > len(str(a)):
        min_factor = 10 ** (piece_length - 1)
    else:
        min_factor = a // multiplier
        if min_factor * multiplier < a:
            min_factor += 1

    if num_digits < len(str(b)):
        max_factor = 10 ** piece_length - 1
    else:
        max_factor = b // multiplier
        if max_factor * multiplier > b:
            max_factor -= 1

    return multiplier * (max_factor * (max_factor + 1) - min_factor * (min_factor - 1)) // 2

def sum_pairs(a: int, b: int, num_digits: int) -> int:
    piece_length, r = divmod(num_digits, 2)
    return 0 if r else sum_invalid_ids(a, b, num_digits, piece_length)

def sum_repeats(a: int, b: int, num_digits: int) -> int:
    factors = [n for n in range(1, num_digits // 2 + 1) if num_digits % n == 0]
    counts = { l: sum_invalid_ids(a, b, num_digits, l) for l in factors }
    ret = sum(counts.values())
    for n in factors:
        for nn in factors:
            if nn >= n:
                break
            if n % nn == 0:
                ret -= counts[nn]
    return ret

def solve(data: list[str]) -> tuple[int, int]:
    ans1 = ans2 = 0
    for line in data:
        a, b = map(int, line.split("-"))
        for l in range(len(str(a)), len(str(b)) + 1):
            ans1 += sum_pairs(a, b, l)
            ans2 += sum_repeats(a, b, l)
    return ans1, ans2
