from pick import pick

from board import Board
from character_utils import get_character_list
from game import Duel
from player import Player


def welcome():
    return (
        '               *** BattleCON AI Project v0.1 ***\n'
        '  All rules and characters from the board game by Level 99 Games\n'
        '  Ctrl + c any time to quit\n'
        '                               ***\n\n')


def list_commands():
    return ['Start a basic duel', 'Practice', 'Quit']


def select_user_char():
    user_char, i1 = pick(get_character_list(), 'Choose your character:', '=>')
    return Player(user_char, False)


def select_user_char_and_opponent():
    user_char, i1 = pick(get_character_list(), 'Choose your character:', '=>')
    oppo_char, i2 = pick(get_character_list(), 'Choose your opponent:', '=>')
    return Player(user_char, False), Player(oppo_char, True)


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
        resp, i = pick(list_commands(), output + 'Menu:', '=>')
        output = ''

        if resp == 'Start a basic duel':
            user_player, ai_player = select_user_char_and_opponent()
            duel = Duel(user_player, ai_player, Board())
            duel.start()
        elif resp == 'Practice':
            user_player = select_user_char()
            dummy_player = Player('Training Dummy', True)
            duel = Duel(user_player, dummy_player, Board())
            duel.start()


main()
