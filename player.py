from collections import deque
from random import choice, shuffle

from character_utils import character_by_name
from dummy import DummyAgent, Dummy
from pair import Pair
from user import UserAgent
from utils import get_available_indices


class Player:
    def __init__(self, name, is_ai):
        self.name = name
        self.is_ai = is_ai
        self.life = 20
        self.position = None
        self.discarded_styles = deque()
        self.discarded_bases = deque()
        # self.discarded_other = deque()
        self.played_styles = []
        self.played_bases = []

        if name == 'Training Dummy':
            self.character = Dummy()
            self.agent = DummyAgent()
            self.life = float('inf')
        else:
            self.character = character_by_name(name)
            if self.character is None:
                self.character = character_by_name('Simple Bob')

            if self.is_ai:
                self.agent = DummyAgent()
            else:
                self.agent = UserAgent()

    def get_ante(self, info):
        return None

    @property
    def status(self):
        return {
            'life': self.life,
            'position': self.position
        }

    def discard_style(self, index):
        self.discarded_styles.append(index)

    def discard_base(self, index):
        self.discarded_bases.append(index)

    def init_discards(self, state):
        self.discard_style(0)
        self.discard_base(0)
        self.discard_style(1)
        self.discard_base(1)

    def recover_discards(self):
        self.discarded_styles.popleft()
        self.discarded_bases.popleft()

    def recycle(self):
        self.recover_discards()
        self.discard_style(self.played_styles.pop())
        self.discard_base(self.played_bases.pop())
        self.played_styles = []
        self.played_bases = []

    def get_selection(self, state):
        stylei = choice(self.available_styles)
        basei = choice(self.available_bases)
        self.played_styles.append(stylei)
        self.played_bases.append(basei)
        return Pair(self.character.styles[stylei], self.character.bases[basei])

    def get_new_base(self, state):
        basei = choice(self.available_bases)
        self.played_bases.append(basei)
        return self.character.bases[basei]

    @property
    def available_styles(self):
        return get_available_indices(self.character.styles, self.discarded_styles, self.played_styles)

    @property
    def available_bases(self):
        return get_available_indices(self.character.bases, self.discarded_bases, self.played_bases)

    # def has_playable_styles(self): # is this needed?
    #    return len(get_available_indices(self.character.styles, self.discarded_styles, self.played_styles)) > 0

    def has_playable_bases(self):
        return len(get_available_indices(self.character.bases, self.discarded_bases, self.played_bases)) > 0

    def get_possible_start_of_beat(self, selection):
        possible = []
        effects = selection.get_effects('startOfBeat')
        for effect in effects:
            for action in effect.actions:
                possible.append(action.behaviors)
        return possible

    def get_start_of_beat(self, possible_behaviors, state):
        chosen = []
        indices = [x for x in range(0, len(possible_behaviors))]
        for i in indices:
            chosen.append(choice(possible_behaviors[i]))
        return chosen

    @property
    def stunned(self):
        return False
