# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from .solution import Map, Solution

_CURR_DIR = Path(__file__).resolve().parent
_SIZE_FACTOR = 5


def _visualize_p1() -> None:
    """"""
    solution = Solution()
    solution.part_1()
    _visualize(solution.data, "part_1")


def _visualize_p2() -> None:
    """"""
    solution = Solution()
    solution.part_2()
    _visualize(solution.data, "part_2")


def _visualize(map_: Map, file_stem: str) -> None:
    data = map_.map_

    start_col = 0
    for c, col in enumerate(zip(*data)):
        if map_.has_floor:
            col = col[:-1]
        if not all(cell == Map.Block.AIR for cell in col):
            start_col = max(0, c - 1)
            break

    end_col = len(data[0]) - 1
    for c, col in enumerate(reversed(list(zip(*data)))):
        if map_.has_floor:
            col = col[:-1]
        if not all(cell == Map.Block.AIR for cell in col):
            end_col = len(data[0]) - 1 - max(0, c - 1)
            break

    width = (end_col - start_col + 1) * _SIZE_FACTOR
    height = len(data) * _SIZE_FACTOR
    img = Image.new(mode="RGB", size=(width, height))

    for r, row in enumerate(data):
        for c, cell in enumerate(row[start_col : end_col + 1]):
            match cell:
                case Map.Block.AIR:
                    color = (0, 0, 0)
                case Map.Block.ROCK:
                    color = (90, 77, 65)
                case Map.Block.SAND:
                    color = (194, 178, 128)
                case _:
                    raise ValueError(f"Unknown block {cell}")
            for x in range(_SIZE_FACTOR * c, _SIZE_FACTOR * (c + 1)):
                for y in range(_SIZE_FACTOR * r, _SIZE_FACTOR * (r + 1)):
                    img.putpixel((x, y), color)

    out_path = _CURR_DIR / f"{file_stem}.png"
    img.save(out_path)
