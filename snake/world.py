"""Represent the abstract world of the game."""

import dataclasses
import enum
import itertools
import random
from typing import List, Optional, Final, Sequence, cast, assert_never, Iterable

from icontract import ensure, require, invariant

class ImmutablePosition:
    """
    Represent a tile in the game in the tile space.

    Origin is at the top-left corner.
    """
    _x: int
    _y: int

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def same_coordinates(self, other: 'ImmutablePosition') -> bool:
        """Check for position equivalence w.r.t. coordinates."""
        return self._x == other._x and self._y == other._y


@dataclasses.dataclass
class Position(ImmutablePosition):
    """Represent a mutable position in a game world."""
    def update_coordinates(self, other: 'ImmutablePosition') -> None:
        """Update the coordinates to match the ``other``."""
        self._x = other._x
        self._y = other._y



class Direction(enum.Enum):
    """
    Direction of the snake.
    Starts with East, updates on last input of the user.
    """
    North = "North"
    East = "East"
    South = "South"
    West = "West"

class NonNegativeInt(int):
    @require(lambda value: value >= 0)
    def __new__(cls, value: int) -> "NonNegativeInt":
        return cast(NonNegativeInt, value)



class PositiveInt(int):
    @require(lambda value: value > 0)
    def __new__(cls, value: int) -> "PositiveInt":
        return cast(PositiveInt, value)


def within_cage(pos: Position, width: PositiveInt, height: PositiveInt) -> bool:
    """Check whether the given ``pos`` is within the cage."""
    return (
            1 <= pos.x <= width - 2
            and 1 <= pos.y <= height - 2
    )


def collides(
        pos: Position,
        other: Iterable[Position]
) -> bool:
    """Check whether the ``pos`` collides with ``other`` positions."""
    return any(
        pos.same_coordinates(part)
        for part in other
    )


@invariant(
    lambda self:
    not within_cage(self._head, self.width, self.height),
    "Head within the world"
)
@invariant(
    lambda self:
    all(
        within_cage(part, self.width, self.height)
        for part in self._tail
    ),
    "Tail within the world"
)
@invariant(
    lambda self:
    not (self._apple is not None)
    or (
            within_cage(self._apple, self.width, self.height)
    ),
    "Apple within the world"
)
@invariant(
    lambda self:
    not (self._apple is not None)
    or (
            not collides(
                self.applie,
                itertools.chain(
                    [self._head], self._tail
                )
            )
    ),
    "Apple not inside the snake"
)
class World:
    width: Final[PositiveInt]
    height: Final[PositiveInt]

    _head: Final[Position]
    _tail: Final[List[Position]]

    _direction: Direction

    # TODO(lanNo19): undo optional -- it should always exist
    _apple: Optional[Position]

    @property
    def head(self) -> ImmutablePosition:
        return self._head

    @property
    def tail(self) -> Sequence[ImmutablePosition]:
        return self._tail

    @property
    def apple(self) -> Optional[ImmutablePosition]:
        return self._apple

    def __init__(self) -> None:
        self.width = PositiveInt(32)
        self.height = PositiveInt(32)
        self._head = Position(15, 15)
        self._tail: List[Position] = []
        self._direction = Direction.East

    def score(self) -> NonNegativeInt:
        """Compute the score based on the snake length."""
        return NonNegativeInt(len(self._tail) * 10)

    def update_world(self) -> bool:
        """
        Try to update the world.

        :return: True if the world is in a consistent state; otherwise False -- meaning that
        the game should terminate as no further world updates are possible.
        """
        next_head: Position
        match self._direction:
            case Direction.North:
                next_head = Position(x=self._head.x, y=self._head.y - 1)
            case Direction.South:
                next_head = Position(x=self._head.x, y=self._head.y + 1)
            case Direction.East:
                next_head = Position(x=self._head.x + 1, y=self._head.y)
            case Direction.West:
                next_head = Position(x=self._head.x - 1, y=self._head.y)
            case _:
                assert_never(self._direction)

        if (
                not within_cage(next_head, self.width, self.height)
                or collides(next_head, self._tail)
        ):
            return False

        # region Update snake

        # No update to the apple in this block expected.
        old_apple_position = dataclasses.replace(self._apple)

        if next_head.same_coordinates(self._apple):
            self._tail.append(dataclasses.replace(self._head))
        else:
            if len(self._tail) != 0:
                self._tail[:-1] = self._tail[1:]
                self._tail[-1] = dataclasses.replace(self._head)

        self._head.update_coordinates(next_head)

        assert old_apple_position.same_coordinates(self._apple), (
            "Updating the tail and the head should not change the apple just yet."
        )
        # endregion

        # Update apple
        if self._apple.same_coordinates(self._head):
            next_apple = dataclasses.replace(self._apple)

            while collides(
                next_apple,
                itertools.chain([self._head], self._tail)
            ):
                next_apple = Position(
                    x=random.randint(1, self.width - 2),
                    y=random.randint(1, self.height - 2)
                )
                assert within_cage(next_apple, self.width, self.height)

            self._apple.update_coordinates(next_apple)

        return True

    def update_direction(self, new_direction: Direction) -> None:
        self._direction = new_direction

    # TODO(lanNo19): Go away!
    @ensure(lambda self, new_direction:
            new_direction != {
                Direction.Up: Direction.Down,
                Direction.Down: Direction.Up,
                Direction.Left: Direction.Right,
                Direction.Right: Direction.Left
            }.get(self._direction, None),
            "The new direction must not be the opposite of the current direction.")
    def listen_to_keys(self, new_direction):
        """
        Updates snake direction while preventing reverse movement.
        """
        opposite = {
            Direction.Up: Direction.Down,
            Direction.Down: Direction.Up,
            Direction.Left: Direction.Right,
            Direction.Right: Direction.Left
        }

        if new_direction != opposite.get(self._direction, None):
            self._direction = new_direction
