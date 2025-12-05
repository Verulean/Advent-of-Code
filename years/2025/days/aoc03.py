fmt_dict = { "cast_type": lambda x: tuple(map(int, x)) }

def get_joltage(line: tuple[int], num_digits: int) -> int:
    bank_length = len(line)
    i_unused = 0
    ret = 0
    for digit in range(num_digits):
        end_index = bank_length - num_digits + digit + 1
        largest_digit = -1
        for j in range(i_unused, end_index):
            if line[j] > largest_digit:
                largest_digit = line[j]
                i_unused = j + 1
        ret = 10 * ret + largest_digit
    return ret

def solve(data: list[tuple[int]]) -> tuple[int, int]:
    ans1 = sum(get_joltage(line, 2) for line in data)
    ans2 = sum(get_joltage(line, 12) for line in data)
    return ans1, ans2
