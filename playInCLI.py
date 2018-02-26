from pick import pick
from board import Board
from characterUtils import getCharacterList
from player import Player
from game import Duel

def welcome():
	return (
		'                   *** BattleCON AI Project v0.1 ***\n'
		'  Built using rules and characters from the board game by Level 99 Games\n'
		'  Ctrl + c any time to quit\n'
		'                                   ***              \n\n')

def listCommands():
	return ['Start a basic duel', 'Practice', 'Quit']

def selectUserChar():
	userChar, i1 = pick(getCharacterList(), 'Choose your character:', '=>')
	return Player(userChar, False)

def selectUserCharAndOpponent():
	userChar, i1 = pick(getCharacterList(), 'Choose your character:', '=>')
	oppoChar, i2 = pick(getCharacterList(), 'Choose your opponent:', '=>')
	return Player(userChar, False), Player(oppoChar, True)

def main():
	new = True
	resp = ''
	output = ''
	while resp != 'Quit':
		if new:
			output = welcome()
			new = False
		elif len(output) > 0:
			output = output + '\n\n'
		resp, i = pick(listCommands(), output + 'Menu:', '=>')
		output = ''

		if resp == 'Start a basic duel':
			userPlayer, aiPlayer = selectUserCharAndOpponent()
			duel = Duel(userPlayer, aiPlayer, Board())
			duel.start()
		elif resp == 'Practice':
			userPlayer = selectUserChar()
			dummyPlayer = Player('Training Dummy', True)
			duel = Duel(userPlayer, dummyPlayer, Board())
			duel.start()

main()
