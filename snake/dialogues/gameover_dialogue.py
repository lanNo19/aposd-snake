from turtle import Turtle

from snake.clock import Clock
from snake.idialogue import IDialogue


class GameOverDialogue(IDialogue):

    def __init__(self, clock: Clock, turtle: Turtle):
        super().__init__(clock, turtle)

    def mount(self, switch_dialogue_callback):
        pass

    def unmount(self):
        pass

    def refresh(self):
        # keyboard input checking
        # turtle drawing
        pass