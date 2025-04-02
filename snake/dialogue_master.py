import time

from snake.dialogues.game_dialogue import GameDialogue
from snake.dialogues.gameover_dialogue import GameOverDialogue
from snake.dialogues.welcome_dialogue import WelcomeDialogue
from snake.idialogue import IDialogue
from snake.world import World


class DialogueMaster:
    dialogue: IDialogue
    world: World

    def put_dialogue(self, d: IDialogue, switch_dialogue_callback):
        if self.dialogue is not None:
            self.dialogue.unmount()
        if d is not None:
            d.mount(switch_dialogue_callback)
            self.dialogue = d

    def endless_loop(self):
        while self.dialogue is not None:
            start = self.dialogue.clock.now()
            self.dialogue.refresh()
            end = self.dialogue.clock.now()
            delta = end - start
            sleep_time = 1000/25 - delta
            time.sleep(sleep_time)

    def welcome_to_game_callback(self):
        game_dialogue = GameDialogue(self.world, self.dialogue.clock, self.dialogue.turtle)
        self.put_dialogue(d=game_dialogue, switch_dialogue_callback=self.game_to_gameover_callback())

    def game_to_gameover_callback(self):
        gameover_dialogue = GameOverDialogue(self.dialogue.clock, self.dialogue.turtle)
        self.put_dialogue(d=gameover_dialogue, switch_dialogue_callback=self.ending_callback())

    def ending_callback(self):
        exit()