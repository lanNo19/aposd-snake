import sys
from turtle import Turtle

from snake.clock import Clock
from snake.dialogue_master import DialogueMaster
from snake.world import World
from snake.dialogues.welcome_dialogue import WelcomeDialogue


def main() -> int:
    world = World()
    clock = Clock()
    turtle = Turtle()
    welcome_dialogue = WelcomeDialogue(clock, turtle)
    dialogue_master = DialogueMaster()
    dialogue_master.put_dialogue(d=welcome_dialogue, switch_dialogue_callback=dialogue_master.welcome_to_game_callback)
    while True:
        dialogue_master.endless_loop()
    return 0

if __name__ == "__main__":
    sys.exit(main())