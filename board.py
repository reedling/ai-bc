from copy import deepcopy

class Board:
	def __init__(self):
		self.spaces = [{} for i in range(7)]

	def setCharacterAtPosition(self, char, position):
		if 'character' in self.spaces[position - 1]:
			print('Tried to set character position to ' + position + ', but it is already occupied.')
		else:
			if char.position is not None:
				self.spaces[char.position - 1].pop('character')

			self.spaces[position - 1]['character']= char
			char.position = position
		# need to keep track of positions traveled through per beat? not sure yet

	def getStatus(self):
		return deepcopy(self.spaces)
