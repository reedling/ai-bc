from copy import deepcopy


class Board:
    def __init__(self):
        self.spaces = [{} for i in range(7)]

    def retreat(self, actor, nonactor, distance):
        if actor.position < nonactor.position:
            magnitude = -distance
        else:
            magnitude = distance
        self.movePlayer(actor, magnitude)

    def movePlayer(self, player, magnitude):
        if magnitude < 0:
            for i in range(magnitude, 0):
                if player.position > 0:
                    self.setPlayerAtPosition(player, player.position - 1)
        else:
            for i in range(magnitude):
                if player.position < len(self.spaces) - 1:
                    self.setPlayerAtPosition(player, player.position + 1)

    def teleportPlayerTo(self, player, position):
        return

    def setPlayerAtPosition(self, player, position, direction=None):
        if 'player' in self.spaces[position]:
            if direction is not None:  # attempt jump
                if direction is 'left':
                    if position > 0:
                        self.setPlayerAtPosition(player, position - 1, 'left')
                    else:
                        print('Tried to jump over player at ' + position
                              + ', but already at left edge of the board.')
                elif direction is 'right':
                    if position < len(self.spaces) - 1:
                        self.setPlayerAtPosition(player, position + 1, 'right')
                    else:
                        print('Tried to jump over player at ' + position
                              + ', but already at right edge of the board.')
                else:
                    print('Tried to set player position to ' + position
                          + ', but it is already occupied. '
                          + 'Invalid direction given: ' + direction)
            else:
                print('Tried to set player position to ' + position
                      + ', but it is already occupied.')
        else:
            if player.position is not None:
                self.spaces[player.position].pop('player')
            self.spaces[position]['player'] = player
            player.position = position
        # need to keep track of positions traveled through

    def getStatus(self):
        return deepcopy(self.spaces)
