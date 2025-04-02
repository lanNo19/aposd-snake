from turtle import Turtle

from snake.clock import Clock
from snake.idialogue import IDialogue
from snake.world import World


class GameDialogue(IDialogue):
    world: World

    def __init__(self, world, clock: Clock, turtle: Turtle):
        super().__init__(clock, turtle)
        self.world = world

    def mount(self):

    def unmount(self):

    def refresh(self):
