class Range:
    def __init__(self, *args):
        self.__intervals = []
        match len(args):
            case 1:
                x = args[0]
                if isinstance(x, int):
                    self.__intervals.append((0, args[0]))
                else:
                    self.__intervals.extend(map(list, x))
                    self.__normalize()
            case 2:
                self.__intervals.append(list(args[:2]))

    def __combine_intervals(self):
        for i in range(len(self.__intervals) - 2, -1, -1):
            (x1, y1), (x2, y2) = self.__intervals[i], self.__intervals[i + 1]
            if y1 >= x2:
                del self.__intervals[i]
                self.__intervals[i] = [min(x1, x2), max(y1, y2)]

    def __normalize(self):
        self.__intervals = sorted(self.__intervals)
        self.__combine_intervals()

    def __add_interval(self, x, y):
        if not self.__intervals or x > self.__intervals[-1][1]:
            self.__intervals.append([x, y])
            return
        if y < self.__intervals[0][0] - 1:
            self.__intervals.insert(0, [x, y])
            return
        overlap = False
        for i, (a, b) in enumerate(self.__intervals):
            if a <= x <= b:
                overlap = True
                self.__intervals[i][1] = max(y, b)
            elif a <= y <= b:
                overlap = True
                self.__intervals[i][0] = min(x, a)
            elif x <= a and y >= b:
                overlap = True
                self.__intervals[i] = (x, y)
        if overlap:
            self.__combine_intervals()
        else:
            for i, ((_, b), (c, _)) in enumerate(
                zip(self.__intervals, self.__intervals[1:])
            ):
                if b < x and y < c:
                    self.__intervals.insert(i + 1, [x, y])

    def __remove_interval(self, x, y):
        for i, (a, b) in reversed(list(enumerate(self.__intervals))):
            if x >= b or y <= a:
                continue
            elif x <= a and y >= b:
                del self.__intervals[i]
            elif x > a and y < b:
                self.__intervals[i][1] = x
                self.__intervals.insert(i + 1, [y, b])
            elif x > a:
                self.__intervals[i][1] = min(b, x)
            else:
                self.__intervals[i][0] = max(a, y)

    def __len__(self):
        return len(self.__intervals)

    def __add__(self, other):
        if isinstance(other, int):
            return Range((a + other, b + other) for a, b in self.__intervals)
        return self | other

    def __sub__(self, other):
        if isinstance(other, int):
            return Range((a - other, b - other) for a, b in self.__intervals)
        elif isinstance(other, tuple):
            difference = self.copy()
            difference.__remove_interval(other[0], other[1])
            return difference
        elif isinstance(other, Range):
            difference = self.copy()
            for a, b in other.__intervals:
                difference.__remove_interval(a, b)
            return difference
        return None

    def __or__(self, other):
        union = self.copy()
        if isinstance(other, tuple):
            union.__add_interval(other[0], other[1])
            return union
        elif isinstance(other, Range):
            for a, b in other.__intervals:
                union.__add_interval(a, b)
            return union
        return None

    def __and__(self, other):
        if not isinstance(other, (tuple, Range)):
            return None
        return self - (self - other)

    def __xor__(self, other):
        return (self | other) - (self & other)

    def __iter__(self):
        return (map(tuple, self.__intervals))

    def __eq__(self, other):
        return len(self) == len(other) and all(x == y for x, y in zip(self, other))

    def __contains__(self, other):
        if isinstance(other, int):
            return any(a <= other < b for a, b in self.__intervals)
        rng = Range(other)
        return rng == (self & rng)

    def __str__(self):
        return f"Range({self.__intervals})"

    def copy(self):
        return Range(self.__intervals)

    def clear(self):
        self.__intervals.clear()

    def values(self, reverse=False):
        if reverse:
            for a, b in reversed(self.__intervals):
                for n in range(b - 1, a - 1, -1):
                    yield n
        else:
            for a, b in self.__intervals:
                for n in range(a, b):
                    yield n

    def find_slot(self, n: int) -> int | None:
        for a, b in self.__intervals:
            if b - a >= n:
                return a
        return None

    @property
    def min(self):
        return self.__intervals[0][0] if self.__intervals else None

    @property
    def max(self):
        return self.__intervals[-1][1] - 1 if self.__intervals else None

    @property
    def size(self):
        return sum(b - a for a, b in self.__intervals)
