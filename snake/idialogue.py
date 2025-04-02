from abc import ABC, abstractmethod
from turtle import Turtle

from snake.clock import Clock


class IDialogue(ABC, Clock, Turtle):
    @abstractmethod
    def mount(self):
        pass

    @abstractmethod
    def unmount(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    def __init__(self, clock: Clock, turtle: Turtle):
        super().__init__()
        self.turtle = turtle
        self.clock = clock
        self.mount()