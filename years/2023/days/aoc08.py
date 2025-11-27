from itertools import cycle
from util import sync_cycles


fmt_dict = { "sep": "\n\n" }

def find_cycle(turns, node_map, start, end_condition):
    if start not in node_map:
        return None
    node = start
    seen = {}
    for steps, turn in enumerate(cycle(turns), 1):
        node = node_map[node][turn]
        k = (node, steps % len(turns))
        first = seen.get(k, None)
        if first is None:
            seen[k] = steps
            continue
        cycle_start = first
        cycle_length = steps - first
        for (adj, _), step in seen.items():
            if end_condition(adj):
                return cycle_start, cycle_length, step - cycle_start

def solve(data):
    turns = tuple(d == "R" for d in data[0])
    node_map = {}
    starts = set()
    for line in data[1].splitlines():
        source, dests = line.split(" = ")
        left, right = dests.strip("()").split(", ")
        node_map[source] = (left, right)
        if source.endswith("A"):
            starts.add(source)
    # Part 1
    s, _, o = find_cycle(turns, node_map, "AAA", lambda n: n == "ZZZ")
    ans1 = s + o
    # Part 2
    cycle_starts, cycle_lengths, cycle_offsets = [], [], []
    for start in starts:
        s, l, o = find_cycle(turns, node_map, start, lambda n: n.endswith("Z"))
        cycle_starts.append(s)
        cycle_lengths.append(l)
        cycle_offsets.append(o)
    return ans1, sync_cycles(cycle_starts, cycle_lengths, cycle_offsets)
