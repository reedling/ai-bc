from pick import pick
from board import Board
from characters import Character, getCharacterList
from game import Duel

def welcome():
	return (
		'                   *** BattleCON AI Project v0.1 ***\n'
		'  Built using rules and characters from the board game by Level 99 Games\n'
		'  Ctrl + c any time to quit\n'
		'                                   ***              \n\n')

def listCommands():
	return ['Start a basic duel', 'Quit']

def selectPlayerCharAndOpponent():
	userChar, i1 = pick(getCharacterList(), 'Choose your character:', '=>')
	oppoChar, i2 = pick(getCharacterList(), 'Choose your opponent:', '=>')
	return Character(userChar, False), Character(oppoChar, True)

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
			playerChar, aiChar = selectPlayerCharAndOpponent()
			duel = Duel(playerChar, aiChar, Board())
			duel.start()

main()
