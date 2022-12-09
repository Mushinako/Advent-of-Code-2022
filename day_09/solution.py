# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list[tuple[str, int]]


class Solution(SolutionAbstract):
    day = 9
    data: _Data

    @staticmethod
    def _process_data(raw_data: list[str]) -> _Data:
        """
        Process day 09 data.
        """
        data: _Data = []
        for line in raw_data:
            if not (row := line.strip()):
                continue
            direction, count = row.split()
            data.append((direction, int(count)))
        return data

    def part_1(self) -> int:
        """
        Day 09 part 1 solution.
        """
        visited: set[complex] = {0 + 0j}
        head = 0 + 0j
        tail = 0 + 0j
        for direction_str, count in self.data:
            match direction_str:
                case "U":
                    direction = 0 + 1j
                case "D":
                    direction = 0 - 1j
                case "L":
                    direction = -1 + 0j
                case "R":
                    direction = 1 + 0j
                case d:
                    raise ValueError(f"Unknown direction {d}")
            for _ in range(count):
                head += direction
                tail = self._pull(head, tail)
                visited.add(tail)

        return len(visited)

    def part_2(self) -> int:
        """
        Day 09 part 2 solution.
        """
        visited: set[complex] = {0 + 0j}
        segments = [0 + 0j] * 10
        for direction_str, count in self.data:
            match direction_str:
                case "U":
                    direction = 0 + 1j
                case "D":
                    direction = 0 - 1j
                case "L":
                    direction = -1 + 0j
                case "R":
                    direction = 1 + 0j
                case d:
                    raise ValueError(f"Unknown direction {d}")
            for _ in range(count):
                segments[0] += direction
                for i in range(len(segments) - 1):
                    segments[i + 1] = self._pull(segments[i], segments[i + 1])
                visited.add(segments[-1])

        return len(visited)

    def _pull(self, head: complex, tail: complex) -> complex:
        """"""
        diff = head - tail
        # Overlap or touching
        if -1 <= diff.real <= 1 and -1 <= diff.imag <= 1:
            return tail
        # Horizontal changes
        match diff.real:
            # Left
            case -1 | -2:
                real_move = -1
            # Same column
            case 0:
                real_move = 0
            # Right
            case 1 | 2:
                real_move = 1
            # Unknown
            case _:
                raise ValueError(f"Unknown diff {diff}")
        # Vertical changes
        match diff.imag:
            # Bottom
            case -1 | -2:
                imag_move = -1
            # Same row
            case 0:
                imag_move = 0
            # Top
            case 1 | 2:
                imag_move = 1
            # Unknown
            case _:
                raise ValueError(f"Unknown diff {diff}")
        return tail + complex(real_move, imag_move)
