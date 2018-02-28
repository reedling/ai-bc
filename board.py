from copy import copy


class Board:
    def __init__(self):
        self.spaces = [{} for i in range(7)]

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

    def move(self, player, magnitude):
        if magnitude < 0:
            for i in range(magnitude, 0):
                if player.position > 0:
                    self.set(player, player.position - 1, 'left')
        else:
            for i in range(magnitude):
                if player.position < len(self.spaces) - 1:
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
                    if position < len(self.spaces) - 1:
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
        return copy(self.spaces)
