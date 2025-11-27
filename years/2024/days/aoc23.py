from collections import deque, defaultdict


def get_triples(connections):
    return {
        tuple(sorted([a, b, c]))
        for a, adjs in connections.items() if a.startswith("t")
        for b in adjs
        for c in adjs & connections[b]
    }

def get_max_clique(connections):
    max_clique = set()
    computers = sorted(connections)
    for i, c1 in enumerate(computers):
        for c2 in computers[i + 1:]:
            if c2 not in connections[c1]:
                continue
            clique = set()
            q = deque()
            q.extend([c1, c2])
            while q:
                node = q.popleft()
                if node in clique:
                    continue
                if not (clique <= connections[node]):
                    continue
                clique.add(node)
                for adj in connections[node] - clique:
                    q.append(adj)
            max_clique = max(max_clique, clique, key=len)
    return max_clique

def solve(data):
    connections = defaultdict(set)
    for line in data:
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)
    return len(get_triples(connections)), ",".join(sorted(get_max_clique(connections)))
