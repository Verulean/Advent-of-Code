from datetime import datetime
from pyperclip import copy
from pytz import timezone
import aoc_util


def get_default_day(d: datetime) -> int:
    min_day = 1
    max_day = 25 if d.year < 2025 else 12
    if d < datetime(d.year, 12, min_day, tzinfo=d.tzinfo):
        return min_day
    if d > datetime(d.year, 12, max_day, tzinfo=d.tzinfo):
        return max_day
    return d.day

def main(
    year: int,
    day: int,
    time: bool = False,
    n_trials: int = 1000,
    print_solution: bool = True,
    file_suffix: str = "",
) -> None:
    aoc = aoc_util.aoc_import(year, day, file_suffix)
    fmt = getattr(aoc, "fmt_dict", {})
    data = aoc_util.aoc_input(year, day, **fmt)

    if fmt.get("test", False):
        test_data = aoc_util.aoc_input(year, day, **(fmt | {"file_prefix": "t"}))
        test_solution = aoc.solve(test_data)
        if print_solution:
            print("Example Solution:")
            if isinstance(test_solution, tuple):
                for part in test_solution:
                    print(part)
            else:
                print(test_solution)

    if time:
        t = aoc_util.time_to_string(n_trials, aoc.solve, data)
        if n_trials == 1:
            result = t
        else:
            result = f"average of {t} over {n_trials} runs."

        print(f"Day {str(day).rjust(2)}: {result}")

    solution = aoc.solve(data)
    if print_solution:
        print("\nPuzzle Solution:")
        if isinstance(solution, tuple):
            for part in solution:
                print(part)
            copy(str(solution[-1]))
        else:
            print(solution)
            copy(str(solution))
    return solution


if __name__ == "__main__":
    now = datetime.now(timezone("America/New_York"))
    day = get_default_day(now)
    main(now.year, day)
