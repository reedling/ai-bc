from random import randint
from pair import Pair
from dummy import DummyAgent, Dummy

class Player:
	def __init__(self, name, aiControlled):
		self.name = name
		self.aiControlled = aiControlled
		self.life = 20
		self.position = None

		if name == 'Training Dummy':
			self.character = Dummy()
			self.agent = DummyAgent()
			self.life = float('inf')

	def getAnte(self, info):
		return None

	def getStatus(self):
		return {
			'life': self.life,
			'position': self.position
		}

	def setInitialDiscards(self, state):
		return

	def isStunned(self):
		return False

	def getSelection(self, state):
		return Pair('fake-style', 'fake-base')

	def getNewBase(self, state):
		return 'new-fake-base'

	def getStartOfBeatBehavior(self, possibleBehaviors, state):
		return

	def hasRemainingPlayableBases(self):
		val = randint(0, 9)
		if val == 0:
			return False
		else:
			return True
