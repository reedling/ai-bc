from random import randint


class Duel:
    def __init__(self, p1, p2, board):
        self.p1 = p1
        self.p2 = p2
        self.board = board
        self.beat = 1
        self.active_p = None
        self.active_p_sel = None
        self.reactive_p = None
        self.reactive_p_sel = None

    def state_for_player(self, player, oppo):
        return {
            'me': player.status,
            'opponent': oppo.status,
            'board': self.board.status,
            'beat': self.beat
        }

    def start(self):
        self.p1.init_discards(
            self.state_for_player(self.p1, self.p2))
        self.p2.init_discards(
            self.state_for_player(self.p2, self.p1))
        self.board.set(self.p1, 2)
        self.board.set(self.p2, 4)
        while (self.p1.life > 0
               and self.p2.life > 0
               and self.beat < 16):
            self.coordinate_beat()
            self.beat += 1

    def coordinate_beat(self):
        # print('beat {}'.format(self.beat))
        p1_selection = self.p1.get_selection(
            self.state_for_player(self.p1, self.p2))
        p2_selection = self.p2.get_selection(
            self.state_for_player(self.p2, self.p1))
        self.coordinate_antes()
        clash = self.coordinate_reveal(p1_selection, p2_selection)
        while (clash
               and self.p1.has_playable_bases()
               and self.p2.has_playable_bases()):
            p1_selection.base = self.p1.get_new_base(
                self.state_for_player(self.p1, self.p2))
            p2_selection.base = self.p2.get_new_base(
                self.state_for_player(self.p2, self.p1))
            clash = self.handle_priority_selection(p1_selection, p2_selection)

        if (clash
            and (not self.p1.has_playable_bases()
                 or not self.p2.has_playable_bases())):
            self.coordinate_recycle()
            return

        self.coordinate_start_of_beat()
        self.coordinate_attack(self.active_p, self.active_p_sel,
                               self.reactive_p, self.reactive_p_sel)
        self.coordinate_attack(self.reactive_p, self.reactive_p_sel,
                               self.active_p, self.active_p_sel)

        # Note that recycle includes end of beat effects and
        #  UAs that apply at the end of every beat
        # self.coordinate_end_of_beat()
        self.coordinate_recycle()
        # print(self.board.spaces)

    def coordinate_antes(self):
        def ca(to_ante, next_up, first_invocation, last_ante=None):
            ante = to_ante.get_ante(self.state_for_player(to_ante, next_up))
            # apply ante to board or players as necessary
            if ante is not None or last_ante is not None or first_invocation:
                ca(next_up, to_ante, False, ante)

        if self.active_p is None:
            val = randint(0, 1)
            if val == 0:
                ca(self.p1, self.p2, True)
            else:
                ca(self.p2, self.p1, True)
        else:
            ca(self.active_p, self.reactive_p, True)

    def coordinate_reveal(self, p1_selection, p2_selection):
        # Will need to apply special handling for Special Actions
        # Will need to take into account special modifiers
        #    outside of the styles/bases themselves as well
        # Apply reveal effects for last active player (or randomly choose)
        # Apply reveal effects for reactive player
        return self.handle_priority_selection(p1_selection, p2_selection)

    def handle_priority_selection(self, p1_selection, p2_selection):
        # print('p1 {}'.format(p1_selection))
        # print('p2 {}'.format(p2_selection))
        if p1_selection.priority > p2_selection.priority:
            self.active_p = self.p1
            self.active_p_sel = p1_selection
            self.reactive_p = self.p2
            self.reactive_p_sel = p2_selection
        elif p1_selection.priority < p2_selection.priority:
            self.active_p = self.p2
            self.active_p_sel = p2_selection
            self.reactive_p = self.p1
            self.reactive_p_sel = p1_selection
        else:  # Clash!
            # print('clash!')
            return True

    def coordinate_start_of_beat(self):
        active_behaviors = self.active_p.get_start_of_beat(
            self.active_p.get_possible_start_of_beat(self.active_p_sel),
            self.state_for_player(self.active_p, self.reactive_p))
        self.execute(active_behaviors, self.active_p, self.reactive_p)
        reactive_behaviors = self.reactive_p.get_start_of_beat(
            self.reactive_p.get_possible_start_of_beat(self.reactive_p_sel),
            self.state_for_player(self.reactive_p, self.active_p))
        self.execute(reactive_behaviors, self.reactive_p, self.active_p)

    def coordinate_attack(self, atkr, atkr_sel, dfdr, dfdr_sel):
        if (not atkr.stunned):
            self.coordinate_before_activating(
                atkr, atkr_sel,
                dfdr, dfdr_sel
            )

    def coordinate_before_activating(self, atkr, atkr_sel, dfdr, dfdr_sel):
        behaviors = atkr.get_before_activating(
            atkr.get_possible_before_activating(atkr_sel),
            self.state_for_player(atkr, dfdr))
        self.execute(behaviors, atkr, dfdr)

    def coordinate_recycle(self):
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
        def ex(behavior):
            # print(behavior)
            if behavior.type == 'advance':
                self.board.advance(actor, nonactor, behavior.val)
            elif behavior.type == 'retreat':
                self.board.retreat(actor, nonactor, behavior.val)

        for b in behaviors:
            ex(b)
