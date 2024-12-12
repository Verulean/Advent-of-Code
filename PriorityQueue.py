import heapq


class PriorityQueue(list):
    def pop(self):
        return heapq.heappop(self)

    def push(self, value):
        return heapq.heappush(self, value)
