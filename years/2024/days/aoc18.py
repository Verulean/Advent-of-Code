from util import Dijkstra, Neighbors, binary_search, ints


fmt_dict = { "sep": None }

class ByteRunner(Dijkstra):
    def __init__(self, bytes, goal):
        super().__init__()
        self.bytes = bytes
        self.goal = goal
        self.start = (0, 0)
        self.get_neighbors = Neighbors(goal[0] + 1, goal[1] + 1, out_set=bytes)

    def is_goal(self, state):
        return state == self.goal

    def neighbors(self, state):
        return ((1, neighbor) for neighbor in self.get_neighbors(*state))

def find_path_length(bytes, goal):
    return ByteRunner(bytes, goal).run()

def find_blocker(all_bytes, goal):
    f = lambda t: find_path_length(set(all_bytes[:t]), goal) is None
    t = binary_search(0, len(all_bytes) - 1, f)
    return ",".join(map(str, all_bytes[t - 1]))

def solve(data):
    all_bytes = [tuple(ints(line)) for line in data.split()]
    t = 1024 if len(all_bytes) > 30 else 12
    goal = (70, 70) if len(all_bytes) > 30 else (6, 6)
    ans1 = find_path_length(set(all_bytes[:t]), goal)
    ans2 = find_blocker(all_bytes, goal)
    return ans1, ans2
