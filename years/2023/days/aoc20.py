from collections import defaultdict, deque
from math import prod


def parse_modules(lines):
    graph = {}
    inverse_graph = defaultdict(set)
    flipflops = {}
    conjunctions = {}
    for line in lines:
        src, dests = line.split(" -> ")
        dests = dests.split(", ")
        match src[0]:
            case "%":
                src = src[1:]
                flipflops[src] = False
            case "&":
                src = src[1:]
                conjunctions[src] = {}
        graph[src] = set(dests)
        for dest in dests:
            inverse_graph[dest].add(src)
    for dest in conjunctions:
        conjunctions[dest] = { src: False for src in inverse_graph[dest] }
    return graph, inverse_graph, flipflops, conjunctions

def run_simulation(graph, flipflops, conjunctions, steps):
    pulses = [0, 0]
    q = deque()
    for _ in range(steps):
        q.append((None, "broadcaster", False))
        while q:
            sender, node, state = q.popleft()
            pulses[state] += 1
            if node in conjunctions:
                conjunctions[node][sender] = state
                state = not all(conjunctions[node].values())
            elif node in flipflops:
                if not state:
                    state = flipflops[node] = not flipflops[node]
                else:
                    continue
            for adj in graph.get(node, set()):
                q.append((node, adj, state))
    return prod(pulses)

def decode_counters(graph, inverse_graph):
    subcycles = []
    binary_encoders = { inverse_graph[node].pop() for node in inverse_graph[inverse_graph["rx"].pop()] }
    for head in graph["broadcaster"]:
        curr = head
        bits = []
        while curr not in binary_encoders:
            receivers = graph[curr]
            c, f = receivers & binary_encoders, receivers - binary_encoders
            bits.append(1 if c else 0)
            curr = f.pop() if f else c.pop()
        length = 0
        for b in reversed(bits):
            length = (length << 1) + b
        subcycles.append(length)
    return prod(subcycles)

def solve(data):
    graph, inverse_graph, flipflops, conjunctions = parse_modules(data)
    ans1 = run_simulation(graph, flipflops, conjunctions, 1000)
    ans2 = decode_counters(graph, inverse_graph)
    return ans1, ans2
