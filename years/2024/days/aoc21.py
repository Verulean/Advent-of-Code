from collections import deque
from functools import cache


def parse_pad(pad):
    key_to_pos = {}
    ignore = None
    for i, row in enumerate(pad):
        for j, key in enumerate(row):
            match key:
                case " ":
                    ignore = i + j * 1j
                case _:
                    key_to_pos[key] = i + j * 1j
    return ignore, key_to_pos

NUMPAD = parse_pad(["789", "456", "123", " 0A"])
KEYPAD = parse_pad([" ^A", "<v>"])

@cache
def get_inputs(start, end, ignore):
    paths = set()
    q = deque()
    q.append((start, ""))
    while q:
        pos, input = q.popleft()
        if pos == end:
            paths.add(input + "A")
            continue
        if pos == ignore:
            continue
        if pos.real < end.real:
            q.append((pos + 1, input + "v"))
        elif pos.real > end.real:
            q.append((pos - 1, input + "^"))
        if pos.imag < end.imag:
            q.append((pos + 1j, input + ">"))
        elif pos.imag > end.imag:
            q.append((pos - 1j, input + "<"))
    return paths

@cache
def find_shortest(code, robots=2, layer=0):
    if layer == robots + 1:
        return len(code)
    ignore, key_to_pos = KEYPAD if layer else NUMPAD
    length = 0
    pos = key_to_pos["A"]
    for c in code:
        next_pos = key_to_pos[c]
        length += min(find_shortest(
            subcode,
            robots,
            layer + 1
        ) for subcode in get_inputs(pos, next_pos, ignore))
        pos = next_pos
    return length

def solve(data):
    ans1 = 0
    ans2 = 0
    for code in data:
        numeric_piece = int(code.lstrip("0").rstrip("A"))
        ans1 += find_shortest(code) * numeric_piece
        ans2 += find_shortest(code, robots=25) * numeric_piece
    return ans1, ans2
