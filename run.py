# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import argparse
import shutil
import webbrowser
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from colorama import Fore, init

from aoc_io import download_input, submit_output

if TYPE_CHECKING:
    from .utils import SolutionAbstract

init(autoreset=True)

_PREPARATION_COMMANDS = {"e", "er", "prepare"}
_DOWNLOAD_COMMANDS = {"d", "dl", "download"}
_PRINT_COMMANDS = {"p", "pr", "print"}
_SUBMIT_COMMANDS = {"s", "sub", "submit"}
_ALL_COMMANDS = (
    _PREPARATION_COMMANDS | _DOWNLOAD_COMMANDS | _PRINT_COMMANDS | _SUBMIT_COMMANDS
)


def _main() -> None:
    parser = argparse.ArgumentParser(description="AoC 2021 day 01")
    parser.add_argument("command", choices=_ALL_COMMANDS)
    parser.add_argument("day", type=int, choices=range(1, 26))
    parser.add_argument("part", type=int, choices=(1, 2), nargs="?")
    args = parser.parse_args()

    # Prepare
    if args.command in _PREPARATION_COMMANDS:
        parent_dir = Path(__file__).resolve().parent
        target_dir = parent_dir / f"day_{args.day:>02}"
        if not target_dir.exists():
            origin_dir = parent_dir / "day_xx"
            shutil.copytree(origin_dir, target_dir)
        for subpath in target_dir.iterdir():
            if subpath.suffix not in {".md", ".py"}:
                continue
            with subpath.open("r") as f:
                data = f.read()
            data = data.replace("xx", f"{args.day:>02}").replace("-1", str(args.day))
            with subpath.open("w") as f:
                f.write(data)
        webbrowser.open("https://adventofcode.com/2021")
        download_input(day=args.day)
        return

    # Download input
    if args.command in _DOWNLOAD_COMMANDS:
        download_input(day=args.day)
        return

    # Run and get solution
    if args.part is None:
        raise ValueError("No part number provided.")
    solution = _get_solution(args.day, args.part)
    if solution is None:
        print(f"{Fore.RED}No response got. This part may need manual processing.")
        return
    if args.command in _PRINT_COMMANDS:
        print(f"{Fore.GREEN}Got solution {solution!r}")
    elif args.command in _SUBMIT_COMMANDS:
        print(f"{Fore.GREEN}Got solution {solution!r}")
        submit_output(day=args.day, part=args.part, answer=solution)


def _get_solution(day: int, part: int) -> str | int:
    """"""
    dir_name = f"day_{day:>02}"
    solution_module = import_module(f"{dir_name}.solution")
    SolutionClass: type[SolutionAbstract] = getattr(solution_module, "Solution")
    solution_obj = SolutionClass()
    if part == 1:
        return solution_obj.part_1()
    elif part == 2:
        return solution_obj.part_2()
    else:
        raise ValueError(f"Unknown part number {part}.")


if __name__ == "__main__":
    _main()
