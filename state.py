class State:
    def __init__(self, player, opponent, board, beat):
        self.p = player
        self.o = opponent
        self.board = board
        self.beat = beat

    def permits(self, behavior):
        if behavior.is_move():
            x = self.permits_movement(behavior)
            return x
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
