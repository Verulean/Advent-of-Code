from collections import defaultdict
from itertools import combinations
from math import prod


fmt_dict = { "cast_type": lambda x: tuple(map(int, x.split(","))) }

Junction = tuple[int]

class Graph(defaultdict):
    def __init__(self):
        super().__init__(set)

    def add_junction(self, u: Junction) -> None:
        self[u].add(u)

    def connect(self, u: Junction, v: Junction) -> None:
        if v in self[u]:
            return
        self[u] |= self[v]
        for node in self[v]:
            self[node] = self[u]

    def get_circuits(self) -> list[set[Junction]]:
        junctions = set(self.keys())
        circuits = []
        while junctions:
            circuit = self[junctions.pop()]
            circuits.append(circuit)
            junctions -= circuit
        return circuits

    def is_connected(self) -> bool:
        return len(next(iter(self.values()))) == len(self)

def dist(connection: tuple[Junction, Junction]) -> int:
    u, v = connection
    return (u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2 + (u[2] - v[2]) ** 2 

def solve(data: list[Junction]) -> tuple[int, int | None]:
    connection_count = 1000
    graph = Graph()
    for p in data:
        graph.add_junction(p)
    connections = sorted(combinations(data, 2), key=dist)
    for u, v in connections[:connection_count]:
        graph.connect(u, v)
    ans1 = prod(sorted(map(len, graph.get_circuits()))[-3:])
    for u, v in connections[connection_count:]:
        graph.connect(u, v)
        if graph.is_connected():
            return ans1, u[0] * v[0]
    return ans1, None
