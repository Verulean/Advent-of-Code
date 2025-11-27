from math import prod
import networkx


def solve(data):
    g = networkx.Graph()
    for line in data:
        source, dests = line.split(": ")
        dests = dests.split()
        g.add_node(source)
        for dest in dests:
            g.add_edge(source, dest)
    g.remove_edges_from(networkx.minimum_edge_cut(g))
    return prod(map(len, networkx.connected_components(g)))
