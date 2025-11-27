from util import ints


fmt_dict = {
    "sep": "\n\n",
}

def is_sorted(rules, line):
    line_dict = { n: i for i, n in enumerate(line) }
    for a, b in rules:
        if a not in line_dict or b not in line_dict:
            continue
        if line_dict[a] > line_dict[b]:
            return False
    return True

def rectify(rules, line):
    nums = set(line)
    rules = [r for r in rules if r[0] in nums and r[1] in nums]
    line_dict = { n: i for i, n in enumerate(line) }
    while True:
        for a, b in rules:
            if line_dict[a] > line_dict[b]:
                line_dict[a], line_dict[b] = line_dict[b], line_dict[a]
                break
        else:
            break
    ret_index = len(line) // 2
    for n, i in line_dict.items():
        if i == ret_index:
            return n

def solve(data):
    rules, lines = data
    rules = [ints(r) for r in rules.split()]
    lines = [ints(l) for l in lines.split()]
    ans1 = ans2 = 0
    for line in lines:
        if is_sorted(rules, line):
            ans1 += line[len(line) // 2]
        else:
            ans2 += rectify(rules, line)
    return ans1, ans2
