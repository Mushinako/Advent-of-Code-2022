# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from utils import SolutionAbstract

if TYPE_CHECKING:
    from typing import Self


class Solution(SolutionAbstract):
    day = 5
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 05 data.
        """
        # Skip and store supplies, parse actions
        supplies_data: list[str] = []
        actions: list[_Action] = []
        supplies_data_ended = False
        for row in raw_data:
            if not row:
                supplies_data_ended = True
                continue
            if supplies_data_ended:
                actions.append(_Action.from_input(row))
            else:
                supplies_data.append(row)

        # Remove numbers row
        supplies_data.pop()

        # Parse stacks. Each stack is from bottom to top
        supplies_data.reverse()
        row_len = len(supplies_data[0])
        # `[A] ` is length 4. Pad a space at the end of the last one and the full
        #   length should be 4x stack count
        if (row_len + 1) % 4:
            raise ValueError(f"Unexpected row length: {row_len}")
        stack_count = (row_len + 1) // 4
        stacks: list[_Stack] = [_Stack([]) for _ in range(stack_count)]
        for row in supplies_data:
            for i in range(stack_count):
                # Stack name at second letter of the 4-letter group
                index = 4 * i + 1
                if crate := row[index].strip():
                    stacks[i].stack(crate)

        return _Data(stacks=stacks, actions=actions)

    def part_1(self) -> str:
        """
        Day 05 part 1 solution.
        """
        for action in self.data.actions:
            from_stack = self.data.stacks[action.from_ - 1]
            to_stack = self.data.stacks[action.to - 1]
            to_stack.stack(*reversed(from_stack.take(action.move_count)))
        return "".join(stack.items[-1] for stack in self.data.stacks)

    def part_2(self) -> str:
        """
        Day 05 part 2 solution.
        """
        for action in self.data.actions:
            from_stack = self.data.stacks[action.from_ - 1]
            to_stack = self.data.stacks[action.to - 1]
            to_stack.stack(*from_stack.take(action.move_count))
        return "".join(stack.items[-1] for stack in self.data.stacks)


@dataclass(frozen=True, kw_only=True)
class _Data:
    """"""

    stacks: list[_Stack]
    actions: list[_Action]


@dataclass(frozen=True)
class _Stack:
    """
    A stack of crates, from bottom to top
    """

    items: list[str]

    def stack(self, *items: str) -> None:
        """"""
        self.items.extend(items)

    def take(self, count: int) -> tuple[str]:
        """"""
        if len(self.items) < count:
            raise ValueError(f"Not enough to take: {len(self.items)} < {count}")
        taken = tuple(self.items[-count:])
        del self.items[-count:]
        return taken


@dataclass(frozen=True, kw_only=True)
class _Action:
    """"""

    _INPUT_RE: ClassVar[re.Pattern[str]] = re.compile(
        r"^move (\d+) from (\d+) to (\d+)$"
    )

    move_count: int
    from_: int
    to: int

    @classmethod
    def from_input(cls, input_: str) -> Self:
        """"""
        match = cls._INPUT_RE.fullmatch(input_)
        if match is None:
            raise ValueError(f"Invalid input: {input_}")
        return cls(move_count=int(match[1]), from_=int(match[2]), to=int(match[3]))
