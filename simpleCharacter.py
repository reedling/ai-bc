from utils import getStandardBases
from card import Style, Base


class SimpleBob:
    def __init__(self):
        self.styles = [Style('Plain', 'gray', 0, 0, 0) for i in range(5)]
        self.bases = getStandardBases()
