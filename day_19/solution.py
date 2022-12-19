# pyright: reportMissingTypeStubs=false
""""""

from __future__ import annotations

import re
from dataclasses import dataclass
from math import ceil
from typing import TYPE_CHECKING

from utils import SolutionAbstract

if TYPE_CHECKING:
    _Data = list["_Blueprint"]

_BLUEPRINT_RE = re.compile(
    r"^Blueprint (\d+):"
    r" Each ore robot costs (\d+) ore\."
    r" Each clay robot costs (\d+) ore\."
    r" Each obsidian robot costs (\d+) ore and (\d+) clay\."
    r" Each geode robot costs (\d+) ore and (\d+) obsidian\.$"
)


class Solution(SolutionAbstract):
    day = 19
    data: _Data

    def _process_data(self, raw_data: list[str]) -> _Data:
        """
        Process day 19 data.
        """
        blueprints: list[_Blueprint] = []
        for line in raw_data:
            m = _BLUEPRINT_RE.fullmatch(line)
            if m is None:
                raise ValueError(f'Invalid line: "{line}"')
            ore_robot = _Robot(ore_cost=int(m[2]), clay_cost=0, obby_cost=0)
            clay_robot = _Robot(ore_cost=int(m[3]), clay_cost=0, obby_cost=0)
            obby_robot = _Robot(ore_cost=int(m[4]), clay_cost=int(m[5]), obby_cost=0)
            geode_robot = _Robot(ore_cost=int(m[6]), clay_cost=0, obby_cost=int(m[7]))
            blueprints.append(
                _Blueprint(
                    index=int(m[1]),
                    ore_robot=ore_robot,
                    clay_robot=clay_robot,
                    obby_robot=obby_robot,
                    geode_robot=geode_robot,
                )
            )
        return blueprints

    def part_1(self) -> int:
        """
        Day 19 part 1 solution.
        """
        sum_ = 0
        l = len(self.data)
        ll = len(str(l))
        for i, b in enumerate(self.data, start=1):
            print(f"\r\x1b[KRunning blueprint #{i:>{ll}}/{l}...", end="\r")
            runner = _BlueprintRunner(b)
            sum_ += b.index * runner.run()
        print()
        return sum_

    def part_2(self) -> ...:
        """
        Day 19 part 2 solution.
        """


class _BlueprintRunner:
    """"""

    blueprint: _Blueprint

    def __init__(self, blueprint: _Blueprint) -> None:
        self.blueprint = blueprint

    def run(self) -> int:
        """"""
        resource_count = self._run(
            time=26, robots=_RobotCount(), resources=_ResourceCount()
        )
        return resource_count.geode

    def _run(
        self, *, time: int, robots: _RobotCount, resources: _ResourceCount
    ) -> _ResourceCount:
        """"""
        if time < 0:
            raise ValueError(f"Negative time: {time=} {robots=} {resources=}")
        if time == 0:
            return resources
        # Cannot create more robots
        if time == 1:
            return resources.pass_time(robots=robots, time=1)
        # Assuming no concurrent robot creation
        # Do nothing
        resource_possibilities = [
            resources.pass_time(robots=robots, time=time),
        ]
        # Create robots. Assuming no concurrent robot creation
        # At least 2 mins have to be left (1 for creation, 1 for actual use)
        curr_max_resouces = resources.pass_time(robots=robots, time=time - 2)
        curr_max_ore = curr_max_resouces.ore
        curr_max_clay = curr_max_resouces.clay
        curr_max_obby = curr_max_resouces.obby
        # Create ore robot
        ore_robot_ore_cost = self.blueprint.ore_robot.ore_cost
        if curr_max_ore >= ore_robot_ore_cost:
            time_needed = (
                ceil(max(0, ore_robot_ore_cost - resources.ore) / robots.ore) + 1
            )
            new_resources = self._run(
                time=time - time_needed,
                robots=robots.diff_copy(ore=1),
                resources=resources.pass_time(
                    robots=robots, time=time_needed
                ).diff_copy(ore=-ore_robot_ore_cost),
            )
            if new_resources.geode:
                resource_possibilities.append(new_resources)
        # Create clay robot
        clay_robot_ore_cost = self.blueprint.clay_robot.ore_cost
        if curr_max_ore >= clay_robot_ore_cost:
            time_needed = (
                ceil(max(0, clay_robot_ore_cost - resources.ore) / robots.ore) + 1
            )
            new_resources = self._run(
                time=time - time_needed,
                robots=robots.diff_copy(clay=1),
                resources=resources.pass_time(
                    robots=robots, time=time_needed
                ).diff_copy(ore=-clay_robot_ore_cost),
            )
            if new_resources.geode:
                resource_possibilities.append(new_resources)
        # Create obby robot
        obby_robot_ore_cost = self.blueprint.obby_robot.ore_cost
        obby_robot_clay_cost = self.blueprint.obby_robot.clay_cost
        if (
            robots.clay
            and curr_max_ore >= obby_robot_ore_cost
            and curr_max_clay >= obby_robot_clay_cost
        ):
            time_needed = (
                max(
                    ceil(max(0, obby_robot_ore_cost - resources.ore) / robots.ore),
                    ceil(max(0, obby_robot_clay_cost - resources.clay) / robots.clay),
                )
                + 1
            )
            new_resources = self._run(
                time=time - time_needed,
                robots=robots.diff_copy(obby=1),
                resources=resources.pass_time(
                    robots=robots, time=time_needed
                ).diff_copy(ore=-obby_robot_ore_cost, clay=-obby_robot_clay_cost),
            )
            if new_resources.geode:
                resource_possibilities.append(new_resources)
        # Create geode robot
        geode_robot_ore_cost = self.blueprint.geode_robot.ore_cost
        geode_robot_obby_cost = self.blueprint.geode_robot.obby_cost
        if (
            robots.obby
            and curr_max_ore >= geode_robot_ore_cost
            and curr_max_obby >= geode_robot_obby_cost
        ):
            time_needed = (
                max(
                    ceil(max(0, geode_robot_ore_cost - resources.ore) / robots.ore),
                    ceil(max(0, geode_robot_obby_cost - resources.obby) / robots.obby),
                )
                + 1
            )
            new_resources = self._run(
                time=time - time_needed,
                robots=robots.diff_copy(geode=1),
                resources=resources.pass_time(
                    robots=robots, time=time_needed
                ).diff_copy(ore=-geode_robot_ore_cost, obby=-geode_robot_obby_cost),
            )
            if new_resources.geode:
                resource_possibilities.append(new_resources)
        # Return max geode
        # print(f"  {time=} {robots=} {resources=} {resource_possibilities=}")
        return max(resource_possibilities, key=lambda r: r.geode)


@dataclass(frozen=True, kw_only=True)
class _Robot:
    ore_cost: int
    clay_cost: int
    obby_cost: int


@dataclass(frozen=True, kw_only=True)
class _Blueprint:
    index: int
    ore_robot: _Robot
    clay_robot: _Robot
    obby_robot: _Robot
    geode_robot: _Robot


@dataclass(frozen=True, kw_only=True)
class _RobotCount:
    ore: int = 1
    clay: int = 0
    obby: int = 0
    geode: int = 0

    def diff_copy(
        self, *, ore: int = 0, clay: int = 0, obby: int = 0, geode: int = 0
    ) -> _RobotCount:
        """"""
        return _RobotCount(
            ore=self.ore + ore,
            clay=self.clay + clay,
            obby=self.obby + obby,
            geode=self.geode + geode,
        )


@dataclass(frozen=True, kw_only=True)
class _ResourceCount:
    ore: int = 0
    clay: int = 0
    obby: int = 0
    geode: int = 0

    def diff_copy(
        self, *, ore: int = 0, clay: int = 0, obby: int = 0, geode: int = 0
    ) -> _ResourceCount:
        """"""
        return _ResourceCount(
            ore=self.ore + ore,
            clay=self.clay + clay,
            obby=self.obby + obby,
            geode=self.geode + geode,
        )

    def pass_time(self, *, robots: _RobotCount, time: int) -> _ResourceCount:
        """"""
        return self.diff_copy(
            ore=robots.ore * time,
            clay=robots.clay * time,
            obby=robots.obby * time,
            geode=robots.geode * time,
        )
