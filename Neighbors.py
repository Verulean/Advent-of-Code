class Neighbors:
    def __init__(self, mode=0, m=None, n=None, loop=False):
        self.__loop = loop
        self.__m = m
        self.__n = n

        if mode == 0:
            self.__offsets = ((1, 0), (0, 1), (-1, 0), (0, -1))
        elif mode == 1:
            self.__offsets = (
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
                (-1, -1),
                (0, -1),
                (1, -1),
            )

    def __call__(self, i, j):
        if self.__loop:
            for di, dj in self.__offsets:
                yield ((i + di) % self.__m, (j + dj) % self.__n)
        else:
            for di, dj in self.__offsets:
                if 0 <= i + di < self.__m and 0 <= j + dj < self.__n:
                    yield (i + di, j + dj)

    def __getitem__(self, pos):
        return self(*pos)
