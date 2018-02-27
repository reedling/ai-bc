from copy import deepcopy

class Board:
	def __init__(self):
		self.spaces = [{} for i in range(7)]

	def movePlayerTo(self, player, position):
		return

	def teleportPlayerTo(self, player, position):
		return

	def setPlayerAtPosition(self, player, position):
		if 'player' in self.spaces[position - 1]:
			print('Tried to set player position to ' + position + ', but it is already occupied.')
		else:
			if player.position is not None:
				self.spaces[player.position - 1].pop('player')

			self.spaces[position - 1]['player'] = player
			player.position = position
		# need to keep track of positions traveled through

	def getStatus(self):
		return deepcopy(self.spaces)
