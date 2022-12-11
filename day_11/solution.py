# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import operator
from math import lcm
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import ClassVar, Protocol

    class _BinaryOperator(Protocol):
        def __call__(self, a: int, b: int, /) -> int:
            ...

    class _WorryIncrease(Protocol):
        def __call__(self, worriedness: int, /) -> int:
            ...

    _Data = list["_Monkey"]


class Solution(SolutionAbstract):
    day = 11
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 11 data.
        """
        raw_data_iter = iter(raw_data)
        while True:
            # Index
            start_row = next(raw_data_iter).strip()
            index_str = start_row.removeprefix("Monkey").removesuffix(":").strip()
            index = int(index_str)
            # Starting items
            items_row = next(raw_data_iter).strip()
            items_str = items_row.removeprefix("Starting items:").strip()
            items = map(int, items_str.split(","))
            # Worriedness increase operation
            operation_row = next(raw_data_iter).strip()
            operation_str = operation_row.removeprefix("Operation: new = old").strip()
            worry_increase = self._get_worry_increase(*operation_str.split())
            # Division test
            test_row = next(raw_data_iter).strip()
            divisor_str = test_row.removeprefix("Test: divisible by").strip()
            divisor = int(divisor_str)
            # True monkey
            true_row = next(raw_data_iter).strip()
            true_index_str = true_row.removeprefix("If true: throw to monkey").strip()
            true_index = int(true_index_str)
            # False monkey
            false_row = next(raw_data_iter).strip()
            false_index_str = false_row.removeprefix(
                "If false: throw to monkey"
            ).strip()
            false_index = int(false_index_str)
            # Create monkey
            _Monkey(
                index=index,
                items=items,
                worry_increase=worry_increase,
                divisor=divisor,
                true_monkey_index=true_index,
                false_monkey_index=false_index,
            )
            # Spacer
            try:
                next(raw_data_iter)
            except StopIteration:
                break

        return _Monkey.monkeys

    def _get_worry_increase(
        self, operation_str: str, operand_str: str
    ) -> _WorryIncrease:
        """"""
        operation: _BinaryOperator
        match operation_str:
            case "+":
                operation = operator.add
            case "*":
                operation = operator.mul
            case _:
                raise ValueError(f"Unknown operator: {operation_str}")
        match operand_str:
            case "old":
                return lambda x: operation(x, x)
            case n:
                return lambda x: operation(x, int(n))

    def part_1(self) -> int:
        """
        Day 11 part 1 solution.
        """
        for _ in range(20):
            for monkey in self.data:
                monkey.play_part_1()
        inspect_counts = sorted(monkey.inspect_count for monkey in self.data)
        return inspect_counts[-1] * inspect_counts[-2]

    def part_2(self) -> int:
        """
        Day 11 part 2 solution.
        """
        for _ in range(10000):
            for monkey in self.data:
                monkey.play_part_2()
        inspect_counts = sorted(monkey.inspect_count for monkey in self.data)
        return inspect_counts[-1] * inspect_counts[-2]


class _Monkey:
    """"""

    monkeys: ClassVar[list[_Monkey]] = []
    _monkey_divisor_lcm: ClassVar[None | int] = None

    index: int
    items: list[int]
    worry_increase: _WorryIncrease
    divisor: int
    true_monkey_index: int
    false_monkey_index: int

    inspect_count: int

    def __init__(
        self,
        *,
        index: int,
        items: Iterable[int],
        worry_increase: _WorryIncrease,
        divisor: int,
        true_monkey_index: int,
        false_monkey_index: int,
    ) -> None:
        if len(_Monkey.monkeys) != index:
            raise ValueError("Monkeys not created in order")
        _Monkey.monkeys.append(self)
        self.index = index
        self.items = list(items)
        self.worry_increase = worry_increase
        self.divisor = divisor
        self.true_monkey_index = true_monkey_index
        self.false_monkey_index = false_monkey_index
        self.inspect_count = 0

    @property
    def true_monkey(self) -> _Monkey:
        return self.monkeys[self.true_monkey_index]

    @property
    def false_monkey(self) -> _Monkey:
        return self.monkeys[self.false_monkey_index]

    @classmethod
    def get_monkey_divisor_lcm(cls) -> int:
        """"""
        if cls._monkey_divisor_lcm is None:
            cls._monkey_divisor_lcm = lcm(*(monkey.divisor for monkey in cls.monkeys))
        return cls._monkey_divisor_lcm

    def __str__(self) -> str:
        return f"Monkey #{self.index}"

    def __repr__(self) -> str:
        return str(self)

    def play_part_1(self) -> None:
        """"""
        for item in self.items:
            self.inspect_count += 1
            item = self.worry_increase(item) // 3
            if item % self.divisor:
                self.false_monkey.items.append(item)
            else:
                self.true_monkey.items.append(item)
        self.items.clear()

    def play_part_2(self) -> None:
        """"""
        for item in self.items:
            self.inspect_count += 1
            item = self.worry_increase(item) % self.get_monkey_divisor_lcm()
            if item % self.divisor:
                self.false_monkey.items.append(item)
            else:
                self.true_monkey.items.append(item)
        self.items.clear()

    def to_verbose_str(self) -> str:
        """"""
        return (
            f"Monkey {self.index}: inspected {self.inspect_count} times; has "
            f"{self.items}"
        )
