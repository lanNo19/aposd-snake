"""Represent the abstract world of the game."""

import dataclasses
import enum
from typing import List, Optional, Final, Sequence, cast

from icontract import ensure, require


@dataclasses.dataclass
class Position:
    """
    Represent a tile in the game in the tile space.

    Origin is at the top-left corner.
    """
    x: int
    y: int

class Direction(enum.Enum):
    """
    Direction of the snake.
    Starts with East, updates on last input of the user.
    """
    North = "North"
    East = "East"
    South = "South"
    West = "West"


class PositiveInt(int):
    @require(lambda value: value > 0)
    def __new__(cls, value: int) -> "PositiveInt":
        return cast(PositiveInt, value)

class World:
    width: Final[PositiveInt]
    height: Final[PositiveInt]

    head: Position
    tail: List[Position]
    direction: Direction

    apple: Optional[Position]
    score: int

    @ensure(lambda tail: not tail)
    @ensure(lambda head: head.x is 15 and head.y is 15)
    @ensure(lambda score: score is 0)
    @ensure(lambda direction: direction is Direction.East)
    def __init__(self) -> None:
        self.width = PositiveInt(32)
        self.height = PositiveInt(32)
        self.head = Position(15, 15)
        self.tail: List[Position] = []
        self.score = 0
        self.direction = Direction.East

