from importlib.util import module_from_spec, spec_from_file_location
from timeit import timeit
from pathlib import Path
import requests


CURRENT_WORKING_DIRECTORY = Path(__file__).parent


def aoc_import(year: int, day: int, file_suffix: str = ""):
    spec = spec_from_file_location(
        f"aoc{day:02}",
        CURRENT_WORKING_DIRECTORY.joinpath("years", str(year), "days", f"aoc{day:02}{file_suffix}.py")
    )
    aoc = module_from_spec(spec)
    spec.loader.exec_module(aoc)
    return aoc

def aoc_input(
    year: int,
    day: int,
    cast_type = str,
    strip: bool = True,
    sep: str = "\n",
    file_prefix: str = "",
    download: bool = True,
    **kwargs
):
    file_path = CURRENT_WORKING_DIRECTORY.joinpath("years", str(year), "input", f"{file_prefix}{day:02n}.txt")
    if not file_path.exists():
        if download:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            download_input(year, day, file_path)
        else:
            return []

    with open(file_path) as f:
        if sep is None:
            return f.read().rstrip("\n")
        return [
            cast_type(i.strip()) if strip else cast_type(i)
            for i in f.read().rstrip("\n").split(sep)
        ]


def download_input(year: int, day: int, path: Path) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    session_id = get_session_id()
    if session_id is None:
        return
    kwargs = {
        "headers": {
            "User-Agent": "github.com/Verulean/Advent-of-Code discord:@verulean"
        },
        "cookies": {"session": session_id},
    }
    response = requests.get(url, **kwargs)
    if not response.ok:
        raise RuntimeError(f"Request failed. {response.content}")
    with open(path, "w+") as f:
        f.write(response.text.rstrip("\n"))


def get_session_id() -> str | None:
    with open("session.cookie") as f:
        return f.read().strip()
    return None


def time_to_string(n: int, solve, data, pad: int = 11) -> str:
    units = ((1e0, "s"), (1e-3, "ms"), (1e-6, "μs"), (1e-9, "ns"))
    t = timeit(lambda: solve(data), number=n) / n

    for magnitude, unit in units:
        if t > magnitude:
            return f"{t/magnitude:.4f} {unit}".rjust(pad)
