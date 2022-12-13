# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Literal

    _PacketContent = int | list["_PacketContent"]
    _Data = list["_PacketPair"]


class Solution(SolutionAbstract):
    day = 13
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 13 data.
        """
        it = iter(raw_data)
        data: list[_PacketPair] = []
        while True:
            left = _Packet(eval(next(it)))
            right = _Packet(eval(next(it)))
            data.append(_PacketPair(left=left, right=right))
            try:
                next(it)
            except StopIteration:
                break

        return data

    def part_1(self) -> int:
        """
        Day 13 part 1 solution.
        """
        return sum(i for i, pair in enumerate(self.data, start=1) if pair.is_in_order())

    def part_2(self) -> int:
        """
        Day 13 part 2 solution.
        """
        packets = [packet for pair in self.data for packet in (pair.left, pair.right)]
        packets.extend([_Packet([[2]]), _Packet([[6]])])
        packets.sort()

        prod = 1
        for i, packet in enumerate(packets, start=1):
            if packet.data == [[2]] or packet.data == [[6]]:
                prod *= i
        return prod


@total_ordering
@dataclass(frozen=True)
class _Packet:
    """"""

    data: _PacketContent

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, _Packet):
            return _compare_packet_contents(self.data, __o.data) == 0
        return NotImplemented

    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, _Packet):
            return _compare_packet_contents(self.data, __o.data) == -1
        return NotImplemented


@dataclass(frozen=True, kw_only=True)
class _PacketPair:
    """"""

    left: _Packet
    right: _Packet

    def is_in_order(self) -> bool:
        """"""
        return self.left < self.right


def _compare_packet_contents(
    left: _PacketContent, right: _PacketContent
) -> Literal[-1, 0, 1]:
    """"""
    if isinstance(left, int):
        if isinstance(right, int):
            match left - right:
                case n if n < 0:
                    return -1
                case n if n > 0:
                    return 1
                case _:
                    return 0
        else:
            return _compare_packet_contents([left], right)
    else:
        if isinstance(right, int):
            return _compare_packet_contents(left, [right])
        else:
            for i in range(len(left)):
                left_el = left[i]
                try:
                    right_el = right[i]
                except IndexError:
                    return 1
                compare = _compare_packet_contents(left_el, right_el)
                if compare != 0:
                    return compare
            if len(left) < len(right):
                return -1
            return 0
