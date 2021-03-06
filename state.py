class State:
    def __init__(self, player, opponent, board, beat):
        self.p = player
        self.o = opponent
        self.board = board
        self.beat = beat

    def get_permitted_behaviors(self, action):
        a = action
        need_state = action.needs_state_for_behaviors
        behaviors = a.behaviors_for_state(self) if need_state else a.behaviors
        return [b for b in behaviors if self.permits(b)]

    def permits_action(self, action):
        return len(self.get_permitted_behaviors(action)) > 0

    def permits(self, behavior):
        if behavior.is_move():
            x = self.permits_movement(behavior)
            return x
        elif behavior.btype == 'teleport':
            return not self.board.position_is_occupied(behavior.val)
        else:
            return True

    def permits_movement(self, behavior):
        ok = True
        if self.p.position < self.o.position:
            if behavior.btype == 'advance':
                ok = self.movement_fits(self.p, self.o, behavior.val)
            elif behavior.btype == 'retreat':
                ok = self.movement_fits(self.p, self.o, -behavior.val)
            elif behavior.btype == 'push':
                ok = self.movement_fits(self.o, self.p, behavior.val)
            elif behavior.btype == 'pull':
                ok = self.movement_fits(self.o, self.p, -behavior.val)
        elif self.p.position > self.o.position:
            if behavior.btype == 'advance':
                ok = self.movement_fits(self.p, self.o, -behavior.val)
            elif behavior.btype == 'retreat':
                ok = self.movement_fits(self.p, self.o, behavior.val)
            elif behavior.btype == 'push':
                ok = self.movement_fits(self.o, self.p, -behavior.val)
            elif behavior.btype == 'pull':
                ok = self.movement_fits(self.o, self.p, behavior.val)
        else:
            print('Unknown movement type received: {}'.format(behavior.btype))
        return ok

    def movement_fits(self, mover, other, magnitude):
        noJumps = mover.position + magnitude
        if noJumps >= 0 and noJumps < self.board.length:
            if (magnitude < 0
                    and other.position < mover.position
                    and other.position >= noJumps):
                return (noJumps - 1) >= 0
            elif (magnitude > 0
                    and other.position > mover.position
                    and other.position <= noJumps):
                return (noJumps + 1) < self.board.length
            else:
                return True
        else:
            return False
