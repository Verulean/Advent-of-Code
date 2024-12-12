from datetime import datetime
from pyperclip import copy
from pytz import timezone
import aoc_util


DT_NOW = datetime.now(timezone("America/New_York"))
CURRENT_YEAR = DT_NOW.year
CURRENT_DAY = DT_NOW.day


def main(
    n=min(CURRENT_DAY, 25),
    time=False,
    n_trials=1000,
    print_solution=True,
    file_suffix="",
):
    aoc = aoc_util.aoc_import(n, file_suffix)
    fmt = getattr(aoc, "fmt_dict", {})
    data = aoc_util.aoc_input(n, **fmt)

    if fmt.get("test", False):
        test_data = aoc_util.aoc_input(n, **(fmt | {"file_prefix": "t"}))
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

        print(f"Day {str(n).rjust(2)}: {result}")

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
    main()
