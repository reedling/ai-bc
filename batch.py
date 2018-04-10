import argparse
import time

from board import Board
from character_utils import get_character_list
from game import Duel
from player import Player


def current_milli_time():
    return int(round(time.time() * 1000))


def main(char1, char2, n, start_time):
    if n > 0:
        wins1 = 0
        wins2 = 0
        ties = 0
        for i in range(n):
            p1 = Player(char1, True)
            p2 = Player(char2, True)
            duel = Duel(
                p1,
                p2,
                Board()
            )
            duel.start()
            if duel.winner is p1:
                wins1 += 1
            elif duel.winner is p2:
                wins2 += 1
            else:
                ties += 1
        elapsed = current_milli_time() - start_time
        char1_details = (char1, wins1, wins1/n * 100)
        char2_details = (char2, wins2, wins2/n * 100)
        print('Ran {} duels in {}ms.'.format(n, elapsed))
        print('P1 ("{}") won {} duels. ({}%)'.format(*char1_details))
        print('P2 ("{}") won {} duels. ({}%)'.format(*char2_details))
        if ties > 0:
            print('There were {} ties!'.format(ties))
    else:
        print('n must be greater than 0')


purpose = 'Run a bunch of duels between AI agents and output results.'
parser = argparse.ArgumentParser(description=purpose)
parser.add_argument('c1', nargs=1)
parser.add_argument('c2', nargs=1)
parser.add_argument('n', nargs=1)
args = parser.parse_args()

characters = get_character_list()
main(args.c1[0], args.c2[0], int(args.n[0]), current_milli_time())
