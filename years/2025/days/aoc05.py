from util import Range


fmt_dict = { "sep": "\n\n" }

def solve(data: list[str]) -> tuple[int, int]:
    fresh = Range()
    for line in data[0].split():
        a, b = map(int, line.split("-"))
        fresh |= (a, b + 1)
    ans1 = sum(1 for n in map(int, data[1].split()) if n in fresh)
    return ans1, fresh.size
