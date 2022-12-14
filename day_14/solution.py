# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from enum import Enum
from itertools import count
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import TypeAlias

    _Data: TypeAlias = "_Map"
    _R = int
    _C = int
    _Coord = tuple[_R, _C]


class Solution(SolutionAbstract):
    day = 14
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 14 data.
        """
        line_strs = [
            [coord_str.strip().split(",") for coord_str in line.split("->")]
            for line in raw_data
        ]
        # Revert order
        lines = [[(int(r), int(c)) for c, r in line] for line in line_strs]
        return _Map(lines)

    def part_1(self) -> int:
        """
        Day 14 part 1 solution.
        """
        i = 0  # Make linter happy
        for i in count(0):
            stop_reason = self.data.drop_sand()
            if stop_reason == _Map.StopReason.VOID:
                break
        return i

    def part_2(self) -> int:
        """
        Day 14 part 2 solution.
        """
        self.data.add_floor()
        i = 0  # Make linter happy
        for i in count(0):
            stop_reason = self.data.drop_sand()
            if stop_reason == _Map.StopReason.FULL:
                break
        return i


class _Map:
    """"""

    map_: list[list[Block]]
    max_r: int
    has_floor: bool

    class Block(Enum):
        AIR = " "
        ROCK = "█"
        SAND = "."

    class StopReason(Enum):
        SETTLED = "settled"
        VOID = "void"
        FULL = "full"

    def __init__(self, lines: list[list[_Coord]]) -> None:
        self.max_r = max(r for line in lines for r, _ in line)
        max_c = 500 + self.max_r + 3
        self.map_ = [[_Map.Block.AIR] * (max_c + 1) for _ in range(self.max_r + 3)]
        self.has_floor = False

        for line in lines:
            self.add_line(line)

    def __str__(self) -> str:
        col_span = self.max_r + 1
        return "\n".join(
            "".join(cell.value for cell in row[500 - col_span : 500 + col_span + 1])
            for row in self.map_
        )

    def add_line(self, line: list[_Coord]) -> None:
        """"""
        line = line.copy()
        pr, pc = line.pop()
        self.map_[pr][pc] = _Map.Block.ROCK
        for r, c in reversed(line):
            if pr == r:
                if pc < c:
                    coords = ((r, ic) for ic in range(pc + 1, c + 1))
                else:
                    coords = ((r, ic) for ic in range(c, pc))
            elif pc == c:
                if pr < r:
                    coords = ((ir, c) for ir in range(pr + 1, r + 1))
                else:
                    coords = ((ir, c) for ir in range(r, pr))
            else:
                raise ValueError("Cannot for line of rocks")

            for cr, cc in coords:
                self.map_[cr][cc] = _Map.Block.ROCK

            pr = r
            pc = c

    def add_floor(self) -> None:
        """"""
        r = self.max_r + 2
        self.add_line([(r, 0), (r, len(self.map_[0]) - 1)])
        self.has_floor = True

    def drop_sand(self) -> StopReason:
        """"""
        r = 0
        c = 500
        if self.map_[r][c] != _Map.Block.AIR:
            return _Map.StopReason.FULL

        while True:
            nr = r + 1
            if not self.has_floor and nr > self.max_r:
                # Fell into the void
                return _Map.StopReason.VOID
            nc = c
            if self.map_[nr][nc] != _Map.Block.AIR:
                # Try bottom left
                nc = c - 1
                if self.map_[nr][nc] != _Map.Block.AIR:
                    # Try bottom right
                    nc = c + 1
                    if self.map_[nr][nc] != _Map.Block.AIR:
                        # Settle on top
                        self.map_[r][c] = _Map.Block.SAND
                        return _Map.StopReason.SETTLED
            # Keep dropping
            r = nr
            c = nc
