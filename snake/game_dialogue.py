from turtle import Turtle

from snake.clock import Clock
from snake.idialogue import IDialogue
from snake.world import World, Direction


class GameDialogue(IDialogue):
    world: World

    def __init__(self, world, clock: Clock, turtle: Turtle):
        super().__init__(clock, turtle)
        self.world = world

    def mount(self):
        self.key_handler()

    def unmount(self):
        self.turtle_obj.screen.onkeypress(None, "Up")
        self.turtle_obj.screen.onkeypress(None, "Down")
        self.turtle_obj.screen.onkeypress(None, "Left")
        self.turtle_obj.screen.onkeypress(None, "Right")

    def refresh(self):

    def key_handler(self):
        self.turtle.screen.listen()
        self.turtle.screen.onkeypress(lambda: self.world.listen_to_keys(Direction.North), "Up")
        self.turtle.screen.onkeypress(lambda: self.world.listen_to_keys(Direction.South), "Down")
        self.turtle.screen.onkeypress(lambda: self.world.listen_to_keys(Direction.East), "Right")
        self.turtle.screen.onkeypress(lambda: self.world.listen_to_keys(Direction.West), "Left")

