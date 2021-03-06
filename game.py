from random import randint

from selection import Finisher
from state import State


# With 2 players and a board, coordinates a single duel.
# Invoke start() to kick off duel, which returns result string.
class Duel:
    def __init__(self, p1, p2, board, do_print=False):
        self.p1 = p1
        self.p2 = p2
        self.board = board
        self.do_print = do_print
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

        # Play 15 beats or until one player runs out of life.
        while (self.p1.life > 0
               and self.p2.life > 0
               and self.beat < 16):
            self.coordinate_beat()

            if self.winner is None:
                self.beat += 1

        # Determine victor (or see if there was a tie).
        return self.handle_duel_end()

    def coordinate_beat(self):
        self.p1.refresh()
        self.p2.refresh()

        p1_sel = self.p1.get_selection(
            self.state_for_player(self.p1, self.p2))
        p2_sel = self.p2.get_selection(
            self.state_for_player(self.p2, self.p1))

        ante_finisher = self.coordinate_antes()

        # If a finisher was anted, anteing stops, and we skip to reveal.
        # (There can be no clashes in this case.)
        if ante_finisher is not None:
            if self.p1.ante_finisher:
                self.coordinate_reveal(ante_finisher, p2_sel)
            elif self.p2.ante_finisher:
                self.coordinate_reveal(p1_sel, ante_finisher)

        # If no finisher was anted, we have to check for a clash.
        # -- While there's a clash, the players have to pick new bases.
        # -- If they don't have any remaining bases to choose, recycle.
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

        # Handle effects that are not associated with a particular trigger.
        # This is often the case for stun_guard and other modifiers.
        self.handle_effects(self.p1.get_selection_effects(), self.p1, self.p2)
        self.handle_effects(self.p2.get_selection_effects(), self.p2, self.p1)

        # Coordinate what are typically the action phases of the beat.
        self.coordinate_start_of_beat()
        self.coordinate_attack(self.active_p, self.reactive_p)
        self.coordinate_attack(self.reactive_p, self.active_p)
        self.coordinate_end_of_beat()
        self.coordinate_recycle()

    def coordinate_antes(self):
        # Some characters/selections have effects that are applied during ante.
        self.handle_effects(self.p1.get_ante_effects(), self.p1, self.p2)
        self.handle_effects(self.p2.get_ante_effects(), self.p2, self.p1)

        # Keep prompting players to ante until both players decide not to or
        # something ends the ante phase (like an anted finisher).
        def ca(to_ante, next_up, first_invocation, last_ante=None):
            ante = to_ante.get_ante(self.state_for_player(to_ante, next_up))
            if isinstance(ante, Finisher):
                to_ante.selection = ante
                return ante
            if ante is not None or last_ante is not None or first_invocation:
                return ca(next_up, to_ante, False, ante)

        # If there's no active player yet, randomly determine first ante.
        # Otherwise, active player antes first.
        if self.active_p is None:
            val = randint(0, 1)
            if val == 0:
                return ca(self.p1, self.p2, True)
            else:
                return ca(self.p2, self.p1, True)
        else:
            return ca(self.active_p, self.reactive_p, True)

    def coordinate_reveal(self, p1_selection, p2_selection):
        # Will need to apply special handling for Special Actions.
        # If there's no active player yet, randomly determine whose
        # reveal effects are applied first.
        # Otherwise, active player's effects happen first.
        trigger = 'reveal'
        if self.active_p is None:
            p1_effects = self.p1.get_effects(trigger, p1_selection)
            p2_effects = self.p2.get_effects(trigger, p2_selection)
            val = randint(0, 1)
            if val == 0:
                self.handle_effects(p1_effects, self.p1, self.p2)
                self.handle_effects(p2_effects, self.p2, self.p1)
            else:
                self.handle_effects(p2_effects, self.p2, self.p1)
                self.handle_effects(p1_effects, self.p1, self.p2)
        else:
            a = p1_selection if self.active_p is self.p1 else p2_selection
            r = p1_selection if self.reactive_p is self.p1 else p2_selection
            act_effects = self.active_p.get_effects(trigger, a)
            react_effects = self.reactive_p.get_effects(trigger, r)
            self.handle_effects(act_effects, self.active_p, self.reactive_p)
            self.handle_effects(react_effects, self.reactive_p, self.active_p)
        return self.handle_priority_selection(p1_selection, p2_selection)

    def handle_priority_selection(self, p1_selection, p2_selection):
        # Player with higher priority becomes the active player.
        # If there's a tie and *one* player used a finisher, that
        #  player wins the tie.
        # If both players use a finisher and there's a priority tie,
        #  something else happens (not implemented yet).
        # If there's a tie and neither player used a finisher, clash.
        p1_pri = p1_selection.priority + self.p1.priority
        p2_pri = p2_selection.priority + self.p2.priority
        if p1_pri > p2_pri:
            self.active_p = self.p1
            self.active_p.active = True
            self.reactive_p = self.p2
            self.reactive_p.active = False
        elif p1_pri < p2_pri:
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
        # not handled in the same way as a normal clash.
        else:  # Clash!
            return True

    def coordinate_start_of_beat(self):
        actor = self.active_p
        reactor = self.reactive_p
        trigger = 'startOfBeat'
        self.handle_effects(actor.get_effects(trigger), actor, reactor)
        self.coordinate_actions(actor, reactor, trigger)
        self.handle_effects(reactor.get_effects(trigger), reactor, actor)
        self.coordinate_actions(reactor, actor, trigger)

    def coordinate_attack(self, atkr, dfdr):
        # If stunned, before/afterActivating & onDamage/Hit do not happen
        #  because the entire attack phase is skipped.
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
                        self.coordinate_on_damage(atkr, dfdr)
            self.coordinate_after_activating(atkr, dfdr)

    def coordinate_before_activating(self, atkr, dfdr):
        trigger = 'beforeActivating'
        self.handle_effects(atkr.get_effects(trigger), atkr, dfdr)
        self.coordinate_actions(atkr, dfdr, trigger)

    def coordinate_on_hit(self, atkr, dfdr):
        trigger = 'onHit'
        self.handle_effects(atkr.get_effects(trigger), atkr, dfdr)
        self.coordinate_actions(atkr, dfdr, trigger)

    def apply_damage(self, atkr, dfdr):
        damage = atkr.selection.power + atkr.power
        if damage is None or damage == 0:
            return 0

        damage = dfdr.handle_damage(damage, atkr)
        return damage

    def coordinate_on_damage(self, atkr, dfdr):
        trigger = 'onDamage'
        self.handle_effects(atkr.get_effects(trigger), atkr, dfdr)
        self.coordinate_actions(atkr, dfdr, trigger)

    def coordinate_after_activating(self, atkr, dfdr):
        trigger = 'afterActivating'
        self.handle_effects(atkr.get_effects(trigger), atkr, dfdr)
        self.coordinate_actions(atkr, dfdr, trigger)

    def coordinate_end_of_beat(self):
        actor = self.active_p
        reactor = self.reactive_p
        trigger = 'endOfBeat'
        self.handle_effects(actor.get_effects(trigger), actor, reactor)
        self.coordinate_actions(actor, reactor, trigger)
        self.handle_effects(reactor.get_effects(trigger), reactor, actor)
        self.coordinate_actions(reactor, actor, trigger)

    def coordinate_recycle(self):
        if self.we_have_a_winner():
            return  # skip if we have a winner

        # If there's no active player when we reach the recycle phase
        #  (because someone ran out of selectable cards before the
        #  active player could be decided) then randomly decide who
        #  gets to recycle first. Generally, this won't matter.
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

    def coordinate_actions(self, actor, nonactor, trigger):
        state = self.state_for_player(actor, nonactor)

        # As long as the player has valid actions that they can perform,
        #  get the player to select their specific behavior, execute it,
        #  and then reevaluate what valid actions are available.
        permitted = [a for a in actor.actions if state.permits_action(a)]
        while len(permitted) > 0:
            chosen, behavior = actor.get_behavior(permitted, state, trigger)
            self.execute([behavior], actor, nonactor)
            actor.remove_action(chosen)
            state = self.state_for_player(actor, nonactor)
            permitted = [a for a in actor.actions if state.permits_action(a)]

    def execute(self, behaviors, actor, nonactor):
        # If there are no conditionals associated with the behavior,
        #  we can just execute it.
        # If there are conditionals, however, we may need to evaluate
        #  before/after the execution of the behavior.
        def ex_with_conditionals(behavior, behavior_execution):
            if len(behavior.conditionals) == 0:
                behavior_execution()
            else:
                self.handle_conditionals(behavior.conditionals,
                                         actor, nonactor,
                                         behavior_execution)

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
            elif behavior.btype == 'teleport':
                ex_with_conditionals(
                    behavior,
                    lambda: self.board.teleport(actor, behavior.val)
                )

        for b in behaviors:
            ex(b)

    def handle_effects(self, effects, actor, nonactor):
        if effects is None:
            return

        if not isinstance(effects, list):
            effects = [effects]
        for e in effects:
            # Handle all associated modifiers, actions, and conditionals.
            # Given that conditionals contain other effects, this may
            #  lead to new effects being handled.
            self.handle_modifiers(e.modifiers, actor, nonactor)
            self.grant_actions(e.actions, actor, nonactor)
            self.handle_conditionals(e.conditionals, actor, nonactor)

    # (Most modifiers apply to the actor, but some apply to their opponent.)
    def handle_modifiers(self, modifiers, actor, nonactor):
        mods = []
        omods = []
        for m in modifiers:
            if m.opponent:
                omods.append(m)
            else:
                mods.append(m)
        for mod in mods:
            actor.handle_modifier(mod)
        for omod in omods:
            nonactor.handle_modifier(omod)

    # Adds to the list of actions that are available to the player this beat.
    # See 'coordinate_actions' above for details on how valid actions are
    #  chosen and executed.
    def grant_actions(self, actions, actor, nonactor):
        for a in actions:
            actor.grant_action(a)

    # For most conditionals, we just need to evaluate once.
    # For conditionals with type 'changes' that are associated with actions,
    #  we must evaluate them both before and after the execution.
    def handle_conditionals(self, conditionals, actor, nonactor,
                            behavior_execution=None):
        before = {}
        for c in conditionals:
            if c.type == 'changes':
                before[c] = c.fn(self.state_for_player(actor, nonactor))
            else:
                if c.fn(self.state_for_player(actor, nonactor)) == c.expected:
                    self.handle_effects(c.if_result, actor, nonactor)
                else:
                    self.handle_effects(c.else_result, actor, nonactor)
        if behavior_execution is not None:
            behavior_execution()

        # Right now this only has handling for type 'changes'.  May need
        #  another type for the opposite behavior or even more complex
        #  conditions.
        for cond in before:
            beforeVal = before[cond]
            if cond.fn(self.state_for_player(actor, nonactor)) != beforeVal:
                self.handle_effects(cond.if_result, actor, nonactor)
            else:
                self.handle_effects(cond.else_result, actor, nonactor)

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
            # Ran out of beats instead of a player's life hitting 0
            #  (or some other win condition).
            if self.p1.life > self.p2.life:
                self.winner = self.p1
                res = m.format(self.p1, 'BEAT', self.p2)
            elif self.p1.life < self.p2.life:
                self.winner = self.p2
                res = m.format(self.p2, 'BEAT', self.p1)
            else:  # Players have equal life in this case.
                # Reactive player wins on a tie.
                if self.reactive_p is not None:
                    self.winner = self.reactive_p
                    res = m_r.format(self.reactive_p, 'BEAT', self.active_p)
                else:
                    # This seems improbabl3 -- they would need to run out
                    #  of cards before selections could be determined every
                    #  single beat...
                    res = m.format(self.p1, 'TIED', self.p2)
        else:
            res = m_early.format(self.winner, 'BEAT', self.loser, self.beat)

        if self.do_print:
            print(res)
        return res
