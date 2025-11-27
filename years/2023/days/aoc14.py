from itertools import cycle
from util import to_array
import numpy as np


def trunc_roll(arr, dir, axis):
    rolled = np.roll(arr, dir, axis)
    m, n = rolled.shape
    match axis, dir:
        case 0, -1:
            rolled[m - 1, :] = False
        case 0, 1:
            rolled[0, :] = False
        case 1, -1:
            rolled[:, n - 1] = False
        case 1, 1:
            rolled[:, 0] = False
    return rolled

class RockAndRoll:
    __DIRECTIONS = ((-1, 0), (-1, 1), (1, 0), (1, 1))
    def __init__(self, rounded_rocks, cube_rocks):
        self.__round = RockAndRoll.__to_nested_tuple(rounded_rocks)
        self.__cube = np.array(cube_rocks)
        self.__round_to_iteration = { self.__round: 0 }
        self.__iteration_to_round = { 0: self.__round }
        self.__cycle_start = None
        self.__cycle_length = None
        self.__find_cycle()

    @classmethod
    def from_input(cls, lines):
        arr = to_array(lines)
        return cls(arr == "O", arr == "#")

    @staticmethod
    def __to_nested_tuple(arr):
        return tuple(tuple(row) for row in arr)

    def __roll_rocks(self, round, shift, axis):
        round = np.array(round)
        can_roll = round & trunc_roll(~(self.__cube | round), -shift, axis)
        while np.any(can_roll):
            round = np.roll(can_roll, shift, axis) | (round & ~can_roll)
            can_roll = round & trunc_roll(~(self.__cube | round), -shift, axis)
        return RockAndRoll.__to_nested_tuple(round)

    def __find_cycle(self):
        round = self.__round
        for i, d in enumerate(cycle(self.__DIRECTIONS)):
            round = self.__roll_rocks(round, *d)
            j = self.__round_to_iteration.get((round, d), None)
            if j is not None:
                self.__cycle_start = j
                self.__cycle_length = i - j + 1
                break
            self.__round_to_iteration[(round, d)] = i + 1
            self.__iteration_to_round[i + 1] = round

    def __cycle_index(self, i):
        if i < self.__cycle_start + self.__cycle_length:
            return i
        return (i - self.__cycle_start) % self.__cycle_length + self.__cycle_start

    def total_load(self, i):
        round = self.__iteration_to_round[self.__cycle_index(i)]
        m = len(round)
        return sum((m - i) * sum(row) for i, row in enumerate(round))

def solve(data):
    r = RockAndRoll.from_input(data)
    return r.total_load(1), r.total_load(4_000_000_000)
