def solve(data: list[str]) -> tuple[int, int]:
    p = 50
    ans1, ans2 = 0, 0

    for line in data:
        offset = int(line[1:])
        if line.startswith("L"):
            offset *= -1
        rotations, p_new = divmod(p + offset, 100)

        # Part 1
        if not p_new:
            ans1 += 1

        # Part 2
        ans2 += abs(rotations)
        if offset < 0:
            if not p_new:
                ans2 += 1
            if not p:
                ans2 -= 1

        p = p_new

    return ans1, ans2
