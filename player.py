from collections import deque
from random import choice

from character_utils import character_by_name
from dummy import DummyAgent, Dummy
from pair import Pair
from user import UserAgent
from utils import (choose_random_valid_behavior, get_possible_behaviors,
                   get_available_indices, stacks)


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
        self.selection = None
        self.soak = 0
        self.stunned = False
        self.stun_guard = 0
        self.stun_immune = False
        self.can_hit = True
        self.dodge = False
        self.active = False

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

    def __str__(self):
        return self.name + '(' + str(self.life) + ')'

    def refresh(self):
        self.soak = 0
        self.stunned = False
        self.stun_guard = 0
        self.stun_immune = False
        self.can_hit = True
        self.dodge = False

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
        self.selection = None

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
        return get_available_indices(
            self.character.styles, self.discarded_styles, self.played_styles
        )

    @property
    def available_bases(self):
        return get_available_indices(
            self.character.bases, self.discarded_bases, self.played_bases
        )

    # def has_playable_styles(self): # is this needed?
    #   return len(get_available_indices(
    #       self.character.styles, self.discarded_styles, self.played_styles
    #   )) > 0

    def has_playable_bases(self):
        return len(get_available_indices(
            self.character.bases, self.discarded_bases, self.played_bases
        )) > 0

    def apply_selection_modifiers(self):
        selection = self.selection
        for mod in selection.modifiers:
            if hasattr(self, mod):
                if stacks(mod):
                    curr = getattr(self, mod)
                    setattr(self, mod, curr + selection.modifiers[mod])
                else:
                    setattr(self, mod, selection.modifiers[mod])

    def get_start_of_beat(self, state):
        possible = get_possible_behaviors(self.selection, 'startOfBeat')
        return choose_random_valid_behavior(possible, state)

    def get_before_activating(self, state):
        possible = get_possible_behaviors(self.selection, 'beforeActivating')
        return choose_random_valid_behavior(possible, state)

    def get_on_hit(self, state):
        possible = get_possible_behaviors(self.selection, 'onHit')
        return choose_random_valid_behavior(possible, state)

    def get_on_damage(self, state):
        possible = get_possible_behaviors(self.selection, 'onDamage')
        return choose_random_valid_behavior(possible, state)

    def get_after_activating(self, state):
        possible = get_possible_behaviors(self.selection, 'afterActivating')
        return choose_random_valid_behavior(possible, state)

    def get_end_of_beat(self, state):
        possible = get_possible_behaviors(self.selection, 'endOfBeat')
        return choose_random_valid_behavior(possible, state)

    def handle_damage(self, damage, attacker):
        if damage > 0:
            damage = self.soak_damage(damage)
            if damage > self.stun_guard and not self.stun_immune:
                self.stunned = True
            self.life -= damage
        return damage

    # Returns leftover un-soaked damage
    def soak_damage(self, damage):
        damage = damage - self.soak
        if damage > 0:
            return damage
        else:
            return 0
