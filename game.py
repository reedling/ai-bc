from random import randint

class Duel:
	def __init__(self, player1, player2, board):
		self.player1 = player1
		self.player2 = player2
		self.board = board
		self.beat = 1
		self.activePlayer = None
		self.activePlayerSelection = None
		self.reactivePlayer = None
		self.reactivePlayerSelection = None

	def getStateForPlayer(self, player, oppo):
		return {
			'me': player.getStatus(),
			'opponent': oppo.getStatus(),
			'board': self.board.getStatus(),
			'beat': self.beat
		}

	def start(self):
		self.player1.setInitialDiscards(self.getStateForPlayer(self.player1, self.player2))
		self.player2.setInitialDiscards(self.getStateForPlayer(self.player2, self.player1))
		self.board.setPlayerAtPosition(self.player1, 3);
		self.board.setPlayerAtPosition(self.player2, 5);
		while self.player1.life > 0 and self.player2.life > 0 and self.beat < 16:
			self.coordinateBeat()
			self.beat += 1

	def coordinateBeat(self):
		#print('beat {}'.format(self.beat))
		player1Selection = self.player1.getSelection(self.getStateForPlayer(self.player1, self.player2))
		player2Selection = self.player2.getSelection(self.getStateForPlayer(self.player2, self.player1))
		self.coordinateAntes()
		clash = self.coordinateReveal(player1Selection, player2Selection)
		while clash and self.player1.hasRemainingPlayableBases() and self.player2.hasRemainingPlayableBases():
			player1Selection.base = self.player1.getNewBase(self.getStateForPlayer(self.player1, self.player2))
			player2Selection.base = self.player2.getNewBase(self.getStateForPlayer(self.player2, self.player1))
			clash = self.handlePrioritySelection(player1Selection, player2Selection)

		if clash and (not self.player1.hasRemainingPlayableBases() or not self.player2.hasRemainingPlayableBases()):
			self.coordinateRecycle()
			return

		self.coordinateStartOfBeat()
		self.coordinateActiveAttack()
		self.coordinateReactiveAttack()

		self.coordinateRecycle()

	def coordinateAntes(self):
		def _getAnte(toAnte, nextUp, firstCall, lastAnte=None):
			ante = toAnte.getAnte(self.getStateForPlayer(toAnte, nextUp))
			# apply ante to board or players as necessary
			if ante is not None or lastAnte is not None or firstCall:
				_getAnte(nextUp, toAnte, False, ante)

		if self.activePlayer is None:
			val = randint(0, 1)
			if val == 0:
				_getAnte(self.player1, self.player2, True)
			else:
				_getAnte(self.player2, self.player1, True)
		else:
			_getAnte(self.activePlayer, self.reactivePlayer, True)

	def coordinateReveal(self, player1Selection, player2Selection):
		# will need to apply special handling for Special Actions
		# will need to take into account special modifiers outside of the styles/bases themselves as well
		# apply reveal effects for last active player (or randomly choose)
		# apply reveal effects for reactive player
		return self.handlePrioritySelection(player1Selection, player2Selection)

	def handlePrioritySelection(self, player1Selection, player2Selection):
		#print('p1 {}'.format(player1Selection))
		#print('p2 {}'.format(player2Selection))
		if player1Selection.priority > player2Selection.priority:
			self.activePlayer = self.player1
			self.activePlayerSelection = player1Selection
			self.reactivePlayer = self.player2
			self.reactivePlayerSelection = player2Selection
		elif player1Selection.priority < player2Selection.priority:
			self.activePlayer = self.player2
			self.activePlayerSelection = player2Selection
			self.reactivePlayer = self.player1
			self.reactivePlayerSelection = player1Selection
		else: # clash!
			#print('clash!')
			return True

	def coordinateStartOfBeat(self):
		activeStartOfBeat = self.activePlayer.getStartOfBeatBehavior(
			self.activePlayer.getPossibleStartOfBeatBehaviors(self.activePlayerSelection),
			self.getStateForPlayer(self.activePlayer, self.reactivePlayer))
		reactiveStartOfBeat = self.reactivePlayer.getStartOfBeatBehavior(
			self.reactivePlayer.getPossibleStartOfBeatBehaviors(self.reactivePlayerSelection),
			self.getStateForPlayer(self.reactivePlayer, self.activePlayer))

	def coordinateActiveAttack(self):
		return

	def coordinateReactiveAttack(self):
		return

	def coordinateRecycle(self):
		# note that recycle includes end of beat effects, recycle itself, and UAs that apply at the end of every beat
		self.activePlayer.recycle()
		self.reactivePlayer.recycle()
		return
