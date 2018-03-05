from random import randint

from selection import Finisher
from state import State
from utils import stacks


class Duel:
    def __init__(self, p1, p2, board):
        self.p1 = p1
        self.p2 = p2
        self.board = board
        self.beat = 1
        self.active_p = None
        self.reactive_p = None
        self.winner = None
        self.loser = None

    def state_for_player(self, player, oppo):
        return State(player, oppo, self.board, self.beat)

    def start(self):
        self.p1.select_finisher(
            self.state_for_player(self.p1, self.p2)
        )
        self.p2.select_finisher(
            self.state_for_player(self.p2, self.p1)
        )
        self.p1.init_discards(
            self.state_for_player(self.p1, self.p2)
        )
        self.p2.init_discards(
            self.state_for_player(self.p2, self.p1)
        )
        self.board.set(self.p1, 2)
        self.board.set(self.p2, 4)
        while (self.p1.life > 0
               and self.p2.life > 0
               and self.beat < 16):
            self.coordinate_beat()

            if self.winner is None:
                self.beat += 1

        self.handle_duel_end()

    def coordinate_beat(self):
        # print('beat {}'.format(self.beat))
        self.p1.refresh()
        self.p2.refresh()

        p1_sel = self.p1.get_selection(
            self.state_for_player(self.p1, self.p2))
        p2_sel = self.p2.get_selection(
            self.state_for_player(self.p2, self.p1))

        ante_finisher = self.coordinate_antes()
        if ante_finisher is not None:
            # print('FINISHER {}'.format(ante_finisher))
            if self.p1.ante_finisher:
                self.coordinate_reveal(ante_finisher, p2_sel)
            elif self.p2.ante_finisher:
                self.coordinate_reveal(p1_sel, ante_finisher)

        if ante_finisher is None:
            clash = self.coordinate_reveal(p1_sel, p2_sel)
            while (clash
                   and self.p1.has_playable_bases()
                   and self.p2.has_playable_bases()):
                p1_sel.base = self.p1.get_new_base(
                    self.state_for_player(self.p1, self.p2))
                p2_sel.base = self.p2.get_new_base(
                    self.state_for_player(self.p2, self.p1))
                clash = self.handle_priority_selection(p1_sel, p2_sel)

            if (clash
                and (not self.p1.has_playable_bases()
                     or not self.p2.has_playable_bases())):
                self.coordinate_recycle()
                return

        if self.p1.selection is None:
            self.p1.selection = p1_sel
        if self.p2.selection is None:
            self.p2.selection = p2_sel
        self.p1.apply_selection_modifiers()
        self.p2.apply_selection_modifiers()

        self.coordinate_start_of_beat()
        self.coordinate_attack(self.active_p, self.reactive_p)
        self.coordinate_attack(self.reactive_p, self.active_p)

        # Note that recycle includes end of beat effects and
        #  UAs that apply at the end of every beat
        self.coordinate_end_of_beat()
        self.coordinate_recycle()
        # print(self.board.spaces)

    def coordinate_antes(self):
        def ca(to_ante, next_up, first_invocation, last_ante=None):
            ante = to_ante.get_ante(self.state_for_player(to_ante, next_up))
            if isinstance(ante, Finisher):
                to_ante.selection = ante
                return ante
            # apply ante to board or players as necessary
            if ante is not None or last_ante is not None or first_invocation:
                return ca(next_up, to_ante, False, ante)

        if self.active_p is None:
            val = randint(0, 1)
            if val == 0:
                return ca(self.p1, self.p2, True)
            else:
                return ca(self.p2, self.p1, True)
        else:
            return ca(self.active_p, self.reactive_p, True)

    def coordinate_reveal(self, p1_selection, p2_selection):
        # Will need to apply special handling for Special Actions
        # Will need to take into account special modifiers
        #    outside of the styles/bases themselves as well
        if self.active_p is None:
            val = randint(0, 1)
            if val == 0:
                self.p1.apply_reveal_effects()
                self.p2.apply_reveal_effects()
            else:
                self.p2.apply_reveal_effects()
                self.p1.apply_reveal_effects()
        else:
            self.active_p.apply_reveal_effects()
            self.reactive_p.apply_reveal_effects()
        return self.handle_priority_selection(p1_selection, p2_selection)

    def handle_priority_selection(self, p1_selection, p2_selection):
        # print('p1 {}'.format(p1_selection))
        # print('p2 {}'.format(p2_selection))
        # print('{} vs {}'.format(p1_selection, p2_selection))
        if p1_selection.priority > p2_selection.priority:
            self.active_p = self.p1
            self.active_p.active = True
            self.reactive_p = self.p2
            self.reactive_p.active = False
        elif p1_selection.priority < p2_selection.priority:
            self.active_p = self.p2
            self.active_p.active = True
            self.reactive_p = self.p1
            self.reactive_p.active = False
        elif (isinstance(p1_selection, Finisher)
              and not isinstance(p2_selection, Finisher)):
            self.active_p = self.p1
            self.active_p.active = True
            self.reactive_p = self.p2
            self.reactive_p.active = False
        elif (isinstance(p2_selection, Finisher)
              and not isinstance(p1_selection, Finisher)):
            self.active_p = self.p2
            self.active_p.active = True
            self.reactive_p = self.p1
            self.reactive_p.active = False
        # Need to implement finishers matching priority, because this is
        # not handled in the same way as a normal clash
        else:  # Clash!
            # print('clash!')
            return True

    def coordinate_start_of_beat(self):
        active_behaviors = self.active_p.get_start_of_beat(
            self.state_for_player(self.active_p, self.reactive_p)
        )
        self.execute(active_behaviors, self.active_p, self.reactive_p)
        reactive_behaviors = self.reactive_p.get_start_of_beat(
            self.state_for_player(self.reactive_p, self.active_p)
        )
        self.execute(reactive_behaviors, self.reactive_p, self.active_p)

    def coordinate_attack(self, atkr, dfdr):
        if (not atkr.stunned):
            self.coordinate_before_activating(atkr, dfdr)
            if atkr.can_hit:
                in_range = self.board.check_range(atkr, dfdr)
                if in_range and not dfdr.dodge:
                    self.coordinate_on_hit(atkr, dfdr)
                    damage = self.apply_damage(atkr, dfdr)
                    if dfdr.life <= 0:
                        self.winner = atkr
                        self.loser = dfdr
                    if damage > 0:
                        # print('{} used {} for {}'.format(atkr, atkr.selection, damage))
                        self.coordinate_on_damage(atkr, dfdr)
            self.coordinate_after_activating(atkr, dfdr)

    def coordinate_before_activating(self, atkr, dfdr):
        behaviors = atkr.get_before_activating(
            self.state_for_player(atkr, dfdr)
        )
        self.execute(behaviors, atkr, dfdr)

    def coordinate_on_hit(self, atkr, dfdr):
        behaviors = atkr.get_on_hit(
            self.state_for_player(atkr, dfdr)
        )
        self.execute(behaviors, atkr, dfdr)

    def apply_damage(self, atkr, dfdr):
        damage = atkr.selection.power
        if damage is None or damage == 0:
            return 0

        damage = dfdr.handle_damage(damage, atkr)
        return damage

    def coordinate_on_damage(self, atkr, dfdr):
        behaviors = atkr.get_on_damage(
            self.state_for_player(atkr, dfdr)
        )
        self.execute(behaviors, atkr, dfdr)

    def coordinate_after_activating(self, atkr, dfdr):
        behaviors = atkr.get_after_activating(
            self.state_for_player(atkr, dfdr)
        )
        self.execute(behaviors, atkr, dfdr)

    def coordinate_end_of_beat(self):
        active_behaviors = self.active_p.get_end_of_beat(
            self.state_for_player(self.active_p, self.reactive_p)
        )
        self.execute(active_behaviors, self.active_p, self.reactive_p)
        reactive_behaviors = self.reactive_p.get_end_of_beat(
            self.state_for_player(self.reactive_p, self.active_p)
        )
        self.execute(reactive_behaviors, self.reactive_p, self.active_p)

    def coordinate_recycle(self):
        if self.we_have_a_winner():
            return  # skip if we have a winner

        if self.active_p is None:
            val = randint(0, 1)
            if val == 0:
                self.p1.recycle()
                self.p2.recycle()
            else:
                self.p2.recycle()
                self.p1.recycle()
        else:
            self.active_p.recycle()
            self.reactive_p.recycle()

    def execute(self, behaviors, actor, nonactor):
        def ex_with_conditionals(behavior, behavior_execution):
            if len(behavior.conditionals) == 0:
                behavior_execution()
            else:
                for c in behavior.conditionals:
                    if c.expected_val == 'changes':
                        before = c.fn(self.state_for_player(actor, nonactor))
                        behavior_execution()
                        after = c.fn(self.state_for_player(actor, nonactor))
                        if (before != after):
                            self.handle_effects(c.if_result, actor, nonactor)
                        else:
                            self.handle_effects(c.else_result, actor, nonactor)

        def ex(behavior):
            if behavior.btype == 'advance':
                ex_with_conditionals(
                    behavior,
                    lambda: self.board.advance(actor, nonactor, behavior.val)
                )
            elif behavior.btype == 'retreat':
                ex_with_conditionals(
                    behavior,
                    lambda: self.board.retreat(actor, nonactor, behavior.val)
                )
            elif behavior.btype == 'push':
                ex_with_conditionals(
                    behavior,
                    lambda: self.board.push(actor, nonactor, behavior.val)
                )
            elif behavior.btype == 'pull':
                ex_with_conditionals(
                    behavior,
                    lambda: self.board.pull(actor, nonactor, behavior.val)
                )

        for b in behaviors:
            ex(b)

    def handle_effects(self, effects, actor, nonactor):
        if effects is None:
            return

        mods = {}
        for m in effects.modifiers:
            if stacks(m.mtype) and m.mtype in mods:
                mods[m.mtype] += m.val
            else:
                mods[m.mtype] = m.val
        for mod in mods:
            actor.apply_modifier(mod, mods[mod])

    def we_have_a_winner(self):
        return self.winner is not None

    def handle_duel_end(self):
        dummy = 'Training Dummy'
        if self.p1.name == dummy or self.p2.name == dummy:
            return

        m = '{} {} {}'
        m_r = m + ' - as Reactive Player on last turn'
        m_early = m + ' - on beat {}'
        if self.winner is None:
            if self.p1.life > self.p2.life:
                print(m.format(self.p1, 'BEAT', self.p2))
            elif self.p1.life < self.p2.life:
                print(m.format(self.p2, 'BEAT', self.p1))
            else:  # Equal life in this case
                if self.reactive_p is not None:
                    print(m_r.format(self.reactive_p, 'BEAT', self.active_p))
                else:
                    print(m.format(self.p1, 'TIED', self.p2))
        else:
            print(m_early.format(self.winner, 'BEAT', self.loser, self.beat))
