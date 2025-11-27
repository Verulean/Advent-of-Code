from collections import deque
from copy import deepcopy
from util import Range, ints, lmap, prod


fmt_dict = { "sep": "\n\n" }

def parse_workflow(line):
    src, rest = line.split("{")
    rest = rest[:-1]
    conditions = []
    for piece in rest.split(","):
        match piece.split(":"):
            case [dst]:
                conditions.append((dst, None, None))
                return src, conditions
            case [condition, dst]:
                index, comparison, value = "xmas".index(condition[0]), condition[1], int(condition[2:])
                match comparison:
                    case "<":
                        conditions.append((dst, index, Range(1, value)))
                    case ">":
                        conditions.append((dst, index, Range(value + 1, 4001)))

def get_rating(workflows, part):
    curr = "in"
    while curr not in { "A", "R" }:
        for next, i, r in workflows[curr]:
            if i is None or part[i] in r:
                curr = next
                break
    return sum(part) if curr == "A" else 0

def get_accepted_combinations(workflows):
    ret = 0
    q = deque()
    q.append(("in", [Range(1, 4001) for _ in "xmas"]))
    while q:
        curr, bounds = q.pop()
        match curr:
            case "A":
                ret += prod(r.size for r in bounds)
                continue
            case "R":
                continue
            case _:
                ranges = deepcopy(bounds)
                for next, i, r in workflows[curr]:
                    if not all(r.size > 0 for r in ranges):
                        break
                    if i is None:
                        q.append((next, ranges))
                        break
                    passed = deepcopy(ranges)
                    passed[i] &= r
                    ranges[i] -= r
                    q.append((next, passed))
    return ret

def solve(data):
    workflows = {}
    for line in data[0].split("\n"):
        src, conditions = parse_workflow(line)
        workflows[src] = conditions
    ans1 = sum(get_rating(workflows, part) for part in lmap(ints, data[1].split("\n")))
    ans2 = get_accepted_combinations(workflows)
    return ans1, ans2
