# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list["_Report"]
    _X = int
    _Y = int
    _Coord = tuple[_X, _Y]
    _XRange = tuple[_X, _X]

_REPORT_RE = re.compile(
    r"^Sensor at x=(?P<sx>\-?\d+), y=(?P<sy>\-?\d+): "
    r"closest beacon is at x=(?P<bx>\-?\d+), y=(?P<by>\-?\d+)$"
)


class Solution(SolutionAbstract):
    day = 15
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 15 data.
        """
        data: list[_Report] = []
        for line in raw_data:
            match = _REPORT_RE.fullmatch(line)
            if match is None:
                raise ValueError(f"Invalid line: {line}")
            data.append(
                _Report(
                    sensor=(int(match["sx"]), int(match["sy"])),
                    beacon=(int(match["bx"]), int(match["by"])),
                )
            )
        return data

    def part_1(self) -> int:
        """
        Day 15 part 1 solution.
        """
        target_y = 2000000
        no_beacon_xs: set[_X] = set()
        for report in self.data:
            sx, sy = report.sensor
            d = report.distance
            if sy - d <= target_y <= sy + d:
                d_rem = d - abs(target_y - sy)
                for x in range(sx - d_rem, sx + d_rem + 1):
                    if (x, target_y) != report.beacon:
                        no_beacon_xs.add(x)
        return len(no_beacon_xs)

    def part_2(self) -> int:
        """
        Day 15 part 2 solution.
        """
        side = 4_000_000
        for y in range(side + 1):
            x_ranges = self._get_x_ranges(y)
            if len(x_ranges) == 2:
                x_ranges = sorted(x_ranges)
                x = x_ranges[0][1] + 1
            elif len(x_ranges) == 1:
                range_start, range_end = x_ranges[0]
                if range_start > 0 and range_end < side:
                    raise ValueError(f"Invalid X range combination: {x_ranges}")
                elif range_start > 1 or range_end < side - 1:
                    raise ValueError(f"Invalid X range combination: {x_ranges}")
                elif range_start == 1:
                    x = 0
                elif range_end == side - 1:
                    x = side
                else:
                    continue
            else:
                raise ValueError(f"Invalid X range combination: {x_ranges}")
            return x * side + y
        raise ValueError("No result found")

    def _get_x_ranges(self, y: _Y) -> list[_XRange]:
        """"""
        x_ranges: list[_XRange] = []
        for report in self.data:
            sx, sy = report.sensor
            d = report.distance
            if sy - d <= y <= sy + d:
                d_rem = d - abs(y - sy)
                x_ranges.append((sx - d_rem, sx + d_rem))
        if not x_ranges:
            raise ValueError(f"No X ranges found for y={y}")
        return self._combine_x_ranges(x_ranges)

    def _combine_x_ranges(self, ranges: list[_XRange]) -> list[_XRange]:
        """"""
        if len(ranges) == 1:
            return ranges
        ranges = sorted(ranges)
        last_start, last_end = ranges.pop()

        new_ranges: list[_XRange] = []
        i = 0
        broken = True
        for i, (range_start, range_end) in enumerate(ranges):
            # Completely after
            if range_start > last_end + 1:
                new_ranges.append((range_start, range_end))
                continue
            # Completely before
            if range_end < last_start - 1:
                new_ranges.append((range_start, range_end))
                continue
            # Some overlap or connects
            new_ranges.append((min(range_start, last_start), max(range_end, last_end)))
            break
        else:
            broken = False
        new_ranges += ranges[i + 1 :]

        if not broken:
            if len(new_ranges) <= 2:
                return new_ranges
            else:
                return self._combine_x_ranges(new_ranges[:-1]) + [new_ranges[-1]]

        return self._combine_x_ranges(new_ranges)


@dataclass(frozen=True, kw_only=True)
class _Report:
    sensor: _Coord
    beacon: _Coord

    @cached_property
    def distance(self) -> int:
        sx, sy = self.sensor
        bx, by = self.beacon
        return abs(sx - bx) + abs(sy - by)
