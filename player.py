from collections import deque
from random import choice, randint

from character_utils import character_by_name
from dummy import DummyAgent, Dummy
from selection import Pair
from user import UserAgentCLI
from utils import (choose_random_valid_behavior, get_possible,
                   get_available_indices, stacks)


class Player:
    def __init__(self, name, is_ai):
        self.name = name
        self.is_ai = is_ai
        self.life = 20
        self.position = None
        self.finisher = None
        self.ante_finisher = False
        self.discarded_styles = deque()
        self.discarded_bases = deque()
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
                self.agent = UserAgentCLI()

    def __str__(self):
        return self.name + '(' + str(self.life) + ')'

    def refresh(self):
        self.soak = 0
        self.stunned = False
        self.stun_guard = 0
        self.stun_immune = False
        self.can_hit = True
        self.dodge = False

    def get_ante(self, state):
        if self.finisher is not None and self.life <= 7:
            if hasattr(self.agent, 'get_ante'):
                if self.agent.get_ante(state) == 'Finisher':
                    self.ante_finisher = True
                    return self.finisher
            else:
                if randint(0, 2) == 2:
                    self.ante_finisher = True
                    return self.finisher
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

    def select_finisher(self, state):
        if hasattr(self.character, 'finishers'):
            options = self.character.finishers
            if hasattr(self.agent, 'select_finisher'):
                self.finisher = self.agent.select_finisher(options, state)
            else:
                self.finisher = choice(options)

    def init_discards(self, state):
        if hasattr(self.agent, 'init_discards'):
            styles = self.character.styles
            bases = self.character.bases
            to_discard = self.agent.init_discards(styles, bases, state)
            self.discard_style(to_discard[0])
            self.discard_style(to_discard[1])
            self.discard_base(to_discard[2])
            self.discard_base(to_discard[3])
        else:
            self.discard_style(0)
            self.discard_base(0)
            self.discard_style(1)
            self.discard_base(1)

    def recover_discards(self):
        self.discarded_styles.popleft()
        self.discarded_bases.popleft()

    def recycle(self):
        if self.ante_finisher:
            self.ante_finisher = False
            self.finisher = None
        else:
            self.recover_discards()
            self.discard_style(self.played_styles.pop())
            self.discard_base(self.played_bases.pop())
        self.played_styles = []
        self.played_bases = []
        self.selection = None

    def get_selection(self, state):
        av_s = self.available_styles
        av_b = self.available_bases
        if hasattr(self.agent, 'get_selection'):
            stylei, basei = self.agent.get_selection(av_s, av_b, state)
        else:
            stylei = choice(av_s)
            basei = choice(av_b)
        self.played_styles.append(stylei)
        self.played_bases.append(basei)
        return Pair(self.character.styles[stylei], self.character.bases[basei])

    def get_new_base(self, state):
        av_b = self.available_bases
        if hasattr(self.agent, 'get_new_base'):
            basei = self.agent.get_new_base(av_b, state)
        else:
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

    def apply_reveal_effects(self):
        # need to implement this
        # will probably need game state
        return

    def apply_modifier(self, mod, val):
        if hasattr(self, mod):
            if stacks(mod):
                curr = getattr(self, mod)
                setattr(self, mod, curr + val)
            else:
                setattr(self, mod, val)

    def apply_selection_modifiers(self):
        selection = self.selection
        for mod in selection.modifiers:
            self.apply_modifier(mod, selection.modifiers[mod])

    def get_actions(self, trigger):
        return get_possible(self.selection, trigger)

    def get_behavior(self, actions, state, trigger):
        if hasattr(self.agent, 'get_behavior'):
            chosen, b = self.agent.get_behavior(actions, state, trigger)
        else:
            chosen, b = choose_random_valid_behavior(actions, state)
        return chosen, b

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
