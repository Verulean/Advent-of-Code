from util import lmap


memo = {}
def get_arrangements(line, group_lengths, line_index, group_index, curr_length):
    k = (line_index, group_index, curr_length)
    if k in memo:
        return memo[k]
    if line_index == len(line):
        if group_index == len(group_lengths) and curr_length == 0:
            return 1
        if group_index == len(group_lengths) - 1 and group_lengths[group_index] == curr_length:
            return 1
        return 0
    ret = 0
    for c in (".", "#"):
        if line[line_index] in { c, "?" }:
            if c == ".":
                if curr_length == 0:
                    ret += get_arrangements(line, group_lengths, line_index + 1, group_index, 0)
                if group_index < len(group_lengths) and group_lengths[group_index] == curr_length:
                    ret += get_arrangements(line, group_lengths, line_index + 1, group_index + 1, 0)
            else:
                ret += get_arrangements(line, group_lengths, line_index + 1, group_index, curr_length + 1)
    memo[k] = ret
    return ret

def solve(data):
    ans1 = ans2 = 0
    for line in data:
        line, group_lengths = line.split()
        group_lengths = lmap(int, group_lengths.split(","))
        memo.clear()
        ans1 += get_arrangements(line, group_lengths, 0, 0, 0)
        memo.clear()
        ans2 += get_arrangements(line + 4 * ("?" + line), group_lengths * 5, 0, 0, 0)
    return ans1, ans2
