from collections import deque
from util import PriorityQueue


class Dijkstra:
    start = None
    start_cost = 0

    def __init__(self):
        self.came_from = {}
        self.end = None
        self.cost = self.start_cost

    def is_goal(self, state) -> bool:
        return False

    def neighbors(self, state):
        pass

    def reconstruct_path(self, state):
        path = deque([state])
        while state in self.came_from:
            state = self.came_from[state]
            path.appendleft(state)
        return path

    def reset(self):
        self.came_from.clear()
        self.end = None
        self.cost = None

    def run(self):
        self.reset()
        q = PriorityQueue()
        q.append((self.start_cost, self.start))
        seen = set()
        g_score = { self.start: self.start_cost }
        while q:
            cost, state = q.pop()
            if state in seen:
                continue
            seen.add(state)
            if self.is_goal(state):
                self.end = state
                self.cost = cost
                return cost
            for d_cost, adj_state in self.neighbors(state):
                new_cost = cost + d_cost
                best = g_score.get(adj_state, None)
                if best is None or new_cost < best:
                    self.came_from[adj_state] = state
                    g_score[adj_state] = new_cost
                    q.append((new_cost, adj_state))

    @property
    def path(self):
        return self.reconstruct_path(self.end)
