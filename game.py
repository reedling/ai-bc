from random import randint

class Duel:
	def __init__(self, char1, char2, board):
		self.char1 = char1
		self.char2 = char2
		self.board = board
		self.beat = 1
		self.activePlayer = None
		self.activePlayerSelection = None
		self.reactivePlayer = None
		self.reactivePlayerSelection = None

	def getStateForChar(self, char, oppo):
		return {
			'me': char.getStatus(),
			'opponent': oppo.getStatus(),
			'board': self.board.getStatus(),
			'beat': self.beat
		}

	def start(self):
		self.char1.setInitialDiscards(self.getStateForChar(self.char1, self.char2))
		self.char2.setInitialDiscards(self.getStateForChar(self.char2, self.char1))
		self.board.setCharacterAtPosition(self.char1, 3);
		self.board.setCharacterAtPosition(self.char2, 5);
		while self.char1.life > 0 and self.char2.life > 0 and self.beat < 16:
			self.coordinateBeat()
			self.beat += 1

	def coordinateBeat(self):
		char1Selection = self.char1.getSelection(self.getStateForChar(self.char1, self.char2))
		char2Selection = self.char2.getSelection(self.getStateForChar(self.char2, self.char1))
		self.coordinateAntes()
		clash = self.coordinateReveal(char1Selection, char2Selection)
		while clash and self.char1.hasRemainingPlayableBases() and self.char2.hasRemainingPlayableBases():
			char1Selection.base = self.char1.getNewBase(self.getStateForChar(self.char1, self.char2))
			char2Selection.base = self.char2.getNewBase(self.getStateForChar(self.char2, self.char1))
			clash = self.handlePrioritySelection(char1Selection, char2Selection)

		if clash and (not self.char1.hasRemainingPlayableBases() or not self.char2.hasRemainingPlayableBases()):
			self.coordinateRecycle()
			return

		self.coordinateStartOfBeat()
		self.coordinateActiveAttack()
		self.coordinateReactiveAttack()

		self.coordinateRecycle()

	def coordinateAntes(self):
		def _getAnte(toAnte, nextUp, firstCall, lastAnte=None):
			ante = toAnte.getAnte(self.getStateForChar(toAnte, nextUp))
			# apply ante to board or players as necessary
			if ante is not None or lastAnte is not None or firstCall:
				_getAnte(nextUp, toAnte, False, ante)

		if self.beat == 1:
			val = randint(0, 1)
			if val == 0:
				_getAnte(self.char1, self.char2, True)
			else:
				_getAnte(self.char2, self.char1, True)
		else:
			_getAnte(self.activePlayer, self.reactivePlayer, True)

	def coordinateReveal(self, char1Selection, char2Selection):
		# will need to apply special handling for Special Actions
		# will need to take into account special modifiers outside of the styles/bases themselves as well
		# apply reveal effects for char1
		# apply reveal effects for char2
		return self.handlePrioritySelection(char1Selection, char2Selection)

	def handlePrioritySelection(self, char1Selection, char2Selection):
		if char1Selection.priority > char2Selection.priority:
			self.activePlayer = self.char1
			self.activePlayerSelection = char1Selection
			self.reactivePlayer = self.char2
			self.reactivePlayerSelection = char2Selection
		elif char1Selection.priority < char2Selection.priority:
			self.activePlayer = self.char2
			self.activePlayerSelection = char2Selection
			self.reactivePlayer = self.char1
			self.reactivePlayerSelection = char1Selection
		else: # clash!
			return True

	def coordinateStartOfBeat(self):
		activeStartOfBeat = self.activePlayer.getStartOfBeatBehavior(self.getPossibleStartOfBeatBehaviors(self.activePlayer, self.activePlayerSelection), self.getStateForChar(self.activePlayer, self.reactivePlayer))
		reactiveStartOfBeat = self.reactivePlayer.getStartOfBeatBehavior(self.getPossibleStartOfBeatBehaviors(self.reactivePlayer, self.reactivePlayerSelection), self.getStateForChar(self.reactivePlayer, self.activePlayer))

	def getPossibleStartOfBeatBehaviors(self, player, selection):
		# return 2 dimensional array of possible actions
		return []

	def coordinateActiveAttack(self):
		return

	def coordinateReactiveAttack(self):
		return

	def coordinateRecycle(self):
		# note that recycle includes end of beat effects, recycle itself, and UAs that apply at the end of every beat
		return
