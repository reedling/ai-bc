from random import choice
from pair import Pair
from dummy import DummyAgent, Dummy
from characterUtils import getCharacterByName
from user import UserAgent
from collections import deque
from utils import getAvailableIndices

class Player:
	def __init__(self, name, aiControlled):
		self.name = name
		self.aiControlled = aiControlled
		self.life = 20
		self.position = None
		self.discardedStyles = deque()
		self.discardedBases = deque()
		#self.otherDiscards = deque()
		self.playedStyles = []
		self.playedBases = []

		if name == 'Training Dummy':
			self.character = Dummy()
			self.agent = DummyAgent()
			self.life = float('inf')
		else:
			self.character = getCharacterByName(name)
			if self.character is None:
				self.character = getCharacterByName('Simple Bob')

			if self.aiControlled:
				self.agent = DummyAgent()
			else:
				self.agent = UserAgent()


	def getAnte(self, info):
		return None

	def getStatus(self):
		return {
			'life': self.life,
			'position': self.position
		}

	def discardStyle(self, index):
		self.discardedStyles.append(index)

	def discardBase(self, index):
		self.discardedBases.append(index)

	def setInitialDiscards(self, state):
		self.discardStyle(0)
		self.discardBase(0)
		self.discardStyle(1)
		self.discardBase(1)

	def recoverDiscards(self):
		self.discardedStyles.popleft()
		self.discardedBases.popleft()

	def recycle(self):
		self.recoverDiscards()
		self.discardStyle(self.playedStyles.pop())
		self.discardBase(self.playedBases.pop())
		self.playedStyles = []
		self.playedBases = []

	def getSelection(self, state):
		stylei = choice(self.getAvailableStyles())
		basei = choice(self.getAvailableBases())
		self.playedStyles.append(stylei)
		self.playedBases.append(basei)
		return Pair(self.character.styles[stylei], self.character.bases[basei])

	def getNewBase(self, state):
		basei = choice(self.getAvailableBases())
		self.playedBases.append(basei)
		return self.character.bases[basei]

	def getAvailableStyles(self):
		return getAvailableIndices(self.character.styles, self.discardedStyles, self.playedStyles)

	def getAvailableBases(self):
		return getAvailableIndices(self.character.bases, self.discardedBases, self.playedBases)

	#def hasRemainingPlayableStyles(self): # is this needed?
	#	return len(getAvailableIndices(self.character.styles, self.discardedStyles, self.playedStyles)) > 0

	def hasRemainingPlayableBases(self):
		return len(getAvailableIndices(self.character.bases, self.discardedBases, self.playedBases)) > 0

	def getPossibleStartOfBeatBehaviors(self, selection):
		#print(selection.getEffectsForTrigger('startOfBeat'))
		# return 2 dimensional array of possible actions
		return []

	def getStartOfBeatBehavior(self, possibleBehaviors, state):
		return

	def isStunned(self):
		return False
