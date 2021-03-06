from collections import deque
from functools import reduce
from random import choice, randint

from character_utils import character_by_name
from discards import Discards
from dummy import DummyAgent, Dummy
from selection import Pair
try:
    from user import UserAgentCLI
except:
    print('skipping UserAgentCLI import')
from utils import (choose_random_valid_behavior, get_possible)


class Player:
    def __init__(self, name, is_ai):
        self.name = name
        self.is_ai = is_ai
        self.life = 20
        self.position = None
        self.finisher = None
        self.ante_finisher = False
        self.discards = Discards(2)
        self.played_styles = []
        self.played_bases = []
        self.selection = None
        self.active = False
        self.modifiers = []
        self.refresh()

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

    @property
    def status(self):
        return {
            'life': self.life,
            'position': self.position
        }

    @property
    def soak(self):
        return self.get_mod_val('soak')

    @property
    def stun_guard(self):
        return self.get_mod_val('stun_guard')

    @property
    def stun_immune(self):
        return self.get_mod_val('stun_immune', False)

    @property
    def can_hit(self):
        return self.get_mod_val('can_hit', True)

    @property
    def dodge(self):
        return self.get_mod_val('dodge', False)

    @property
    def power(self):
        return self.get_mod_val('power')

    @property
    def priority(self):
        return self.get_mod_val('priority')

    @property
    def atk_range(self):
        if self.selection.atk_range is not None:
            def range_val(range_mod): return range_mod.val
            range_mods = self.get_relevant_mods('range')
            range_mods = list(map(range_val, range_mods))
            range_mods.append(self.selection.atk_range)
            combos = [[]]
            for m in range_mods:
                t = []
                for y in m:
                    for i in combos:
                        t.append(i+[y])
                combos = t
            return sorted(set([sum(c) for c in combos]))
        else:
            return None

    def get_mod_val(self, mtype, default=0):
        relevant = self.get_relevant_mods(mtype)
        if len(relevant) == 0:
            return default

        if isinstance(default, bool):
            for m in relevant:
                if m.val != default:
                    return m.val
            return default
        elif isinstance(default, (int, float)):
            return reduce((lambda acc, m: acc+m.val), relevant, default)
        else:
            print('Unexpected Mod mtype/def: {} {}'.format(mtype, default))
            return None

    def get_relevant_mods(self, mtype):
        def f(m): return m.mtype == mtype
        return list(filter(f, self.modifiers))

    def refresh(self):
        self.stunned = False
        self.actions = []
        self.update_modifiers()

    def update_modifiers(self):
        for i in range(len(self.modifiers)):
            if self.modifiers[i].onset == 0:
                self.modifiers[i].duration -= 1
            else:
                self.modifiers[i].onset -= 1

        def f(m): return m.duration > 0
        self.modifiers = list(filter(f, self.modifiers))

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

    def get_ante_effects(self):
        if hasattr(self.character, 'get_ante_effects'):
            return self.character.get_ante_effects()
        else:
            return None

    def discard(self, to_discard):
        self.discard_inner(to_discard)

    def discard_inner(self, to_discard):
        self.discards.discard_inner(to_discard)

    def discard_outer(self, to_discard):
        self.discards.discard_outer(to_discard)

    def select_finisher(self, state):
        if hasattr(self.character, 'finishers'):
            options = self.character.finishers
            if hasattr(self.agent, 'select_finisher'):
                self.finisher = self.agent.select_finisher(options, state)
            else:
                self.finisher = choice(options)

    def init_discards(self, state):
        styles = self.character.styles
        bases = self.character.bases
        if hasattr(self.agent, 'init_discards'):
            to_discard = self.agent.init_discards(styles, bases, state)
            self.discard_outer([
                styles[to_discard[0]],
                bases[to_discard[2]]
            ])
            self.discard([
                styles[to_discard[1]],
                bases[to_discard[3]]
            ])
        else:
            self.discard_outer([
                styles[0],
                bases[0]
            ])
            self.discard([
                styles[1],
                bases[1]
            ])

    def recover_discards(self):
        self.discards.cycle_out()

    def recycle(self):
        if self.ante_finisher:
            self.ante_finisher = False
            self.finisher = None
        else:
            self.recover_discards()
            self.discard(self.played_styles.pop())
            self.discard(self.played_bases.pop())
        self.played_styles = []
        self.played_bases = []
        self.selection = None

    def get_selection(self, state):
        av_s = self.available_styles
        av_b = self.available_bases
        if hasattr(self.agent, 'get_selection'):
            style, base = self.agent.get_selection(av_s, av_b, state)
        else:
            style = choice(av_s)
            base = choice(av_b)
        self.played_styles.append(style)
        self.played_bases.append(base)
        return Pair(style, base)

    def get_new_base(self, state):
        av_b = self.available_bases
        if hasattr(self.agent, 'get_new_base'):
            base = self.agent.get_new_base(av_b, state)
        else:
            base = choice(self.available_bases)
        self.played_bases.append(base)
        return base

    @property
    def available_styles(self):
        opts = self.character.styles
        discarded = self.discards.styles
        played = self.played_styles
        return [s for s in opts if s not in discarded and s not in played]

    @property
    def available_bases(self):
        opts = self.character.bases
        discarded = self.discards.bases
        played = self.played_bases
        return [b for b in opts if b not in discarded and b not in played]

    def has_playable_styles(self):
        return len(self.available_styles) > 0

    def has_playable_bases(self):
        return len(self.available_bases) > 0

    def handle_modifier(self, mod):
        if mod.mtype == 'stun' and not self.stun_immune:
            self.stunned = True
        elif callable(mod.mtype):
            mod.mtype(mod.val)
        elif mod.mtype == 'lose_life':
            if self.life - mod.val > 0:
                self.life -= mod.val
            else:
                self.life = 1
        else:
            self.modifiers.append(mod)

    def get_selection_effects(self):
        return self.selection.get_effects()

    def grant_action(self, action):
        self.actions.append(action)

    def remove_action(self, action):
        self.actions.remove(action)

    def get_effects(self, trigger, passed_selection=None):
        if self.selection is not None:
            return self.selection.get_effects(trigger)
        else:
            return passed_selection.get_effects(trigger)

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
