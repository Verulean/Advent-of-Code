from collections import defaultdict, deque
from math import gcd, lcm, prod
from numbers import Number
from operator import add, sub, mul
import hashlib
import numpy as np
import re


# Classes
from Neighbors import Neighbors
from PriorityQueue import PriorityQueue
from Range import Range
from Dijkstra import Dijkstra
from Search import BFS, DFS


# Constants
LETTERS = set("abcdefghijklmnopqrstuvwxyz")
VOWELS = set("aeiou")
CONSONANTS = LETTERS - VOWELS
NORTH = UP = (-1, 0)
NORTHEAST = UPRIGHT = (-1, 1)
EAST = RIGHT = (0, 1)
SOUTHEAST = DOWNRIGHT = (1, 1)
SOUTH = DOWN = (1, 0)
SOUTHWEST = DOWNLEFT = (1, -1)
WEST = LEFT = (0, -1)
NORTHWEST = UPLEFT = (-1, -1)
D4 = (NORTH, EAST, SOUTH, WEST)
D8 = (NORTH, NORTHEAST, EAST, SOUTHEAST, SOUTH, SOUTHWEST, WEST, NORTHWEST)


# Tuple Arithmetic
def __tuple_op(a, b, op):
    match isinstance(a, Number), isinstance(b, Number):
        case True, True:
            return op(a, b)
        case True, False:
            return tuple(op(a, x) for x in b)
        case False, True:
            return tuple(op(x, b) for x in a)
        case False, False:
            return tuple(op(x, y) for x, y in zip(a, b))

def tadd(a, b) -> tuple:
    return __tuple_op(a, b, add)

def tsub(a, b) -> tuple:
    return __tuple_op(a, b, sub)

def tmul(a, b) -> tuple:
    return __tuple_op(a, b, mul)

def tneg(a) -> tuple:
    return tuple(-x for x in a)

def trev(a) -> tuple:
    return tuple(reversed(a))


# Iterable Manipulation
def lmap(func, iterable):
    """list . map"""
    return list(map(func, iterable))

def smap(func, iterable):
    """sum . map"""
    return sum(map(func, iterable))

def minmap(func, iterable):
    """min . map"""
    return min(map(func, iterable))

def maxmap(func, iterable):
    """max . map"""
    return max(map(func, iterable))

def rotate(iterable, n=1):
    d = deque(iterable)
    d.rotate(n)
    return d

def chunks(l, n: int):
    """Yields sub-lists of length `n` of `l`."""
    for i in range(0, len(l), n):
        yield l[i : i + n]

def parts(l, n: int):
    """Yields `n` equal-length sub-lists of `l`."""
    m = len(l) // n
    for i in range(n):
        yield l[i * m : (i + 1) * m]
    if len(l) % n:
        yield l[m * n :]

def windowed(l, n: int):
    """Returns subsequences of length `n` of `l`, starting from each index."""
    return zip(*(l[i:] for i in range(n)))

def is_unique(l) -> bool:
    """Returns whether a collection contains only unique elements."""
    return len(set(l)) == len(l)


# String Parsing
def ints(s: str, negatives: bool=True) -> list[int]:
    """Returns numeric digits of a string as integers.
    
    Parameters:
    s - String to search
    negatives - Whether hyphens indicate negative numbers"""
    pattern = r"\-?\d+" if negatives else r"\d+"
    return lmap(int, re.findall(pattern, s))

def try_int(s: str) -> int | str:
    """Converts input to an integer if possible."""
    try:
        return int(s)
    except ValueError:
        return s

def split_ints(s: str) -> list[int | str]:
    """Splits a string, then converts any numeric elements to integers."""
    return lmap(try_int, s.split())

def floats(s: str, negatives: bool=True) -> list[float]:
    """Returns floating point numbers from a string.
    
    Parameters:
    s - String to search
    negatives - Whether hyphens indicate negative numbers"""
    pattern = r"-?\d+(?:\.\d+)?" if negatives else r"\d+(?:\.\d+)?"
    return lmap(float, re.findall(pattern, s))

def try_float(s: str) -> float | str:
    """Converts input to a float if possible."""
    try:
        return float(s)
    except ValueError:
        return s

def split_floats(s: str) -> list[float | str]:
    """Splits a string, then converts any numeric elements to floats."""
    return lmap(try_float, s.split())

def words(s: str) -> list[str]:
    """Returns alphabetic substrings from a string."""
    return re.findall(r"[A-Za-z]+", s)

def ordch(c: str) -> int:
    """Returns the ordinal of an alphabetic character. A=0, B=1, ..., Z=25"""
    if len(c) == 1 and c.isalpha():
        if c.islower():
            return ord(c) - ord("a")
        return ord(c) - ord("A")
    return None


# Math
def quadratic(a, b, c):
    discriminant = (b ** 2 - 4 * a * c) ** 0.5
    return (-b - discriminant) / 2 / a, (-b + discriminant) / 2 / a

def factors(n: int) -> list[int]:
    """Returns all factors of a natural number."""
    return [d for d in range(1, int(n**0.5) + 1) if n % d == 0]

def prime_factors(n: int) -> dict[int, int]:
    factors = defaultdict(int)
    while n % 2 == 0:
        factors[2] += 1
        n //= 2
    for d in range(3, int(n ** 0.5) + 1, 2):
        while n % d == 0:
            factors[d] += 1
            n //= d
    if n > 2:
        factors[n] += 1
    return factors

def chinese_remainder_theorem(remainders, moduli) -> int:
    # Decompose composite moduli into prime powers
    expanded_congruences = defaultdict(list)
    for remainder, modulo in zip(remainders, moduli):
        for prime, power in prime_factors(modulo).items():
            expanded_congruences[prime].append((power, remainder % (prime ** power)))
    # Check for conflicting congruences
    base_congruences = defaultdict(set)
    max_power = defaultdict(int)
    max_remainder = {}
    for prime, candidates in expanded_congruences.items():
        for power, remainder in candidates:
            base_congruences[prime].add(remainder % prime)
            if power > max_power[prime]:
                max_power[prime] = power
                max_remainder[prime] = remainder
    if any(len(r) > 1 for r in base_congruences.values()):
        return None
    # Apply coprime CRT
    congruences = { p ** power: max_remainder[p] for p, power in max_power.items() }
    P = prod(congruences)
    a = 0
    for modulo, remainder in congruences.items():
        M = P // modulo
        N = pow(M, -1, modulo)
        a += remainder * M * N
    return a

def sync_cycles(starts, lengths, offsets) -> int:
    """Returns the first iteration where all cycles coincide.
    
    Parameters:
    cycles - Iterable containing (cycle_start, cycle_length, end_offset)"""
    LCM = lcm(*lengths)
    n = chinese_remainder_theorem((s + o for s, o in zip(starts, offsets)), lengths) % LCM
    return n if n > 0 else LCM

def shoelace(xs, ys=None) -> int:
    points = xs if ys is None else zip(xs, ys)
    return abs(sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(points, rotate(points)))) >> 1


# Hashing
def md5(s) -> str:
    """MD5 hash."""
    h = hashlib.md5()
    h.update(s)
    return h.hexdigest()

def sha256(s) -> str:
    """SHA 256 hash."""
    h = hashlib.sha256()
    h.update(s)
    return h.hexdigest()


# Numpy Interfaces
def grid_to_string(grid, func=str, sep="") -> str:
    """Converts a grid to a string representation.
    
    Parameters:
    grid - The grid
    func - Function that converts each element to a string
    sep - Separator for the elements in each grid row"""
    return "\n".join(map(lambda seq: sep.join(map(func, seq)), grid))

def to_array(x, f=None, row_delimiter=None, col_delimiter=None, dtype=None):
    if f is None:
        f = lambda e: e
    if not isinstance(x, str):
        return np.array([[f(e) for e in row] for row in x], dtype)
    if row_delimiter is None:
        row_delimiter = "\n"
    match isinstance(row_delimiter, str), isinstance(col_delimiter, str):
        case True, True:
            return np.array([[f(e) for e in row.split(col_delimiter)] for row in x.split(row_delimiter)], dtype)
        case True, False:
            return np.array([[f(e) for e in row] for row in x.split(row_delimiter)], dtype)
        case False, True:
            raise ValueError("column delimiter provided without row delimiter")
        case False, False:
            return np.array([f(x)], dtype)


# Misc
def merge(A, left, right, end, B, f):
    i, j = left, right
    for k in range(left, end):
        if i < right and (j >= end or f(A[i], A[j])):
            B[k] = A[i]
            i += 1
        else:
            B[k] = A[j]
            j += 1

def merge_sort(A, f):
    """Returns the sorted input array.
    
    Parameters:
    A - The array to sort
    f - Comparison function f(a, b), returns True if `a` should be sorted before `b`"""
    n = len(A)
    B = [None] * n
    l = 1
    while l < n:
        for i in range(0, n, l * 2):
            merge(A, i, min(i + l, n), min(i + 2 * l, n), B, f)
        A[:] = B
        l *= 2
    return A

def grid_where(grid, value) -> set[tuple[int]]:
    """Returns a set of indices where a grid is equal to a given value."""
    return { (i, j) for i, line in enumerate(grid) for j, elem in enumerate(line) if elem == value }

def grid_find(grid, value) -> tuple[int] | None:
    """Returns the indices of the first occurrence of a given value in a grid."""
    for i, line in enumerate(grid):
        for j, elem in enumerate(line):
            if elem == value:
                return i, j
    return None

def rotate_direction(direction, angle=90) -> tuple[int]:
    """Rotates a direction by a given angle.
    
    Parameters:
    direction - The direction to rotate, as a tuple of two ints.
    angle - The angle, in degrees, to rotate, where clockwise is positive. Must be a multiple of 45, defaults to 90"""
    return D8[(D8.index(direction) + angle // 45) % 8]
