# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import TypeVar

    _Data = list[str]
    _Cycle = int
    _X = int
    _T = TypeVar("_T")
    _BasicGenerator = Generator[_T, None, None]


class Solution(SolutionAbstract):
    day = 10
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 10 data.
        """
        return [line.strip() for line in raw_data]

    def part_1(self) -> int:
        """
        Day 10 part 1 solution.
        """
        cpu = _Cpu()
        data = cpu.run_program(self.data)
        return sum(cycle * x for cycle, x in data if cycle % 40 == 20)

    def part_2(self) -> None:  # Manual submission
        """
        Day 10 part 2 solution.
        """
        cpu = _Cpu()
        data = cpu.run_program(self.data)

        # 2-wide for easier recognition
        empty_value = "  "
        filled_value = "##"

        crt = [[empty_value] * 40 for _ in range(6)]
        for cycle, x in data:
            r, c = divmod(cycle - 1, 40)
            if x - 1 <= c <= x + 1:
                crt[r][c] = filled_value
        for row in crt:
            print("".join(row))


class _Cpu:
    """"""

    cycle: _Cycle
    x: _X

    def __init__(self) -> None:
        self.cycle = 0
        self.x = 1

    def run_program(self, program: list[str]) -> _BasicGenerator[tuple[_Cycle, _X]]:
        """"""
        for line in program:
            match line.split():
                case ["noop"]:
                    yield self._inc_cycle()
                case ["addx", value_str]:
                    value = int(value_str)
                    for _ in range(2):
                        yield self._inc_cycle()
                    self.x += value
                case _:
                    raise ValueError(f"Unknown command {line}")

    def _inc_cycle(self) -> tuple[_Cycle, _X]:
        """"""
        self.cycle += 1
        return self.cycle, self.x
