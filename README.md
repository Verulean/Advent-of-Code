# Advent-of-Code
Python framework for solving Advent of Code problems.
## Quick Start Guide
1. Clone this repository and write your solutions for each day in `./days`, with the file name `aoc##.py`. For example `aoc01.py` for day 1, `aoc02.py` for day 2, etc.
2. `./days/template.py` is a solution file template set up with common imports. `fmt_dict` controls how the input is parsed into `data`.
3. Run `main.py` to run today's solution. The input is automatically downloaded and saved in `./input`. The answer from `solve(data)` will automatically be copied to your clipboard for submission. If `solve(data)` returns a tuple, e.g. the answers for both parts, only the last element of the tuple will be copied.
4. To run solutions from a previous year, edit `CURRENT_YEAR` to that year. To run a solution for a different day, call `main()` with the day number.
5. To benchmark the execution time of a solution, run `main()` with `time=True` and `n_trials` set to the number of trials to run. `main.py` will print the solution and runtime to the console.
## `fmt_dict`
The `fmt_dict` variable is an optional dictionary you can include in a solution file to change how `main.py` parses the input text.
* `fmt_dict["sep"]` is a delimiter string to split the input by. This will most commonly be something like `"\n"`, `"\n\n"`, or `" "`. Set `fmt_dict["sep"]` to `None` to not split the input. The default value if not defined is `"\n"`.
* `fmt_dict["strip"]` is a flag indicating whether to strip each element of the split string. The default value is `True`.
* `fmt_dict["cast_type"]` is a transform function to apply to each element of the split string. This can be helpful if each line of the input needs to be further parsed, e.g. `fmt_dict["cast_type"]=ints` will transform each line into a list of ints, passing a `list[list[int]]` to `solve(data)`. The default value is `str`.
* `fmt_dict["test"]` is a flag indicating whether the solution should run on sample input in addition to the real input. The sample input file should be saved in `./input/t##.txt`, where `##` is the day number. In other words, the sample input is named the same as the real input, prefixed by a `t`.
