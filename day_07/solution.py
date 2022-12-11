# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import TypeAlias

    _Data: TypeAlias = "_Directory"


class Solution(SolutionAbstract):
    day = 7
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 07 data.
        """
        root = _Directory(name="/")
        root.parent = root
        curr_dir: _Directory = root

        for line in raw_data:
            match line.split():
                case ["$", "cd", path]:
                    match path:
                        case root.name:
                            curr_dir = root
                        case "..":
                            parent = curr_dir.parent
                            if parent is None:
                                raise ValueError("No parent found")
                            curr_dir = parent
                        case _:
                            curr_dir = curr_dir.children_map[path]
                case ["$", "ls"]:
                    pass
                case ["dir", name]:
                    curr_dir.add_children(_Directory(name=name))
                case [size, name]:
                    curr_dir.add_children(_File(name=name, size=int(size)))
                case _:
                    raise ValueError(f"Unknown line: {line}")

        return root

    def part_1(self) -> int:
        """
        Day 07 part 1 solution.
        """
        return sum(
            node.size
            for node in self.data.traverse()
            if isinstance(node, _Directory) and node.size <= 100000
        )

    def part_2(self) -> int:
        """
        Day 07 part 2 solution.
        """
        target = self.data.size - 40000000
        curr_dir: _Directory = self.data
        for child in self.data.traverse():
            if not isinstance(child, _Directory):
                continue
            if child.size < target:
                continue
            if child.size < curr_dir.size:
                curr_dir = child

        return curr_dir.size

    def repr(self) -> str:
        return str(self.data)


class _Node:
    name: str
    parent: None | _Directory
    size: int | property[int]

    def __init__(self, *, name: str) -> None:
        self.name = name
        self.parent = None


class _Directory(_Node):
    children_map: dict[str, _Node]
    _size: None | int = None

    def __init__(self, *, name: str) -> None:
        super().__init__(name=name)
        self.children_map = {}

    def __str__(self) -> str:
        self_str = f"- {self.name} (dir)"
        children_strs = [str(child) for child in self.children_map.values()]
        children_str = "\n".join(children_strs)
        padded_children_str = "\n".join(
            f"  {child_str}" for child_str in children_str.split("\n")
        )
        return f"{self_str}\n{padded_children_str}"

    @property
    def size(self) -> int:
        if self._size is None:
            self._size = sum(child.size for child in self.children_map.values())
        return self._size

    def add_children(self, *nodes: _Node) -> None:
        for node in nodes:
            name = node.name
            if name in self.children_map:
                raise ValueError(f"Existing file: {name}")
            self.children_map[name] = node
            node.parent = self
        self.children_map |= {node.name: node for node in nodes}

    def traverse(self) -> Generator[_Node, None, None]:
        """"""
        yield self
        for child in self.children_map.values():
            if isinstance(child, _Directory):
                yield from child.traverse()
            else:
                yield child


class _File(_Node):
    def __init__(self, *, name: str, size: int) -> None:
        super().__init__(name=name)
        self.size = size

    def __str__(self) -> str:
        return f"- {self.name} (file, size={self.size})"
