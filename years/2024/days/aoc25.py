fmt_dict = { "sep": "\n\n" }

def solve(data):
    locks, keys = [], []
    for block in data:
        bits = int("".join("1" if x == "#" else "0" for x in block.strip("#.").strip("\n")), 2)
        (locks if block[0] == "#" else keys).append(bits)
    return sum(not lock & key for lock in locks for key in keys)
