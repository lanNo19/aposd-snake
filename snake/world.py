"""Represent the abstract world of the game."""

import dataclasses
import enum
import random
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

    def check_fence(self) -> bool:
        if self.x == 0 or self.y == 0 or self.x == 31 or self.y == 31:
            return True
        return False

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
    @ensure(lambda head: head.x == 15 and head.y == 15)
    @ensure(lambda score: score == 0)
    @ensure(lambda direction: direction == Direction.East)
    def __init__(self, game_over_callback) -> None:
        self.width = PositiveInt(32)
        self.height = PositiveInt(32)
        self.head = Position(15, 15)
        self.tail: List[Position] = []
        self.score = 0
        self.direction = Direction.East
        self.game_over_callback = game_over_callback

    def update_world(self) -> World:
        next_x: int
        next_y: int
        match self.direction:
            case Direction.North:
                next_x = self.head.x
                next_y = self.head.y - 1
            case Direction.South:
                next_x = self.head.x
                next_y = self.head.y + 1
            case Direction.East:
                next_x = self.head.x + 1
                next_y = self.head.y
            case Direction.West:
                next_x = self.head.x - 1
                next_y = self.head.y

        next_head_position = Position(next_x, next_y)
        if next_head_position.check_fence() or next_head_position in self.tail:
            self.game_over()
            return self

        if (next_head_position == self.apple):
            self.tail.append(self.head)
            self.head = next_head_position
            self.score += 10
        else:
            if self.tail:
                self.tail[:-1] = self.tail[1:]
                self.tail[-1] = next_head_position

        # for apple
        while self.apple == self.head or self.apple.check_fence() or self.apple in self.tail:
            next_x = random.randint(1, 30)
            next_y = random.randint(1, 30)
            self.apple = Position(next_x, next_y)

        return self

    def listen_to_keys(self, new_direction):
        """Updates snake direction while preventing reverse movement."""
        opposite = {
            Direction.Up: Direction.Down,
            Direction.Down: Direction.Up,
            Direction.Left: Direction.Right,
            Direction.Right: Direction.Left
        }

        if new_direction != opposite.get(self.direction, None):
            self.direction = new_direction

    def game_over(self):
        if self.game_over_callback:
            self.game_over_callback(self)