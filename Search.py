from collections import deque


class Search:
    start = None
    start_cost = 0

    def __init__(self, cost_comparison, append):
        self.cost = self.start_cost
        self.__cost_comparison = cost_comparison
        self.__append = append

    def is_goal(self, state) -> bool:
        return False

    def neighbors(self, state):
        pass

    def run(self):
        self.cost = None
        q = deque()
        self.__append(q, (self.start_cost, self.start))
        while q:
            cost, state = q.pop()
            if self.is_goal(state):
                self.cost = cost if self.cost is None else self.__cost_comparison(self.cost, cost)
            for d_cost, adj_state in self.neighbors(state):
                self.__append(q, (cost + d_cost, adj_state))
        return self.cost

class BFS(Search):
    def __init__(self, maximize=False):
        super().__init__(max if maximize else min, deque.appendleft)

class DFS(Search):
    def __init__(self, maximize=False):
        super().__init__(max if maximize else min, deque.append)
