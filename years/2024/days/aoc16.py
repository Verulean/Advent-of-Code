from collections import deque
from util import Dijkstra


class Reindeer(Dijkstra):
    def __init__(self, walls, start, end):
        super().__init__()
        self.walls = walls
        self.start = (start, 1j)
        self.end = end

    def is_goal(self, state):
        return state[0] == self.end

    def neighbors(self, state):
        p, d = state
        stepped = p + d
        if stepped not in self.walls:
            yield 1, (stepped, d)
        yield 1000, (p, d * 1j)
        yield 1000, (p, d * -1j)

    def count_bests(self, end_states):
        bests = set()
        if self.end_state is None or self.cost is None:
            return bests
        q = deque()
        for state in end_states:
            if self.g_score.get(state, None) == self.cost:
                bests.add(state)
                q.append(state)
        while q:
            state = q.popleft()
            cost = self.g_score[state]
            p, d = state
            unstepped = p - d
            if unstepped not in self.walls:
                prev_cost = cost - 1
                prev_state = unstepped, d
                if prev_cost >= 0 \
                    and prev_state not in bests \
                    and self.g_score.get(prev_state, None) == prev_cost:
                    bests.add(prev_state)
                    q.append(prev_state)
            prev_cost = cost - 1000
            if prev_cost >= 0:
                for rot in 1j, -1j:
                    prev_state = p, d * rot
                    if prev_state not in bests \
                        and self.g_score.get(prev_state, None) == prev_cost:
                        bests.add(prev_state)
                        q.append(prev_state)
        return len({ p for p, _ in bests })

def solve(data):
    walls = set()
    start = end = 0
    for i, row in enumerate(data):
        for j, c in enumerate(row):
            match c:
                case "#":
                    walls.add(i + j * 1j)
                case "S":
                    start = i + j * 1j
                case "E":
                    end = i + j * 1j
    reindeer = Reindeer(walls, start, end)
    return reindeer.run(), reindeer.count_bests([(end, d) for d in (-1, 1j, 1, -1j)])
