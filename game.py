from random import randint

class Duel:
	def __init__(self, char1, char2, board):
		self.char1 = char1
		self.char2 = char2
		self.board = board
		self.beat = 1
		self.activePlayer = char1
		self.reactivePlayer = char2

	def getInfoForChar(self, char, oppo):
		return {
			'me': char.getStatus(),
			'opponent': oppo.getStatus(),
			'board': self.board.getStatus(),
			'beat': self.beat
		}

	def start(self):
		# self.char1.setDiscards(self.getInfoForChar(self.char1, self.char2))
		# self.char2.setDiscards(self.getInfoForChar(self.char2, self.char1))
		self.board.setCharacterAtPosition(self.char1, 3);
		self.board.setCharacterAtPosition(self.char2, 5);
		while self.char1.life > 0 and self.char2.life > 0 and self.beat < 16:
			self.coordinateBeat()
			self.beat += 1

	def coordinateBeat(self):
		# char1Style, char1Base = self.char1.getSelection(self.getInfoForChar(self.char1, self.char2))
		# char2Style, char2Base = self.char2.getSelection(self.getInfoForChar(self.char2, self.char1))
		self.coordinateAntes()
		# self.coordinateReveal()
		# while clashing continues and no one has run out of bases, do:
		#  getNewBase from each player
		#  coordinate reveal
		# if a player ran out of bases:
		#  coordinate recycle, then move to next beat
		#
		# set active player, reactive player
		# active start of beat
		# reactive start of beat
		# active attack
		# reactive attack
		# recycle

		# note that recycle includes end of beat effects, recycle itself, and UAs that apply at the end of every beat


	def coordinateAntes(self):
		def _getAnte(toAnte, nextUp, firstCall, lastAnte=None):
			ante = toAnte.getAnte(self.getInfoForChar(toAnte, nextUp))
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
