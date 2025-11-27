from functools import cache


fmt_dict = { "sep": "\n\n" }

def solve(data):
    patterns = set(data[0].split(", "))
    designs = data[1].split()
    @cache
    def count(design: str):
        if not design:
            return 1
        return sum(count(design.removeprefix(pattern)) for pattern in patterns if design.startswith(pattern))
    ans1 = sum(1 for d in designs if count(d) > 0)
    ans2 = sum(map(count, designs))
    return ans1, ans2
