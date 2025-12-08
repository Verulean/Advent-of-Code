from collections import Counter


def solve(data: list[str]) -> tuple[int, int]:
    beams = Counter([data[0].index("S")])
    ans1 = 0
    for row in data:
        for j, c in enumerate(row):
            match c:
                case "S":
                    beams[j] = 1
                case "^":
                    n = beams[j]
                    if n:
                        beams[j - 1] += n
                        beams[j + 1] += n
                        beams[j] = 0
                        ans1 += 1
    return ans1, sum(beams.values())
