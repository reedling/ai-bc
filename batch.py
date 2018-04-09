import argparse

from board import Board
from character_utils import get_character_list
from game import Duel
from player import Player


def main(char1, char2):
    Duel(
        Player(char1, True),
        Player(char2, True),
        Board()
    ).start()


purpose = 'Run a bunch of duels between AI agents and output results.'
parser = argparse.ArgumentParser(description=purpose)
parser.add_argument('c1', nargs=1)
parser.add_argument('c2', nargs=1)
args = parser.parse_args()

characters = get_character_list()
main(args.c1[0], args.c2[0])
