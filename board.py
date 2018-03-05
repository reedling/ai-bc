class Board:
    def __init__(self):
        self.spaces = [{} for i in range(7)]

    def __str__(self):
        acc = []
        for space in self.spaces:
            if 'player' in space:
                acc.append(space['player'].name[0])
            else:
                acc.append('_')
        return ' '.join(acc)

    @property
    def length(self):
        return len(self.spaces)

    # Will return True if in range.  False otherwise.
    def check_range(self, atkr, dfdr):
        targetable = self.get_positions_in_range(atkr)
        if targetable is None:
            return False
        for dist in targetable:
            if abs(atkr.position - dfdr.position) == dist:
                return True
        return False

    def get_positions_in_range(self, atkr):
        atk_range = atkr.selection.atk_range
        return atk_range

    def retreat(self, actor, nonactor, distance):
        if actor.position < nonactor.position:
            magnitude = -distance
        else:
            magnitude = distance
        self.move(actor, magnitude)

    def advance(self, actor, nonactor, distance):
        if actor.position < nonactor.position:
            magnitude = distance
        else:
            magnitude = -distance
        self.move(actor, magnitude)

    def push(self, actor, nonactor, distance):
        if actor.position < nonactor.position:
            magnitude = distance
        else:
            magnitude = -distance
        self.move(nonactor, magnitude)

    def pull(self, actor, nonactor, distance):
        if actor.position < nonactor.position:
            magnitude = -distance
        else:
            magnitude = distance
        self.move(nonactor, magnitude)

    def move(self, player, magnitude):
        if magnitude < 0:
            for i in range(magnitude, 0):
                if player.position > 0:
                    self.set(player, player.position - 1, 'left')
        else:
            for i in range(magnitude):
                if player.position < self.length - 1:
                    self.set(player, player.position + 1, 'right')

    def teleport(self, player, position):
        return

    def set(self, player, position, direction=None):
        if 'player' in self.spaces[position]:
            if direction is not None:  # attempt jump
                if direction is 'left':
                    if position > 0:
                        self.set(player, position - 1, 'left')
                    else:
                        print('Tried to jump over player at ' + str(position)
                              + ', but already at left edge of the board.')
                elif direction is 'right':
                    if position < self.length - 1:
                        self.set(player, position + 1, 'right')
                    else:
                        print('Tried to jump over player at ' + str(position)
                              + ', but already at right edge of the board.')
                else:
                    print('Tried to set player position to ' + str(position)
                          + ', but it is already occupied. '
                          + 'Invalid direction given: ' + direction)
            else:
                print('Tried to set player position to ' + str(position)
                      + ', but it is already occupied.')
        else:
            if player.position is not None:
                self.spaces[player.position].pop('player')
            self.spaces[position]['player'] = player
            player.position = position
        # need to keep track of positions traveled through

    @property
    def status(self):
        rep = [{} for i in range(self.length)]
        for j in range(self.length):
            if 'player' in self.spaces[j]:
                rep[j]['player'] = self.spaces[j]['player'].name
        return rep
