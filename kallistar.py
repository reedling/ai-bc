from card import Style, Base
from card_logic import Effects, Modifier
from selection import Finisher
from utils import get_standard_bases


class Kallistar:
    def __init__(self):
        self.styles = [
            Style('Flare', 'yellow', 0, 3, 0),
            Style('Caustic', 'green', 0, 1, -1),
            Style('Blazing', 'blue', 0, 0, 1),
            Style('Volcanic', 'orange', [2, 3, 4], 0, 0),
            Style('Ignition', 'red', 0, 1, -1)
        ]
        self.bases = get_standard_bases()
        self.bases.extend([
            Base('Spellbolt', [2, 3, 4, 5, 6], 2, 3)
        ])
        self.finishers = [
            Finisher('Energy Beams I', [1, 3, 5], 7, 6, Effects([
                    Modifier('stun_immune', True)
                ]
            )),
            Finisher('Energy Beams II', [2, 4, 6], 7, 6, Effects([
                    Modifier('stun_immune', True)
                ]
            ))
        ]
