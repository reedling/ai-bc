from card import Style, Base
from card_logic import Effects, Modifier
from selection import Finisher
from utils import get_standard_bases


class SimpleBob:
    def __init__(self):
        self.styles = [
            Style('Plain', 'gray', 0, 0, 0) for i in range(5)
        ]
        self.bases = get_standard_bases()
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
