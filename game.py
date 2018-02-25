from random import randint

class Duel:
	def __init__(self, char1, char2, board):
		self.char1 = char1
		self.char2 = char2
		self.board = board
		self.beat = 1
		self.activePlayer = None
		self.reactivePlayer = None

	def getStateForChar(self, char, oppo):
		return {
			'me': char.getStatus(),
			'opponent': oppo.getStatus(),
			'board': self.board.getStatus(),
			'beat': self.beat
		}

	def start(self):
		# self.char1.setDiscards(self.getStateForChar(self.char1, self.char2))
		# self.char2.setDiscards(self.getStateForChar(self.char2, self.char1))
		self.board.setCharacterAtPosition(self.char1, 3);
		self.board.setCharacterAtPosition(self.char2, 5);
		while self.char1.life > 0 and self.char2.life > 0 and self.beat < 16:
			self.coordinateBeat()
			self.beat += 1

	def coordinateBeat(self):
		# char1Style, char1Base = self.char1.getSelection(self.getStateForChar(self.char1, self.char2))
		# char2Style, char2Base = self.char2.getSelection(self.getStateForChar(self.char2, self.char1))
		self.coordinateAntes()
		clash = self.coordinateReveal(char1Style, char1Base, char2Style, char2Base)
		while clash and self.char1.hasPlayableBases() and self.char2.hasPlayableBases():
			# char1Base = self.char1.getNewBase(self.getStateForChar(self.char1, self.char2))
			# char2Base = self.char2.getNewBase(self.getStateForChar(self.char2, self.char1))
			clash = self.handlePrioritySelection(char1Style, char1Base, char2Style, char2Base)

		if clash and (not self.char1.hasPlayableBases() or not self.char2.hasPlayableBases()):
			self.coordinateRecycle()
			return

		# active start of beat
		# reactive start of beat
		# active attack
		# reactive attack
		# recycle

		# note that recycle includes end of beat effects, recycle itself, and UAs that apply at the end of every beat


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

	def coordinateReveal(self, char1Style, char1Base, char2Style, char2Base):
		# will need to apply special handling for Special Actions
		# will need to take into account special modifiers outside of the styles/bases themselves as well
		# apply reveal effects for char1
		# apply reveal effects for char2
		return self.handlePrioritySelection(char1Style, char1Base, char2Style, char2Base)

	def handlePrioritySelection(self, char1Style, char1Base, char2Style, char2Base):
		char1Priority = char1Style.priority + char1Base.priority
		char2Priority = char2Style.priority + char2Base.priority
		if char1Priority > char2Priority:
			self.activePlayer = self.char1
			self.reactivePlayer = self.char2
		elif char1Priority < char2Priority:
			self.activePlayer = self.char2
			self.reactivePlayer = self.char1
		else: # clash!
			return True

	def coordinateRecycle(self):
		return
